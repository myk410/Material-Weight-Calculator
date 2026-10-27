"""Export both R2 boards using KiCad 7. Run with pcbnew Python bindings."""
from pathlib import Path
import subprocess,os,json
import pcbnew as k
ROOT=Path(__file__).resolve().parents[1]
CLI=os.environ.get('KICAD_CLI','kicad-cli')
for folder,stem in [(ROOT/'pcb','material_weight_calculator'),(ROOT/'pcb'/'display_adapter','display_adapter')]:
 def run(*args):subprocess.run([CLI,*map(str,args)],check=True)
 run('sch','export','netlist','--format','kicadxml','-o',folder/(stem+'.net.xml'),folder/(stem+'.kicad_sch'))
 run('sch','export','pdf','-o',ROOT/'docs'/('schematic.pdf' if stem=='material_weight_calculator' else 'display_adapter_schematic.pdf'),folder/(stem+'.kicad_sch'))
 g=folder/'gerbers';g.mkdir(exist_ok=True)
 for stale in [g/(stem+'.drl'),g/(stem+'-drl_map.svg')]:stale.unlink(missing_ok=True)
 run('pcb','export','gerbers','-l','F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,Edge.Cuts','-o',str(g)+'/',folder/(stem+'.kicad_pcb'))
 run('pcb','export','drill','--format','excellon','--excellon-separate-th','--generate-map','--map-format','svg','-o',str(g)+'/',folder/(stem+'.kicad_pcb'))
 board=k.LoadBoard(str(folder/(stem+'.kicad_pcb')))
 report=ROOT/'validation'/('kicad_drc.rpt' if stem=='material_weight_calculator' else 'adapter_drc.rpt')
 board.BuildConnectivity();k.WriteDRCReport(board,str(report),k.EDA_UNITS_MILLIMETRES,True)
 txt=report.read_text()
 assert all(x in txt for x in ['Found 0 DRC violations','Found 0 unconnected pads','Found 0 Footprint errors']),txt
 print('DRC PASS',stem,flush=True)
