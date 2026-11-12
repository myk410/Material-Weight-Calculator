"""Independent R3 electrical/orientation checks against saved KiCad boards.
CAD pass is deliberately separate from real-part physical evidence.
"""
from pathlib import Path
import json, hashlib, xml.etree.ElementTree as E, csv
import pcbnew as k
ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'pcb'/'r3'; REPORT=ROOT/'validation'/'r3'
STEM='material_weight_calculator'
def actual(board):
    return {(f.GetReference(),p.GetNumber()):p for f in board.GetFootprints() for p in f.Pads() if p.GetNumber()}
def net(p):
    n=p.GetNetname()
    return '' if n.startswith('unconnected-') else n
def check(pads,ref,number,n,x=None,y=None):
    p=pads[ref,str(number)]
    assert net(p)==n,(ref,number,'net',net(p),n)
    if x is not None:assert abs(p.GetPosition().x/1e6-50-x)<.005,(ref,number,'x')
    if y is not None:assert abs(p.GetPosition().y/1e6-50-y)<.005,(ref,number,'y')
def contracts(main,adapter):
    # ADI 3440fd p2 MS top view, independently frozen; no center pad 11.
    expected={'1':'RT','2':'MODE','3':'SW1','4':'SW2','5':'GND','6':'+3V3','7':'VIN','8':'VIN','9':'FB','10':'VC'}
    for p,n in expected.items():
        i=int(p);check(main,'U2',p,n,22.8875 if i<=5 else 27.1125,15+.5*(i-1) if i<=5 else 17-.5*(i-6))
    assert ('U2','11') not in main
    for ref,pins in {'R3':['RT','GND'],'R4':['+3V3','FB'],'R5':['FB','GND'],
                     'R6':['VC','COMP_NODE'],'C6':['COMP_NODE','FB'],'R8':['MODE','VIN'],
                     'L1':['SW1','SW2'],'C1':['VIN','GND'],'C2':['+3V3','GND'],
                     'D1':['VIN','VBAT_LINK'],'D2':['VIN','SW1'],'R7':['SW1','SNUB'],
                     'C7':['SNUB','GND'],'Q1':['LCD_BASE','+3V3','LCD_VCC']}.items():
        for i,n in enumerate(pins,1):check(main,ref,i,n)
    # Cathode bar orientation, viewed from F.Cu.
    check(main,'D1',1,'VIN',12,5);check(main,'D1',2,'VBAT_LINK',16,5)
    check(main,'D2',1,'VIN',26.4,22.5);check(main,'D2',2,'SW1',23.6,22.5)
    # onsemi MMBT3906: pin 1 B, 2 E, 3 C; SOT-23 top-view footprint.
    check(main,'Q1',1,'LCD_BASE',56.5,14.05)
    check(main,'Q1',2,'+3V3',56.5,15.95)
    check(main,'Q1',3,'LCD_VCC',59.5,15)
    # Microchip DS40002183 28-SPDIP. Notch at top. All socket contacts fixed.
    u1=['','ROW0','ROW1','ROW2','ROW3','COL0','COL1','COL2','COL3','','','','LCD_PWR_CTRL','+3V3','GND','','','','UPDI','+3V3','GND','','LCD_CLK','LCD_DATA','LCD_CS','LCD_CD','LCD_RST','']
    for i,n in enumerate(u1,1):check(main,'U1',i,n,35 if i<=14 else 42.62,20+(i-1 if i<=14 else 28-i)*2.54)
    for i,n in enumerate(['ROW0','ROW1','ROW2','ROW3','COL0','COL1','COL2','COL3'],1):check(main,'J1',i,n,12,22.54+(i-1)*2.54)
    for ref,pins,x,y in [('J2',['VBAT_SW','GND'],10,9),('JP1',['VBAT_SW','VBAT_LINK'],19,9),('J4',['+3V3','GND','UPDI'],55,46)]:
        for i,n in enumerate(pins,1):check(main,ref,i,n,x,y+(i-1)*2.54)
    for i,n in enumerate(['GND','+3V3','UPDI'],1):check(main,'J5',i,n,63+(i-1)*2,46)
    cable=['LCD_VCC','GND','LCD_CLK','LCD_DATA','LCD_CS','LCD_CD','LCD_RST','']
    for i,n in enumerate(cable,1):
        check(main,'J3',i,n,70,16+(i-1)*2.54);check(adapter,'J1',i,n,9+(i-1)*2.54,13)
    lcd={1:'LCD_CS',2:'LCD_RST',3:'LCD_CD',**{i:'GND' for i in range(4,12)},12:'LCD_CLK',13:'LCD_DATA',14:'LCD_VCC',15:'GND',16:'VB0_PLUS',17:'VB0_MINUS',18:'VB1_MINUS',19:'VB1_PLUS',20:'VLCD',21:'GND',22:'GND'}
    for i,n in lcd.items():check(adapter,'J2',i,n,21.665+(i-1)*1.27,3)
    check(adapter,'C5',1,'LCD_VCC',6.4375,7);check(adapter,'C5',2,'GND',9.5625,7)  # nonpolar MLCC

def run():
    boards={'main':k.LoadBoard(str(FOLDER/(STEM+'.kicad_pcb'))),
            'adapter':k.LoadBoard(str(ROOT/'pcb'/'r3'/'display_adapter'/'display_adapter.kicad_pcb'))}
    maps={n:actual(b) for n,b in boards.items()};contracts(maps['main'],maps['adapter'])
    # Compare ALL connected pins to native KiCad schematic XML, not just power.
    for name,folder,stem in [('main',FOLDER,STEM),('adapter',ROOT/'pcb'/'r3'/'display_adapter','display_adapter')]:
        schematic={}
        for n in E.parse(folder/(stem+'.net.xml')).findall('.//nets/net'):
            if n.get('name').startswith('unconnected-'):continue
            for node in n.findall('node'):
                if not node.get('ref').startswith('#'):schematic[node.get('ref'),node.get('pin')]=n.get('name')
        copper={key:net(p) for key,p in maps[name].items() if net(p)}
        assert schematic==copper,(name,'schematic/copper mismatch')
    main=boards['main'];f={f.GetReference():f for f in main.GetFootprints()}
    assert all(not p.IsFlipped() for p in f.values())
    for ref in ['U2','L1','D1','D2','C1','C2','C6','C7','R3','R4','R5','R6','R7','R8','R1','R2','C3','C4','C5','Q1']:
        assert all(p.GetAttribute()==k.PAD_ATTRIB_SMD for p in f[ref].Pads())
    for b in boards.values():
        for part in b.GetFootprints():
            if part.GetReference().startswith(('C','R','D','Q','L')) or part.GetReference()=='U2':
                assert all(p.GetAttribute()==k.PAD_ATTRIB_SMD for p in part.Pads()),part.GetReference()
    assert f['J5'].GetFPIDAsString().endswith('JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical')
    assert abs(maps['main']['J5','1'].GetDrillSize().x/1e6-.75)<1e-6
    assert maps['main']['J5','1'].GetShape()==k.PAD_SHAPE_ROUNDRECT
    assert abs(f['J5'].GetOrientationDegrees())<.001
    # All connector pad 1s are square, as are U1 socket pad1. U2 is leaded MSOP.
    for ref in ['U1','J1','J2','JP1','J3','J4']:
        assert maps['main'][ref,'1'].GetShape()==k.PAD_SHAPE_RECT
    for i,(x,y) in enumerate([(5,5),(77,5),(5,63),(77,63)],1):
        q=f['H'+str(i)].GetPosition();assert (round(q.x/1e6-50,3),round(q.y/1e6-50,3))==(x,y)
    body=[p for p in f['U2'].Pads()];assert len(body)==10
    for p in body:
        assert abs(p.GetSize().y/1e6-.35)<1e-6
        assert abs(p.GetSize().x/1e6-1.625)<1e-6
    assert f['Q1'].GetFPIDAsString().endswith('SOT-23_Handsoldering')
    for fp in boards['adapter'].GetFootprints():
        if fp.GetReference().startswith(('C','R')):
            assert all(p.GetAttribute()==k.PAD_ATTRIB_SMD for p in fp.Pads())
    assert f['U1'].GetFPIDAsString().endswith('DIP-28_W7.62mm')
    # Real bottom view reverses x around the board width; y remains upwards.
    with (REPORT/'orientation_pins.csv').open('w',newline='') as out:
        w=csv.writer(out,lineterminator="\n");w.writerow(['Board','Reference','Pin','Net','InstalledFrom','TopX_mm','TopY_mm','UndersideX_mm','UndersideY_mm'])
        for name,pmap in maps.items():
            width=82 if name=='main' else 70
            for (ref,num),p in sorted(pmap.items()):
                x,y=p.GetPosition().x/1e6-50,p.GetPosition().y/1e6-50
                w.writerow([name,ref,num,net(p),'F.Cu',round(x,4),round(y,4),round(width-x,4),round(y,4)])
    report={'revision':'R3','cad_pin_contract':'PASS','all_schematic_pins_match_pcb':'PASS',
            'mounting_holes_preserved':'PASS','MSOP_pitch_and_no_hidden_pad':'PASS','all_discrete_parts_SMD_both_boards':'PASS','owned_DIP_and_connector_contracts_preserved':'PASS','JST_PH_programming_pin_order_and_pitch':'PASS',
            'top_and_mirrored_bottom_coordinates':'PASS','physical_mating':'UNVERIFIED',
            'release':'HOLD','files_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                for p in [FOLDER/(STEM+'.kicad_pcb'),FOLDER/(STEM+'.kicad_sch'),ROOT/'pcb'/'r3'/'display_adapter'/'display_adapter.kicad_pcb']}}
    (REPORT/'pin_audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':run()
