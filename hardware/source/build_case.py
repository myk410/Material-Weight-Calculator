"""Parametric CadQuery enclosure. Units mm. Plan coordinates: x right, y down.
Assembly Z is measured from back face toward the user's fingers.
Each STL is translated to its own positive bounding box; STEP retains assembly positions.
"""
from pathlib import Path
import json, math
import cadquery as cq
ROOT=Path(__file__).resolve().parents[1]
W,H=96.0,184.0
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
KEY_X=[21,39,57,75]; KEY_Y=[77,95,113,131]
LABELS=[['7','8 ↑','9','MENU'],['4','5','6','BACK'],['1','2 ↓','3','CLEAR'],['ON OFF','0','.','ENTER =']]
parts={}; checks=[]
def block(x,y,z,w,h,d,r=0):
 s=cq.Workplane('XY').box(w,h,d).translate((x+w/2,H-y-h/2,z+d/2))
 if r:s=s.edges('|Z').fillet(r)
 return s
def cyl(x,y,z,r,d):return cq.Workplane('XY').circle(r).extrude(d).translate((x,H-y,z))
def hole(s,x,y,z,d=2.9,h=40):return s.cut(cyl(x,y,z,d/2,h))
def nut(s,x,y,z,af=5.35,h=2.45):
 n=cq.Workplane('XY').polygon(6,af/math.cos(math.pi/6)).extrude(h).translate((x,H-y,z))
 return s.cut(n)
def boss(s,x,y,z,h,r=4):return s.union(cyl(x,y,z,r,h))
def slot(s,x,y,z,l=4.5,d=2.9,h=5):
 return s.cut(cq.Workplane('XY').slot2D(l,d).extrude(h).translate((x,H-y,z)))
def engrave(s,text,x,y,z,size=3,depth=.4):
 cutter=cq.Workplane('XY').text(text,size,depth+.1,fontPath=FONT,combine=False).translate((x,H-y,z-depth))
 return s.cut(cutter)
# Front shell: 2.6 mm skin with webs between keys.
f=block(0,0,12,W,H,19,6).cut(block(2.6,2.6,11.9,W-5.2,H-5.2,16.5,4))
caseholes=[(6,6),(90,6),(6,178),(90,178)]
for x,y in caseholes:
 f=boss(f,x,y,12,17)
 f=hole(f,x,y,11.8,h=18)
 f=nut(f,x,y,12,h=2.5)
f=f.cut(block(14.5,11,27.8,67,37,4))
for y in KEY_Y:
 for x in KEY_X:f=f.cut(block(x-7.35,y-7.35,28,14.7,14.7,4,2))
for x in [30,48,66]:f=f.union(block(x-.4,66,26.9,.8,76,1.5))
for y in [86,104,122]:f=f.union(block(13,y-.4,26.9,70,.8,1.5))
# Guide/backing mount positions outside the active key field.
keymounts=[(9,64),(87,64),(9,146),(87,146)]
for x,y in keymounts:
 f=boss(f,x,y,26.6,1.8,4.1)
 f=hole(f,x,y,26.5,h=3.8)
 f=nut(f,x,y,26.6,h=2.4)
dispmounts=[(7,15),(89,15),(7,53),(89,53)]
for x,y in dispmounts:
 f=boss(f,x,y,23.5,4.9,4.1)
 f=hole(f,x,y,23.4,h=5.8)
 f=nut(f,x,y,23.5,h=2.4)
f=engrave(f,'MATERIAL WEIGHT',48,7,31,2.5)
parts['front_shell']=f
# Rear tray, PCB mounts and a recessed removable battery door.
b=block(0,0,0,W,H,12,6).cut(block(2.6,2.6,2.6,W-5.2,H-5.2,10,4))
for x,y in caseholes:
 b=boss(b,x,y,2.6,9.4)
 b=hole(b,x,y,-.1,h=13)
 b=b.cut(cyl(x,y,-.1,2.6,2.1))
# PCB local 82 x 68 mm, top-left plan origin 7,62.
pcbholes=[(12,67),(84,67),(12,125),(84,125)]
for x,y in pcbholes:
 b=boss(b,x,y,2.6,4.4)
 b=hole(b,x,y,2.5,h=8)
 b=nut(b,x,y,4.55,h=2.45)
for x in [19,77]:b=b.union(block(x,10,2.5,1.2,122,1.8))
for y in [30,58,100]:b=b.union(block(10,y,2.5,76,1.2,1.8))
# Battery holder: Pololu 1144 envelope 52 x 37 x 13; cavity 54 x 39.
for x in [20,74.8]:b=b.union(block(x,139,2.5,1.2,39,11))
b=b.union(block(20,138,2.5,56,1.2,11)).union(block(20,178,2.5,56,1.2,11))
b=b.cut(block(13,137,-.1,70,45,2.15,2)).cut(block(19,140,-.1,58,39,3))
for x in [15.5,80.5]:
 b=boss(b,x,159.5,2,5.8,3.4)
 b=hole(b,x,159.5,-.1,h=9)
 b=nut(b,x,159.5,5.3,h=2.5)
parts['rear_shell']=b
cover=block(13.3,137.3,0,69.4,44.4,1.9,1.8)
for x in [15.5,80.5]:cover=hole(cover,x,159.5,-.1,h=3)
cover=engrave(cover,'3 x AAA',48,160,1.9,3,.4)
parts['battery_cover']=cover
# Flat backing; clamp slots permit membrane translation. Do not drill membrane.
backing=block(5.5,60.5,22.5,85,89,2,2)
for x,y in keymounts:backing=slot(backing,x,y,22.3,h=3)
# Ribbon exits toward footer; recess avoids pinching the flex tail.
backing=backing.cut(block(36,139,23.7,24,10.5,1))
parts['keypad_backing']=backing
# Guide registers the electrical membrane and acts as a travel stop below the flexible keypad sheet.
guide=block(5.5,60.5,26,85,89,.6,2)
for y in KEY_Y:
 for x in KEY_X:guide=guide.cut(block(x-5.6,y-5.6,25.9,11.2,11.2,1,.8))
for x,y in keymounts:
 guide=guide.union(cyl(x,y,24.5,3.2,1.7))
 guide=slot(guide,x,y,24.3,h=3)
parts['keypad_guide']=guide
# The guide must be independently removable; secure above backing with separate screws.
# Four rear-facing nut seats in the shell are common to the stack; use 6 mm screws.
# R2: 70 x 50 x 5.8 mm ERC12864FS-655. Body plan origin (13,7.5).
# The glass front is at Z27.9. 0.5 mm closed-cell foam isolates both faces.
# Support only the opaque perimeter/backlight frame; no rigid preload on glass.
cradle=block(3,4,19.6,90,56,2,2).cut(block(15,10,19.5,66,43,2.3))
# Top opening clears the 22-pin solder tail and 70 x 18 mm adapter behind it.
cradle=cradle.cut(block(17,3.9,19.5,62,20.1,2.3))
for x,y in dispmounts:cradle=slot(cradle,x,y,19.5,h=3)
for x in [11.8,83.2]:cradle=cradle.union(block(x,8,21.5,1,49,2.5))
for x,y in caseholes[:2]:cradle=cradle.cut(cyl(x,y,19.5,4.4,8))
for x in [2.4,91.5]:cradle=cradle.cut(block(x,56.05,19.5,2.1,4.1,2.3))
for x in [17.275,78.725]:cradle=cradle.cut(cyl(x,56.3,19.5,1.5,3))
parts['display_cradle']=cradle
# One-piece 55A flexible keypad. All 16 buttons are part of one continuous thin sheet.
# The sheet remains continuous to act as a dust barrier; tune membrane thickness after a real print test.
SHEET_X,SHEET_Y,SHEET_W,SHEET_H=12.0,68.0,72.0,72.0
SHEET_Z,SHEET_T=27.15,.85
BUTTON_W,BUTTON_H,BUTTON_RISE=14.0,14.0,5.0
ACTUATOR_D,ACTUATOR_H=8.0,1.55
keypad=block(SHEET_X,SHEET_Y,SHEET_Z,SHEET_W,SHEET_H,SHEET_T,2.5)
for row,y in enumerate(KEY_Y):
 for col,x in enumerate(KEY_X):
  text=LABELS[row][col]
  # Thick button island above the thin flexible web.
  keypad=keypad.union(block(x-BUTTON_W/2,y-BUTTON_H/2,SHEET_Z+SHEET_T,BUTTON_W,BUTTON_H,BUTTON_RISE,2))
  # Smooth centered actuator below the sheet presses the existing DIYmalls electrical membrane.
  keypad=keypad.union(cyl(x,y,SHEET_Z-ACTUATOR_H,ACTUATOR_D/2,ACTUATOR_H+.05))
  legend_z=SHEET_Z+SHEET_T+BUTTON_RISE
  if text in ['8 ↑','2 ↓']:
   keypad=engrave(keypad,text[0],x,y-2,legend_z,4.8)
   keypad=engrave(keypad,text[-1],x,y+3.7,legend_z,3)
  elif text=='ON OFF':
   keypad=engrave(keypad,'ON',x,y-2,legend_z,2.8);keypad=engrave(keypad,'OFF',x,y+2,legend_z,2.8)
  elif text=='ENTER =':
   keypad=engrave(keypad,'ENTER',x,y-2,legend_z,2.5);keypad=engrave(keypad,'=',x,y+2.5,legend_z,3.5)
  else:keypad=engrave(keypad,text,x,y,legend_z,5 if len(text)==1 else 2.8)
parts['keypad_sheet_55A']=keypad
# Two-key connected-sheet coupon reproduces the real membrane, cap rise and actuator geometry.
coupon_sheet=block(12,68,SHEET_Z,36,18,SHEET_T,2)
for col,x in enumerate(KEY_X[:2]):
 text=LABELS[0][col]
 coupon_sheet=coupon_sheet.union(block(x-BUTTON_W/2,77-BUTTON_H/2,SHEET_Z+SHEET_T,BUTTON_W,BUTTON_H,BUTTON_RISE,2))
 coupon_sheet=coupon_sheet.union(cyl(x,77,SHEET_Z-ACTUATOR_H,ACTUATOR_D/2,ACTUATOR_H+.05))
 legend_z=SHEET_Z+SHEET_T+BUTTON_RISE
 if text=='8 ↑':
  coupon_sheet=engrave(coupon_sheet,'8',x,75,legend_z,4.8)
  coupon_sheet=engrave(coupon_sheet,'↑',x,80.7,legend_z,3)
 else:
  coupon_sheet=engrave(coupon_sheet,text,x,77,legend_z,5)
parts['fit_coupon_keypad_55A']=coupon_sheet
coupon_face=block(7,60,28.4,46,34,2.6,2)
for x in KEY_X[:2]:coupon_face=coupon_face.cut(block(x-7.35,77-7.35,28.3,14.7,14.7,3,2))
parts['fit_coupon_face']=coupon_face
parts['fit_coupon_guide']=block(7,60,26,46,34,.6,2)
for x in KEY_X[:2]:parts['fit_coupon_guide']=parts['fit_coupon_guide'].cut(block(x-5.6,77-5.6,25.9,11.2,11.2,1,.8))
# Mars 5 Ultra: long shells split at y=60.25 with bonded locating tongues.
# The upper/lower seam is bonded; front and rear still separate on M2.5 screws.
seam=60.25
for original,tag,z0,z1 in [('front_shell','front',12,31),('rear_shell','rear',0,12)]:
 full=parts[original]
 upper=full.intersect(block(-1,-1,-1,W+2,seam+1,40))
 lower=full.intersect(block(-1,seam,-1,W+2,H-seam+1,40))
 for x in [2.5,91.7]:
  tz,th=(14,12) if tag=='front' else (4,6)
  tongue=block(x,seam-4,tz,1.8,10,th)
  upper=upper.union(tongue)
  lower=lower.cut(block(x-.2,seam-.2,tz-.2,2.2,6.4,th+.4))
 if tag=='rear':
  upper=upper.union(block(4,seam-3,.8,88,6,1))
  lower=lower.cut(block(3.8,seam-.2,.6,88.4,3.4,1.4))
 parts['mars_'+tag+'_upper']=upper
 parts['mars_'+tag+'_lower']=lower
# M2.5 nut-fit coupon: pockets open underneath, labels recessed on top.
nutcoupon=block(0,0,0,48,18,5,1)
for x,af in [(8,5.2),(24,5.35),(40,5.5)]:
 nutcoupon=nut(nutcoupon,x,8,0,af=af,h=2.45)
 nutcoupon=hole(nutcoupon,x,8,-.1,h=6)
 nutcoupon=engrave(nutcoupon,str(af),x,14,5,2.4)
parts['fit_coupon_nuts']=nutcoupon
# Export.
(ROOT/'stl').mkdir(exist_ok=True);(ROOT/'cad').mkdir(exist_ok=True);(ROOT/'validation').mkdir(exist_ok=True)
assembly=cq.Assembly(name='material_weight_calculator_r2')
for name,part in parts.items():
 shape=part.val(); bb=shape.BoundingBox()
 valid=shape.isValid();n=len(shape.Solids())
 checks.append({'part':name,'valid':valid,'solid_count':n,'volume_mm3':shape.Volume(),'assembly_bbox':[bb.xmin,bb.ymin,bb.zmin,bb.xmax,bb.ymax,bb.zmax]})
 if not valid or n!=1:raise RuntimeError(f'{name}: invalid or disconnected ({n} solids)')
 printable=part.translate((-bb.xmin,-bb.ymin,-bb.zmin))
 target=(ROOT/'cad'/f'{name}_whole_reference.stl') if name in ['front_shell','rear_shell'] else (ROOT/'stl'/f'{name}.stl')
 cq.exporters.export(printable,str(target),tolerance=.035,angularTolerance=.12)
 if name in ['front_shell','rear_shell']:(ROOT/'stl'/f'{name}.stl').unlink(missing_ok=True)
 if name.startswith('mars_') or name in ['keypad_backing','keypad_guide']:
  oriented=printable.rotate((0,0,0),(0,1,0),65).rotate((0,0,0),(0,0,1),90)
  ob=oriented.val().BoundingBox();oriented=oriented.translate((-ob.xmin,-ob.ymin,-ob.zmin))
  od=ROOT/'stl'/'mars5_ultra_oriented';od.mkdir(exist_ok=True)
  cq.exporters.export(oriented,str(od/f'{name}.stl'),tolerance=.035,angularTolerance=.12)
 if name not in ['front_shell','rear_shell'] and not name.startswith('fit_coupon'):
  assembly.add(part,name=name,color=cq.Color(.28,.3,.32) if name=='keypad_sheet_55A' else cq.Color(.65,.67,.69))
 print(name,round(shape.Volume(),1),flush=True)
# Reference electronic envelopes are included in STEP, never in the printable STLs.
lcd_reference=block(13,7.5,22.1,70,50,5.8)
adapter_reference=block(13,5.7,13,70,18,1.6)
assembly.add(lcd_reference,name='LCD_reference_not_for_printing',color=cq.Color(.72,.75,.66))
assembly.add(adapter_reference,name='adapter_PCB_reference_not_for_printing',color=cq.Color(.1,.4,.2))
cq.exporters.export(adapter_reference,str(ROOT/'cad'/'display_adapter_outline.step'))
assembly.save(str(ROOT/'cad'/'calculator_assembly.step'))
# Remove obsolete loose-button aggregate if it exists from an older build.
(ROOT/'stl'/'all_16_buttons.stl').unlink(missing_ok=True)
for old in (ROOT/'stl').glob('button_r*.stl'):old.unlink(missing_ok=True)
# Exact board outline proxy is for visual assembly checks, not a printed PCB substrate.
pcb=block(7,62,7,82,68,1.6)
for x,y in pcbholes:pcb=hole(pcb,x,y,6.9,d=2.9,h=2)
cq.exporters.export(pcb,str(ROOT/'cad'/'pcb_outline.step'))
(ROOT/'validation'/'cad_checks.json').write_text(json.dumps(checks,indent=2))
(ROOT/'source'/'mechanical_parameters.json').write_text(json.dumps({
 'case_mm':[W,H,31],
 'pcb_mm':[82,68,1.6],
 'pcb_origin_plan_mm':[7,62],
 'pcb_bottom_z':7,
 'key_x_mm':KEY_X,
 'key_y_mm':KEY_Y,
 'nominal_key_pitch_mm':18,
 'electrical_keypad_membrane_max_envelope_mm':[72,79,.8],
 'custom_keypad':{
  'construction':'single connected flexible sheet',
  'material':'55A flexible resin',
  'sheet_origin_plan_mm':[SHEET_X,SHEET_Y],
  'sheet_mm':[SHEET_W,SHEET_H,SHEET_T],
  'button_top_mm':[BUTTON_W,BUTTON_H,BUTTON_RISE],
  'actuator_diameter_mm':ACTUATOR_D,
  'actuator_projection_mm':ACTUATOR_H,
  'legend_depth_mm':.4,
  'continuous_dust_barrier':True
 },
 'button_travel_stop_mm':.5,
 'button_rest_gap_mm':.15,
 'screw_clearance_mm':2.9,
 'nut_AF_mm':5.35,
 'nut_pocket_depth_mm':2.45,
 'keypad_pitch_status':'nominal; check full-size template against actual DIYmalls keypad',
 'display':{'part':'ERC12864FS-655','body_mm':[70,50,5.8],'origin_plan_mm':[13,7.5],'window_mm':[14.5,11,67,37],'adapter_mm':[70,18,1.6],'adapter_origin_mm':[13,5.7,13],'foam_each_face_mm':.5},
 'battery_holder':'Pololu 1144, 52 x 37 x 13 mm'
},indent=2))
print('CAD EXPORT COMPLETE',flush=True)
