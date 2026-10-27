"""Pin audit against the EastRising module table and SPI application circuit."""
from pathlib import Path
import json,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1]
main=json.loads((ROOT/'source'/'electrical_design.json').read_text())
adapter=json.loads((ROOT/'source'/'adapter_electrical_design.json').read_text())
M={x['ref']:x for x in main['components']};A={x['ref']:x for x in adapter['components']}
assert M['J3']['pins']==A['J1']['pins']
assert M['U1']['pins']['26']=='LCD_CD' and M['U1']['pins']['27']=='LCD_RST'
expected={'1':'LCD_CS','2':'LCD_RST','3':'LCD_CD','4':'GND','5':'GND',**{str(x):'GND' for x in range(6,12)},'12':'LCD_CLK','13':'LCD_DATA','14':'LCD_VCC','15':'GND','16':'VB0_PLUS','17':'VB0_MINUS','18':'VB1_MINUS','19':'VB1_PLUS','20':'VLCD','21':'GND','22':'GND'}
assert A['J2']['pins']==expected
for ref,pair in [('C1',{'VB0_PLUS','VB0_MINUS'}),('C2',{'VB1_PLUS','VB1_MINUS'}),('C3',{'VLCD','GND'}),('R1',{'VLCD','GND'})]:assert set(A[ref]['pins'].values())==pair
assert A['C5']['pins']=={'1':'LCD_VCC','2':'GND'}
assert A['C1']['value']==A['C2']['value']=='2.2uF 25V X7R'
assert A['C3']['value']=='330nF 25V' and A['R1']['value']=='10M'
pads={p['pin']:p for p in adapter['pads'] if p['ref']=='J2'}
assert len(pads)==22 and abs(pads['22']['x']-pads['1']['x']-26.67)<1e-6
for i in range(1,22):assert abs(pads[str(i+1)]['x']-pads[str(i)]['x']-1.27)<1e-6
actual={}
for net in E.parse(ROOT/'pcb'/'display_adapter'/'display_adapter.net.xml').findall('.//nets/net'):
 if net.get('name').startswith('unconnected-'):continue
 for node in net.findall('node'):actual[(node.get('ref'),node.get('pin'))]=net.get('name').lstrip('/')
expected={(c['ref'],p):n for c in adapter['components'] for p,n in c['pins'].items() if n}
assert expected==actual
result={'display':'ERC12864FS-655','result':'PASS','matched_adapter_connected_pins':len(actual),'signal_pins':22,'pitch_mm':1.27,'cable_connected_wires':7,'backlight':'not connected','sources':['EastRising ERC12864-655 Series Rev1.0, pp7-9','EastRising SPI reference schematic dated 2020-04-21']}
(ROOT/'validation'/'display_pin_audit.json').write_text(json.dumps(result,indent=2));print(result)
