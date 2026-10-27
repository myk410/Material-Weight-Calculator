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
c.rect(33.5,184-47.5,29,27)
for row,y in enumerate([77,95,113,131]):
 for col,x in enumerate([21,39,57,75]):
  yy=184-y;c.roundRect(x-7,yy-7,14,14,2);c.line(x-2,yy,x+2,yy);c.line(x,yy-2,x,yy+2)
  c.setFont('Helvetica',2.2);c.drawCentredString(x,yy+4.3,f'R{row+1} C{col+1}')
c.setFont('Helvetica',2.8);c.drawCentredString(48,149,'DISPLAY WINDOW')
c.restoreState();scale(c,y=32)
c.setFont('Helvetica',9);c.drawString(20*mm,22*mm,'Dashed pad boundary is a nominal 69 x 77 mm reference, not a verified DIYmalls drawing.')
c.showPage();c.save()
print('Generated drill and fit templates')
