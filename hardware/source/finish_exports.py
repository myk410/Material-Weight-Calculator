from pathlib import Path
import io,json,hashlib,zipfile,xml.etree.ElementTree as E
from pypdf import PdfReader,PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
ROOT=Path(__file__).resolve().parents[1]
writer=PdfWriter()
for suffix,title in [('top_reference','Top copper - component-side reference'),('top_transfer','Top copper - MIRRORED toner-transfer mask'),('bottom_reference','Bottom copper - viewed from underside'),('bottom_transfer','Bottom copper - toner-transfer mask')]:
 p=next((ROOT/'validation'/'plot_intermediates').glob('*'+suffix+'.pdf'))
 page=PdfReader(p).pages[0];w,h=map(float,[page.mediabox.width,page.mediabox.height]);buf=io.BytesIO();c=canvas.Canvas(buf,pagesize=(w,h))
 c.setFont('Helvetica-Bold',13);c.drawString(18*mm,h-18*mm,title)
 c.setFont('Helvetica',9);c.drawString(18*mm,h-25*mm,'Material Weight Calculator R1 - 82 x 68 mm board - print 100%, no fit-to-page')
 c.drawString(18*mm,25*mm,'Black is retained copper. Use Gerbers for factory fabrication. Two layers require registration.')
 c.setLineWidth(.25*mm);c.line(20*mm,15*mm,120*mm,15*mm);c.setFont('Helvetica',8);c.drawString(20*mm,19*mm,'100 mm scale check')
 c.save();buf.seek(0);page.merge_page(PdfReader(buf).pages[0]);writer.add_page(page)
with (ROOT/'docs'/'copper_artwork_1to1.pdf').open('wb') as f:writer.write(f)
# Compare actual exported netlist with the source pin map, not just segment count.
elec=json.loads((ROOT/'source'/'electrical_design.json').read_text());actual={}
for net in E.parse(ROOT/'pcb'/'material_weight_calculator.net.xml').findall('.//nets/net'):
 if net.get('name').startswith('unconnected-'):continue
 for node in net.findall('node'):actual[(node.get('ref'),node.get('pin'))]=net.get('name').lstrip('/')
expected={(c['ref'],p):n for c in elec['components'] for p,n in c['pins'].items() if n}
assert actual==expected
(ROOT/'validation'/'schematic_net_check.json').write_text(json.dumps({'matched_connected_pins':len(actual),'result':'PASS'},indent=2))
for name,count in [('schematic.pdf',1),('copper_artwork_1to1.pdf',4),('drill_template.pdf',1),('keypad_fit_template.pdf',1)]:assert len(PdfReader(ROOT/'docs'/name).pages)==count
(ROOT/'pcb'/'gerbers'/'FABRICATION.txt').write_text('Material Weight Calculator R1 PROTOTYPE\n82 x 68 mm; 2 copper layers; 1.6 mm FR-4; plated through holes.\nSeparate PTH and NPTH Excellon drills included.\n0.4 mm tracks; 0.25 mm design clearance; 1.0/0.5 mm vias.\nNo electrical prototype has been bench tested.\n')
# Drop only known generated stale files; keep all user source intact.
for relative in ['pcb/gerbers/material_weight_calculator.drl','pcb/mw-footprints.pretty/MountingHole_2.5mm.kicad_mod']:(ROOT/relative).unlink(missing_ok=True)
( ROOT/'downloads').mkdir(exist_ok=True)
with zipfile.ZipFile(ROOT/'downloads'/'pcb_fabrication_r1.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted((ROOT/'pcb'/'gerbers').glob('*')):z.write(p,p.name)
files=[p for p in ROOT.rglob('*') if p.is_file() and not any(s in p.parts for s in ['__pycache__','downloads','plot_intermediates','pcb-preview']) and p.name not in ['kicad_drc_initial.rpt','manifest.sha256'] and p.suffix not in ['.lck','.kicad_prl']]
manifest=''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT)}\n' for p in sorted(files))
(ROOT/'manifest.sha256').write_text(manifest)
with zipfile.ZipFile(ROOT/'downloads'/'material_weight_calculator_hardware_r1.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files+[ROOT/'manifest.sha256',ROOT/'downloads'/'pcb_fabrication_r1.zip']:z.write(p,'hardware/'+str(p.relative_to(ROOT)))
print('Packaged',len(files),'files; full ZIP bytes:',(ROOT/'downloads'/'material_weight_calculator_hardware_r1.zip').stat().st_size)
