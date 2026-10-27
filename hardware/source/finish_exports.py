"""Label native KiCad copper PDFs, verify nets, package current R2 deliverables."""
from pathlib import Path
import io,json,hashlib,zipfile,xml.etree.ElementTree as E
from pypdf import PdfReader,PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
ROOT=Path(__file__).resolve().parents[1]
for adapter in [False,True]:
 writer=PdfWriter();dims='70 x 18' if adapter else '82 x 68'
 for suffix,title in [('top_reference','Top copper - component-side reference'),('top_transfer','Top copper - MIRRORED toner-transfer mask'),('bottom_reference','Bottom copper - viewed from underside'),('bottom_transfer','Bottom copper - toner-transfer mask')]:
  p=next((ROOT/'validation'/('adapter_plot_intermediates' if adapter else 'plot_intermediates')).glob('*'+suffix+'.pdf'))
  page=PdfReader(p).pages[0];w,h=map(float,[page.mediabox.width,page.mediabox.height]);buf=io.BytesIO();c=canvas.Canvas(buf,pagesize=(w,h))
  c.setFont('Helvetica-Bold',13);c.drawString(18*mm,h-18*mm,('Display adapter: ' if adapter else '')+title)
  c.setFont('Helvetica',9);c.drawString(18*mm,h-25*mm,'Material Weight Calculator R2 - '+dims+' mm board - print 100%, no fit-to-page')
  c.drawString(18*mm,25*mm,'Black is retained copper. Use Gerbers for factory fabrication. Two layers require registration.')
  c.setLineWidth(.25*mm);c.line(20*mm,15*mm,120*mm,15*mm);c.setFont('Helvetica',8);c.drawString(20*mm,19*mm,'100 mm scale check')
  c.save();buf.seek(0);page.merge_page(PdfReader(buf).pages[0]);writer.add_page(page)
 with (ROOT/'docs'/('display_adapter_copper_1to1.pdf' if adapter else 'copper_artwork_1to1.pdf')).open('wb') as f:writer.write(f)
 elec=json.loads((ROOT/'source'/('adapter_electrical_design.json' if adapter else 'electrical_design.json')).read_text());actual={}
 folder=ROOT/'pcb'/'display_adapter' if adapter else ROOT/'pcb';stem='display_adapter' if adapter else 'material_weight_calculator'
 for net in E.parse(folder/(stem+'.net.xml')).findall('.//nets/net'):
  if net.get('name').startswith('unconnected-'):continue
  for node in net.findall('node'):actual[(node.get('ref'),node.get('pin'))]=net.get('name').lstrip('/')
 expected={(c['ref'],p):n for c in elec['components'] for p,n in c['pins'].items() if n}
 assert actual==expected,{'expected':expected,'actual':actual}
 (ROOT/'validation'/('adapter_net_check.json' if adapter else 'schematic_net_check.json')).write_text(json.dumps({'matched_connected_pins':len(actual),'result':'PASS'},indent=2))
 (folder/'gerbers'/'FABRICATION.txt').write_text('Material Weight Calculator R2 PROTOTYPE\n'+dims+' mm; 2 copper layers; 1.6 mm FR-4; plated through holes.\nSeparate PTH/NPTH Excellon drills. 0.4 mm tracks; 0.25 mm clearance; 1.0/0.5 mm vias.\nNo electrical prototype has been bench tested.\n')
for name,count in [('schematic.pdf',1),('display_adapter_schematic.pdf',1),('copper_artwork_1to1.pdf',4),('display_adapter_copper_1to1.pdf',4),('drill_template.pdf',1),('display_adapter_drill.pdf',1),('keypad_fit_template.pdf',1),('display_fit_template.pdf',1)]:assert len(PdfReader(ROOT/'docs'/name).pages)==count
for f in ['pcb_fabrication_r1.zip','material_weight_calculator_hardware_r1.zip']:(ROOT/'downloads'/f).unlink(missing_ok=True)
(ROOT/'downloads').mkdir(exist_ok=True)
with zipfile.ZipFile(ROOT/'downloads'/'pcb_fabrication_r2.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for path,prefix in [(ROOT/'pcb'/'gerbers','main_board'),(ROOT/'pcb'/'display_adapter'/'gerbers','display_adapter')]:
  for p in sorted(path.glob('*')):z.write(p,prefix+'/'+p.name)
files=[p for p in ROOT.rglob('*') if p.is_file() and not any(s in p.parts for s in ['__pycache__','downloads','plot_intermediates','adapter_plot_intermediates','pcb-preview']) and p.name not in ['kicad_drc_initial.rpt','adapter_drc_initial.rpt','manifest.sha256'] and p.suffix not in ['.lck','.kicad_prl']]
manifest=''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT)}\n' for p in sorted(files));(ROOT/'manifest.sha256').write_text(manifest)
with zipfile.ZipFile(ROOT/'downloads'/'material_weight_calculator_hardware_r2.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files+[ROOT/'manifest.sha256',ROOT/'downloads'/'pcb_fabrication_r2.zip']:z.write(p,'hardware/'+str(p.relative_to(ROOT)))
print('Packaged',len(files),'files; full ZIP bytes:',(ROOT/'downloads'/'material_weight_calculator_hardware_r2.zip').stat().st_size)
