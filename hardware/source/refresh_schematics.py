"""Refresh checkable schematics/board metadata without moving or rerouting copper.

Run with KiCad 9 pcbnew Python. Embedded symbols and the project symbol library
come from the same definition. Pin types describe the configured application;
connector power outputs represent externally supplied power, not active headers.
"""
from pathlib import Path
import csv
import json
import uuid
import pcbnew as k

ROOT = Path(__file__).resolve().parents[1]
REV = 'R2.1'
NS = uuid.UUID('f58f5474-d858-4f91-84cd-169369ee392e')
PLUGIN = k.PCB_IO_KICAD_SEXPR()
# Keep plugin-owned objects alive across both boards (KiCad 9 SWIG ownership).
KEEP_ALIVE = []


def refresh(adapter=False, r3=False):
    folder = ROOT / 'pcb' / 'r3' / 'display_adapter' if r3 and adapter else ROOT / 'pcb' / 'r3' if r3 else ROOT / 'pcb' / 'display_adapter' if adapter else ROOT / 'pcb'
    stem = 'display_adapter' if adapter else 'material_weight_calculator'
    datafile = ROOT / 'source' / ('r3_adapter_electrical_design.json' if r3 and adapter else 'r3_electrical_design.json' if r3 else 'adapter_electrical_design.json' if adapter else 'electrical_design.json')
    data = json.loads(datafile.read_text())
    board = k.LoadBoard(str(folder / (stem + '.kicad_pcb')))
    def uid(key): return str(uuid.uuid5(NS, stem + '/' + key))
    def q(value): return json.dumps(str(value))
    # Exact global names allow KiCad's native schematic-parity check, including GND.
    rename = {} if adapter else {'BAT_PLUS': 'VBAT_SW', 'BAT_SWITCH': 'VBAT_LINK'}
    for net in list(board.GetNetsByName().values()):
        if net.GetNetname() in rename:
            net.SetNetname(rename[net.GetNetname()])
    plugin = PLUGIN
    KEEP_ALIVE.append(board)
    for entry in data['components']:
        entry['pins'] = {p: rename.get(n, n) for p, n in entry['pins'].items() if p}
        if not adapter and entry['ref'] == 'J2':
            entry['value'] = 'SWITCHED_3AAA_IN'
            entry['pin_names'] = {'1': 'SW1_OUT_PLUS', '2': 'BAT_MINUS'}
        if not r3 and entry['ref'] in (('C1', 'C2') if adapter else ('C1', 'C2', 'C5')):
            fp = 'C_Radial_L4.5mm_W3.0mm_P2.50mm'
            entry['footprint'] = 'MW_footprints:' + fp
            entry['value'] = '2.2uF 50V X7R'
            entry['manufacturer_part_number'] = 'FG14X7R1H225KRT00'
            old = next(f for f in board.GetFootprints() if f.GetReference() == entry['ref'])
            if old.GetFPIDAsString() != 'MW_footprints:' + fp:
                new = plugin.FootprintLoad(str(folder / 'mw-footprints.pretty'), fp, False)
                new.SetReference(entry['ref']); new.SetValue(entry['value'])
                new.SetFPIDAsString('MW_footprints:' + fp)
                new.SetPosition(old.GetPosition()); new.SetOrientation(old.GetOrientation())
                new.Value().SetVisible(False)
                for pad in new.Pads():
                    original = next(p for p in old.Pads() if p.GetNumber() == pad.GetNumber())
                    pad.SetNet(original.GetNet())
                KEEP_ALIVE.extend((old, new))
                board.Remove(old); board.Add(new)
    for entry in data['pads'] + data['routes'] + data['vias']:
        entry['net'] = rename.get(entry['net'], entry['net'])

    positions = ({'J2': (75, 75), 'J1': (160, 75), 'C1': (225, 50),
                  'C2': (275, 50), 'C3': (325, 50), 'C4': (375, 50),
                  'C5': (225, 100), 'R1': (275, 100), 'H1': (325, 100), 'H2': (375, 100)}
                 if adapter else
                 {'J2': (40, 30), 'JP1': (90, 30), 'D1': (140, 30), 'U2': (190, 30),
                  'C1': (245, 30), 'C2': (300, 30), 'Q1': (355, 30),
                  'J1': (40, 100), 'U1': (115, 100), 'J3': (200, 100),
                  'J4': (270, 100), 'R1': (325, 80), 'R2': (375, 80),
                  'C3': (270, 135), 'C4': (325, 135), 'C5': (375, 135),
                  'H1': (40, 155), 'H2': (90, 155), 'H3': (140, 155), 'H4': (190, 155)})
    if r3 and not adapter:
        positions.update({'L1': (245, 175), 'R3': (40, 175), 'R4': (90, 175),
                          'R5': (140, 175), 'R6': (190, 175), 'C6': (300, 175),
                          'R7': (355, 175), 'C7': (40, 220), 'D2': (90, 220),
                          'R8': (140, 220), 'TP1': (190, 220),
                          'TP2': (245, 220), 'TP3': (300, 220)})
    symbols, instances, wires = [], [], []
    power_flags = []
    def pin_type(ref, pin, connected):
        if adapter:
            if ref == 'J1':
                return 'power_out' if pin in ('1', '2') else 'output'
            if ref == 'J2':
                if pin in ('14', '15'): return 'power_in'
                if pin in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '21', '22'): return 'input'
                if pin == '20': return 'power_out'
        else:
            if ref == 'U1':
                if pin in ('14', '15', '20', '21'): return 'power_in'
                if pin == '18': return 'input'
                return 'bidirectional'
            if ref == 'U2':
                if r3:
                    return {'1':'output', '2':'input', '3':'bidirectional',
                            '4':'bidirectional', '5':'power_in', '6':'power_out',
                            '7':'power_in', '8':'input', '9':'input', '10':'output'}[pin]
                return 'power_out' if pin == '3' else 'power_in'
            if ref == 'Q1': return ({'1':'input','2':'power_in','3':'power_out'} if r3 else {'1':'power_in','2':'input','3':'power_out'})[pin]
            if ref == 'J2': return 'power_out'
        return 'passive'

    for c in data['components']:
        ref, pins = c['ref'], c['pins']
        left = len(pins) if len(pins) < 10 else len(pins) // 2
        count = max(left, len(pins) - left)
        # All connection points on 1.27 mm grid, including short two-pin blocks.
        halfh = max(5.08, (count + 1) * 1.27)
        half, px = 10.16, 15.24
        symname = 'MW_' + ref
        pinstr = []
        x, y = (round(v / 1.27) * 1.27 for v in positions[ref])
        for idx, num in enumerate(sorted(pins, key=int)):
            side = idx < left
            iy = idx if side else idx - left
            yy = halfh - (iy + 1) * 2.54
            xx, angle = (-px, 0) if side else (px, 180)
            name = c.get('pin_names', {}).get(num, num)
            ptype = pin_type(ref, num, bool(pins[num]))
            pinstr.append(f'(pin {ptype} line (at {xx:.4f} {yy:.4f} {angle}) (length 5.08) (name {q(name)} (effects (font (size .9 .9)))) (number {q(num)} (effects (font (size .9 .9)))))')
            wx, wy = x + xx, y - yy
            net = pins[num]
            if net:
                end = wx + (-7.62 if side else 7.62)
                wires.append(f'(wire (pts (xy {wx:.4f} {wy:.4f}) (xy {end:.4f} {wy:.4f})) (stroke (width 0) (type default)) (uuid {uid(ref+num+"wire")}))')
                wires.append(f'(global_label {q(net)} (shape passive) (at {end:.4f} {wy:.4f} {0 if side else 180}) (effects (font (size .9 .9)) (justify {"left" if side else "right"})) (uuid {uid(ref+num+"label")}))')
                if not adapter and ref == 'C1' and num == '1':
                    power_flags.append((wx, wy))
            else:
                wires.append(f'(no_connect (at {wx:.4f} {wy:.4f}) (uuid {uid(ref+num+"nc")}))')
        symbol = (f'(symbol {q(symname)} (pin_names (offset .508)) (in_bom yes) (on_board yes) '
                  f'(property "Reference" {q(ref)} (at 0 {halfh+4:.4f} 0) (effects (font (size 1 1)))) '
                  f'(property "Value" {q(c["value"])} (at 0 {halfh+1.5:.4f} 0) (effects (font (size 1 1)))) '
                  f'(symbol {q(symname+"_0_1")} (rectangle (start {-half} {-halfh:.4f}) (end {half} {halfh:.4f}) (stroke (width .254) (type default)) (fill (type background)))) '
                  f'(symbol {q(symname+"_1_1")} {" ".join(pinstr)}))')
        symbols.append(symbol)
        props = (f'(property "Reference" {q(ref)} (at {x:.4f} {y-halfh-4:.4f} 0) (effects (font (size 1.1 1.1)))) '
                 f'(property "Value" {q(c["value"])} (at {x:.4f} {y-halfh-1.5:.4f} 0) (effects (font (size 1 1)))) '
                 f'(property "Footprint" {q(c["footprint"])} (at {x:.4f} {y:.4f} 0) (effects (font (size 1 1)) hide))')
        instpins = ' '.join(f'(pin {q(n)} (uuid {uid(ref+n+"pin")}))' for n in pins)
        instances.append(f'(symbol (lib_id "MW:{symname}") (at {x:.4f} {y:.4f} 0) (unit 1) (in_bom {"no" if ref.startswith(("H", "TP")) else "yes"}) (on_board yes) (uuid {uid(ref)}) {props} {instpins})')
        c['schematic_uuid'] = uid(ref)

    # VIN is supplied through passive diode D1. The explicit flag documents this
    # source after the diode so ERC checks U2 VIN without retyping it as passive.
    if power_flags:
        symbols.append('(symbol "PWR_FLAG" (power) (pin_names (offset 0)) (in_bom no) (on_board no) (property "Reference" "#FLG" (at 0 2 0) (effects (font (size 1 1)) hide)) (property "Value" "PWR_FLAG" (at 0 4 0) (effects (font (size 1 1)) hide)) (symbol "PWR_FLAG_0_1" (polyline (pts (xy 0 0) (xy 0 1.27) (xy -1.27 1.9) (xy 0 2.54) (xy 1.27 1.9) (xy 0 1.27)) (stroke (width .15) (type default)) (fill (type none)))) (symbol "PWR_FLAG_1_1" (pin power_out line (at 0 0 90) (length 0) (name "pwr" (effects (font (size 1 1)))) (number "1" (effects (font (size 1 1)))))))')
        for i, (x, y) in enumerate(power_flags):
            instances.append(f'(symbol (lib_id "MW:PWR_FLAG") (at {x:.4f} {y:.4f} 0) (unit 1) (in_bom no) (on_board no) (uuid {uid("flag")}) (property "Reference" "#FLG01" (at {x} {y} 0) (effects (font (size 1 1)) hide)) (property "Value" "PWR_FLAG" (at {x} {y} 0) (effects (font (size 1 1)) hide)) (pin "1" (uuid {uid("flagpin")})))')
    library = '(kicad_symbol_lib (version 20220914) (generator kicad_symbol_editor) ' + ' '.join(symbols) + ')'
    (folder / 'MW.kicad_sym').write_text(library)
    (folder / 'sym-lib-table').write_text('(sym_lib_table (lib (name "MW")(type "KiCad")(uri "${KIPRJMOD}/MW.kicad_sym")(options "")(descr "Project symbols with application pin types")))')
    embedded = ' '.join(s.replace('(symbol "MW_', '(symbol "MW:MW_', 1).replace('(symbol "PWR_FLAG"', '(symbol "MW:PWR_FLAG"', 1) for s in symbols)
    paths = ' '.join(f'(path "/{c["schematic_uuid"]}" (reference {q(c["ref"])}) (unit 1) (value {q(c["value"])}) (footprint {q(c["footprint"])}))' for c in data['components'])
    if power_flags: paths += f' (path "/{uid("flag")}" (reference "#FLG01") (unit 1) (value "PWR_FLAG") (footprint ""))'
    notes = (['J1 supplies switched 3.3 V and ground from main J3; connect matching pin numbers.',
              'J2 is the LCD pin landing, not a separate header. Verify front-view pin 1.',
              'A/K backlight contacts remain insulated and unconnected.'] if adapter else
             ['External wiring: AAA+ -> SW1 common; SW1 outer -> J2.1; AAA- -> J2.2.',
              'CYT1107 SW1 is case-mounted. Insulate unused outer terminal. JP1 shunt normally fitted.',
              'J4: 1=3V3, 2=GND, 3=UPDI. Remove batteries for programmer-supplied power.',
              'Q1: PD7 low = LCD on. Keep LCD signal pins low while LCD power is off.',
              'C2 must retain at least 1 uF effective capacitance over voltage/temperature/tolerance.'])
    if r3 and not adapter:
        notes = ['R3 LTC3440EMS MSOP-10 only. VC -> R6 -> C6 -> FB (NOT ground).',
                 'D2: K=VIN A=SW1; R7/C7: SW1-to-ground snubber for VIN above 4.5V.',
                 'J2 switched battery positive; JP1 service shunt; SS14 D1 cathode to VIN.',
                 'MODE via R8 to VIN; SHDN tied to VIN. No RC soft start fitted.',
                 'FABRICATION HOLD: physical LCD/keypad/programmer/switch mating remains unverified.',
                 'J4: remove batteries before programmer power. Never connect two power sources.',
                 'All components on F.Cu; underside drawing is mirrored; U1 notch at pins 1/28.']
    if r3 and adapter:
        notes += ['R3: all passive parts are SMD. C5 is ceramic/nonpolar, not an electrolytic.',
                  'Use owned 0603 kits only after rating, dielectric and value qualification.']
    notes += ['Prototype: firmware and physical assembly tests pending. See PCB_REVIEW.md.',
              'Power pins on source connectors describe external supplies; Q1 collector is switched power output.']
    for i, note in enumerate(notes):
        wires.append(f'(text {q(note)} (at 20 {(235+i*5 if r3 else 190+i*6)} 0) (effects (font (size 1.2 1.2)) (justify left)) (uuid {uid("note"+str(i))}))')
    title = 'UC1701 Display Adapter' if adapter else 'Material Weight Calculator'
    schematic = (f'(kicad_sch (version 20230121) (generator eeschema) (uuid {uid("root")}) (paper "A3") '
                 f'(title_block (title {q(title)}) (date "2026-11-12") (rev "{("R3" if r3 else REV)}") (comment 1 "Prototype - FABRICATION HOLD")) '
                 f'(lib_symbols {embedded}) {" ".join(wires)} {" ".join(instances)} '
                 f'(sheet_instances (path "/" (page "1"))) (symbol_instances {paths}))')
    (folder / (stem + '.kicad_sch')).write_text(schematic)
    for footprint in board.GetFootprints():
        c = next(c for c in data['components'] if c['ref'] == footprint.GetReference())
        footprint.SetValue(c['value'])
        for pad in footprint.Pads():
            pin = pad.GetNumber()
            if pin and not c['pins'].get(pin):
                name = c.get('pin_names', {}).get(pin, '')
                nc = f'unconnected-({c["ref"]}-' + (name + '-' if name else '') + f'Pad{pin})'
                net = board.FindNet(nc)
                if net is None:
                    net = k.NETINFO_ITEM(board, nc); board.Add(net)
                pad.SetNet(net)
        footprint.SetPath(k.KIID_PATH('/' + uid('root') + '/' + c['schematic_uuid']))
    # Refresh only our board text, retaining all footprint locations and copper.
    for drawing in board.GetDrawings():
        if isinstance(drawing, k.PCB_TEXT):
            value = drawing.GetText()
            if value == 'JP1: SERVICE LINK': drawing.SetPosition(k.VECTOR2I(k.FromMM(69), k.FromMM(109)))
            if value == 'MATERIAL WEIGHT R2': drawing.SetText('MATERIAL WEIGHT R2.1')
            if value == 'UC1701 R2': drawing.SetText('UC1701 R2.1')
            if value == 'J3: UC1701 8-WIRE': drawing.SetText('J3: 7 WIRES / 8 PADS')
    if not adapter and not any(isinstance(d, k.PCB_TEXT) and d.GetText() == 'J2: SW+ / GND' for d in board.GetDrawings()):
        for text, x, y in [('J2: SW+ / GND', 62, 60), ('JP1: SERVICE LINK', 19, 59)]:
            item = k.PCB_TEXT(board); item.SetText(text)
            item.SetPosition(k.VECTOR2I(k.FromMM(x+50), k.FromMM(y+50)))
            item.SetTextSize(k.VECTOR2I(k.FromMM(.8), k.FromMM(.8)))
            item.SetTextThickness(k.FromMM(.12)); item.SetLayer(k.F_SilkS); board.Add(item)
    k.SaveBoard(str(folder / (stem + '.kicad_pcb')), board)
    datafile.write_text(json.dumps(data, indent=2) + '\n')
    with (folder / 'bom.csv').open('w', newline='') as out:
        writer = csv.writer(out,lineterminator="\n"); writer.writerow(['Reference', 'Value', 'Footprint', 'ManufacturerPartNumber'])
        writer.writerows((c['ref'], c['value'], c['footprint'], c.get('manufacturer_part_number', '')) for c in data['components'])
    print('Refreshed', stem)


if __name__ == '__main__':
    refresh(False)
    refresh(True)
