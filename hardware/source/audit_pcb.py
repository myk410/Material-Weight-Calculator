"""Check actual KiCad pad nets, copper geometry and mechanical registration.

Requires KiCad 9 pcbnew. The source JSON is checked against the saved board;
critical device connections below are also checked against explicit datasheet
pin assignments rather than inferred from the board generator's labels.
"""
from collections import Counter
from pathlib import Path
import ast
import json
import xml.etree.ElementTree as E
import pcbnew as k

ROOT = Path(__file__).resolve().parents[1]


def point(v):
    return (round(v.x / 1e6 - 50, 4), round(v.y / 1e6 - 50, 4))


def run():
    reports, boards, definitions = {}, {}, {}
    for adapter in (False, True):
        name = 'adapter' if adapter else 'main'
        folder = ROOT / 'pcb' / 'display_adapter' if adapter else ROOT / 'pcb'
        stem = 'display_adapter' if adapter else 'material_weight_calculator'
        data = json.loads((ROOT / 'source' / ('adapter_electrical_design.json' if adapter else 'electrical_design.json')).read_text())
        board = k.LoadBoard(str(folder / (stem + '.kicad_pcb')))
        boards[name] = board
        definitions[name] = {c['ref']: c for c in data['components']}
        expected = {(c['ref'], p): n for c in data['components'] for p, n in c['pins'].items() if n}
        actual = {}
        pads = {(p['ref'], p['pin']): p for p in data['pads']}
        for fp in board.GetFootprints():
            c = definitions[name][fp.GetReference()]
            assert point(fp.GetPosition()) == (round(c['x'],4), round(c['y'],4)), (name, c['ref'], point(fp.GetPosition()), (c['x'],c['y']))
            assert fp.GetFPIDAsString() == c['footprint']
            for pad in fp.Pads():
                key = (fp.GetReference(), pad.GetNumber())
                assert point(pad.GetPosition()) == (round(pads[key]['x'], 4), round(pads[key]['y'], 4)), key
                assert abs(pad.GetDrillSize().x / 1e6 - pads[key]['drill']) < 1e-6
                n = pad.GetNetname()
                if n and not n.startswith('unconnected-'): actual[key] = n
        assert expected == actual, name
        schema = {}
        for net in E.parse(folder / (stem + '.net.xml')).findall('.//nets/net'):
            n = net.get('name')
            if n.startswith('unconnected-'): continue
            for node in net.findall('node'):
                if not node.get('ref').startswith('#'):
                    schema[node.get('ref'), node.get('pin')] = n
        assert schema == actual, name

        def seg(n, layer, a, b, width):
            return (n, layer, tuple(sorted((tuple(round(v, 4) for v in a), tuple(round(v, 4) for v in b)))), round(width, 6))
        tracks = Counter(); vias = Counter()
        for track in board.GetTracks():
            if isinstance(track, k.PCB_VIA):
                vias[(track.GetNetname(), point(track.GetPosition()), track.GetWidth(k.F_Cu)/1e6, track.GetDrillValue()/1e6)] += 1
            else:
                layer = 0 if track.GetLayer() == k.F_Cu else 1
                tracks[seg(track.GetNetname(), layer, point(track.GetStart()), point(track.GetEnd()), track.GetWidth()/1e6)] += 1
        assert tracks == Counter(seg(t['net'], t['layer'], t['a'], t['b'], t['width']) for t in data['routes']), name
        assert vias == Counter((v['net'], (round(v['x'],4),round(v['y'],4)), 1.0, .5) for v in data['vias']), name
        box = board.GetBoardEdgesBoundingBox()
        # Edge bounding box includes half the 0.05 mm outline stroke on each side.
        size = [round(box.GetWidth()/1e6 - .05, 3), round(box.GetHeight()/1e6 - .05, 3)]
        assert size == data['board_size_mm'], size
        reports[name] = {'result': 'PASS', 'connected_pins': len(actual), 'track_segments': sum(tracks.values()),
                         'vias': sum(vias.values()), 'size_mm': size, 'pad_positions_drills_and_copper_match_source': True}

    m, a = definitions['main'], definitions['adapter']
    # Microchip DS40002183E, 28-pin SPDIP; DS20001826F, TO-92;
    # onsemi 2N3906/D; EastRising ERC12864-655 Rev1.0 pp7-9.
    assert {p:m['U1']['pins'][p] for p in ['14','15','19','20','21','23','24','25','26','27','13']} == {
        '14':'+3V3','15':'GND','19':'UPDI','20':'+3V3','21':'GND','23':'LCD_CLK','24':'LCD_DATA','25':'LCD_CS','26':'LCD_CD','27':'LCD_RST','13':'LCD_PWR_CTRL'}
    assert m['U2']['pins'] == {'1':'GND','2':'VIN','3':'+3V3'}
    assert m['D1']['pins'] == {'1':'VIN','2':'VBAT_LINK'}  # cathode, anode
    assert m['Q1']['pins'] == {'1':'+3V3','2':'LCD_BASE','3':'LCD_VCC'}  # E B C
    assert m['J2']['pins'] == {'1':'VBAT_SW','2':'GND'}
    assert m['JP1']['pins'] == {'1':'VBAT_SW','2':'VBAT_LINK'}
    assert m['J3']['pins'] == a['J1']['pins']
    assert m['J4']['pins'] == {'1':'+3V3','2':'GND','3':'UPDI'}
    # Main mounting positions must register with the case's actual source, not
    # just its board proxy. Parse the literal list without executing CAD exports.
    tree = ast.parse((ROOT/'source'/'build_case.py').read_text())
    holes = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t,ast.Name) and t.id=='pcbholes' for t in n.targets))
    params = json.loads((ROOT/'source'/'mechanical_parameters.json').read_text())
    origin = params['pcb_origin_plan_mm']
    mounted = [(m['H'+str(i)]['x']+origin[0], m['H'+str(i)]['y']+origin[1]) for i in range(1,5)]
    assert mounted == holes
    for board_name, refs in [('main', ['C1','C2','C5']),('adapter',['C1','C2'])]:
        for ref in refs:
            c=definitions[board_name][ref]
            assert c['value']=='2.2uF 50V X7R' and c['manufacturer_part_number']=='FG14X7R1H225KRT00'
    # Nominal installed height of the selected flying caps, not a full CAD fit test.
    assert 13 + 1.6 + 5.5 + .5 <= 22.1
    result={'revision':'R2.1','result':'PASS','boards':reports,'critical_pin_maps':'PASS',
            'main_holes_match_case_source':True,'selected_adapter_capacitor_height_clearance_mm':2.0,
            'limits':['No bench measurements or physical assembly test.',
                      'Generic remaining passive footprints still require selected-part body/lead checks.',
                      'Nominal capacitor height arithmetic is not a populated-component CAD collision test.']}
    (ROOT/'validation'/'pcb_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__': run()
