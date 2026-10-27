"""Generate actual-scale vector PCB artwork and resin keypad fit templates."""
from pathlib import Path
import json,math
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import letter
ROOT=Path(__file__).resolve().parents[1]; D=json.loads((ROOT/'source'/'electrical_design.json').read_text());OUT=ROOT/'docs'
PW,PH=letter

def heading(c,title,subtitle):
 c.setFont('Helvetica-Bold',15);c.drawString(18*mm,PH-20*mm,title)
 c.setFont('Helvetica',9);c.drawString(18*mm,PH-27*mm,subtitle)
def scale(c,y=30):
 c.setStrokeColorRGB(0,0,0);c.setLineWidth(.25*mm);c.line(20*mm,y*mm,120*mm,y*mm)
 for x in [20,120]:c.line(x*mm,(y-2)*mm,x*mm,(y+2)*mm)
 c.setFont('Helvetica',9);c.drawString(20*mm,(y+4)*mm,'100 mm scale check - print at Actual Size / 100%')
def coords(x,y,mirror=False):return ((82-x) if mirror else x),68-y

c=canvas.Canvas(str(OUT/'drill_template.pdf'),pagesize=letter)
heading(c,'PCB drill and outline template','82 x 68 mm board. View from component side. Not a copper mask.')
c.saveState();c.translate(30*mm,125*mm);c.scale(mm,mm);c.setLineWidth(.15);c.rect(0,0,82,68)
for p in D['pads']:
 x,y=coords(p['x'],p['y']);d=p['drill']
 c.circle(x,y,d/2,stroke=1,fill=0);c.line(x-1,y,x+1,y);c.line(x,y-1,x,y+1)
for v in D['vias']:
 x,y=coords(v['x'],v['y']);c.circle(x,y,.25,stroke=1,fill=0)
c.restoreState();scale(c)
c.setFont('Helvetica',10);c.drawString(20*mm,105*mm,'Use the Excellon drill files for final tool diameters and coordinates.')
c.drawString(20*mm,98*mm,'Home-etched boards need conductive connections through all layer changes.')
c.showPage();c.save()
c=canvas.Canvas(str(OUT/'keypad_fit_template.pdf'),pagesize=letter)
heading(c,'Keypad alignment check - actual scale','Nominal key pitch: 18 mm. Fit the existing membrane before a full resin print.')
c.saveState();c.translate(25*mm,58*mm);c.scale(mm,mm)
c.setLineWidth(.25);c.rect(0,0,96,184);c.setDash(2,1);c.rect(13.5,184-142,69,77);c.setDash()
c.rect(14.5,184-48,67,37)
for row,y in enumerate([77,95,113,131]):
 for col,x in enumerate([21,39,57,75]):
  yy=184-y;c.roundRect(x-7,yy-7,14,14,2);c.line(x-2,yy,x+2,yy);c.line(x,yy-2,x,yy+2)
  c.setFont('Helvetica',2.2);c.drawCentredString(x,yy+4.3,f'R{row+1} C{col+1}')
c.setFont('Helvetica',2.8);c.drawCentredString(48,148,'DISPLAY WINDOW')
c.restoreState();scale(c,y=32)
c.setFont('Helvetica',9);c.drawString(20*mm,22*mm,'Dashed pad boundary is a nominal 69 x 77 mm reference, not a verified DIYmalls drawing.')
c.showPage();c.save()
print('Generated drill and fit templates')

# Additional adapter drill template and full-size display alignment drawing.
A=json.loads((ROOT/'source'/'adapter_electrical_design.json').read_text())
c=canvas.Canvas(str(OUT/'display_adapter_drill.pdf'),pagesize=letter)
heading(c,'Display adapter drill template','70 x 18 mm. Component side. Pin 1 is the square pad; 22 pins at 1.27 mm pitch.')
c.saveState();c.translate(30*mm,160*mm);c.scale(mm,mm);c.setLineWidth(.15);c.rect(0,0,70,18)
for p in A['pads']:
 x,y=p['x'],18-p['y'];c.circle(x,y,p['drill']/2);c.line(x-.6,y,x+.6,y);c.line(x,y-.6,x,y+.6)
for v in A['vias']:c.circle(v['x'],18-v['y'],.25)
c.restoreState();scale(c);c.showPage();c.save()
c=canvas.Canvas(str(OUT/'display_fit_template.pdf'),pagesize=letter)
heading(c,'ERC12864FS-655 display fit check','Front view, actual size. Confirm module orientation and solder-pin reach before assembly.')
c.saveState();c.translate(35*mm,140*mm);c.scale(mm,mm);c.setLineWidth(.2)
c.rect(0,0,70,50);c.rect(1.5,50-3.5-37,67,37)
# Pin row at top: 1.2 mm from upper edge, on 1.27 mm centers.
for i in range(22):c.circle(21.665+i*1.27,48.8,.25)
for x in [4.275,65.725]:
 for y in [1.2,48.8]:c.circle(x,y,.5)
c.setFont('Helvetica',2.5);c.drawString(19,53,'1');c.drawString(48,53,'22')
c.drawCentredString(35,25,'67 x 37 mm viewing area')
c.restoreState();scale(c)
c.setFont('Helvetica',10);c.drawString(20*mm,115*mm,'Body: 70 x 50 x 5.8 mm maximum. Pin 1 to pin 22: 26.67 mm.')
c.drawString(20*mm,108*mm,'Use manufacturer drawing for pin bends and separate A/K backlight terminals.')
c.drawString(20*mm,101*mm,'Case body origin: X13, Y7.5 mm. Window origin: X14.5, Y11 mm.')
c.showPage();c.save()
