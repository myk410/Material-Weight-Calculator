"""Export R2.1 boards and require native ERC, DRC and schematic parity (KiCad 9)."""
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
 prefix='kicad' if stem=='material_weight_calculator' else 'adapter'
 for fmt,ext in [('report','rpt'),('json','json')]:
  run('sch','erc','--exit-code-violations','--format',fmt,'-o',ROOT/'validation'/(prefix+'_erc.'+ext),folder/(stem+'.kicad_sch'))
  run('pcb','drc','--schematic-parity','--exit-code-violations','--format',fmt,'-o',ROOT/'validation'/(prefix+'_drc.'+ext),folder/(stem+'.kicad_pcb'))
 print('ERC / DRC / PARITY PASS',stem,flush=True)
