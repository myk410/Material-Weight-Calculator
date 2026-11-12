"""Validate R3 and export review files; Gerbers require a separate physical gate.
Usage: /usr/bin/python3 hardware/source/export_r3.py [--manufacturing]
"""
from pathlib import Path
import subprocess, sys, json, hashlib, tempfile, shutil
ROOT=Path(__file__).resolve().parents[1];MAIN=ROOT/'pcb'/'r3'
REPORT=ROOT/'validation'/'r3';DOC=ROOT/'docs'/'r3'
REPORT.mkdir(exist_ok=True);DOC.mkdir(exist_ok=True)
def run(*args):subprocess.run(['kicad-cli',*map(str,args)],check=True)
def validate():
    for name,folder,stem in [('main',MAIN,'material_weight_calculator'),('adapter',ROOT/'pcb'/'display_adapter','display_adapter')]:
        sch=folder/(stem+'.kicad_sch');pcb=folder/(stem+'.kicad_pcb')
        run('sch','export','netlist','--format','kicadxml','-o',folder/(stem+'.net.xml'),sch)
        for fmt,ext in [('json','json'),('report','rpt')]:
            run('sch','erc','--exit-code-violations','--format',fmt,'-o',REPORT/(name+'_erc.'+ext),sch)
            run('pcb','drc','--schematic-parity','--exit-code-violations','--format',fmt,'-o',REPORT/(name+'_drc.'+ext),pcb)
        run('sch','export','pdf','-o',DOC/(name+'_schematic.pdf'),sch)
        for side,layers,extra in [('top','F.Cu,F.Silkscreen,Edge.Cuts',[]),('bottom','B.Cu,B.Silkscreen,Edge.Cuts',['--mirror'])]:
            run('pcb','export','svg','--layers',layers,*extra,'--page-size-mode','2','--exclude-drawing-sheet','--mode-single','-o',DOC/(name+'_'+side+'.svg'),pcb)
    for p in DOC.glob('*.svg'):
        p.write_text('\n'.join(line.rstrip() for line in p.read_text().splitlines())+'\n')
    subprocess.run([sys.executable,str(ROOT/'source'/'verify_r3.py')],check=True)
def physical_gate():
    gate=json.loads((MAIN/'release_gate.json').read_text());failed=[]
    for name,entry in gate['physical_checks'].items():
        if not entry['passed'] or not entry['evidence']:failed.append(name);continue
        for item in entry['evidence']:
            p=(ROOT/item['path']).resolve()
            if not p.is_relative_to(ROOT) or not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:failed.append(name)
    if gate['status']!='APPROVED_FOR_PROTOTYPE_FABRICATION':failed.append('status')
    if failed:raise SystemExit('FABRICATION HOLD: '+', '.join(failed))
def manufacturing():
    # Gate runs before creating any manufacturing directory or files.
    physical_gate()
    validate()
    with tempfile.TemporaryDirectory() as tmp:
        for name,folder,stem in [('main',MAIN,'material_weight_calculator'),('adapter',ROOT/'pcb'/'display_adapter','display_adapter')]:
            out=Path(tmp)/name;out.mkdir()
            run('pcb','export','gerbers','-l','F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,Edge.Cuts','-o',str(out)+'/',folder/(stem+'.kicad_pcb'))
            run('pcb','export','drill','--format','excellon','--excellon-separate-th','-o',str(out)+'/',folder/(stem+'.kicad_pcb'))
        target=MAIN/'manufacturing'
        if target.exists():raise SystemExit('Existing manufacturing output: archive/review it before replacing.')
        shutil.copytree(tmp,target)
if __name__=='__main__':
    if '--manufacturing' in sys.argv:manufacturing()
    else:validate()
