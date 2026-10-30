from pathlib import Path
import cadquery as cq, math, json

ROOT=Path(__file__).resolve().parents[1]
W,H=96.0,184.0
for p in [ROOT/'stl',ROOT/'stl'/'mars5_ultra_oriented',ROOT/'cad',ROOT/'validation']:
    p.mkdir(parents=True,exist_ok=True)

def block(x,y,z,w,h,d,r=0):
    s=cq.Workplane('XY').box(w,h,d).translate((x+w/2,H-y-h/2,z+d/2))
    if r: s=s.edges('|Z').fillet(r)
    return s

def cyl(x,y,z,r,d): return cq.Workplane('XY').circle(r).extrude(d).translate((x,H-y,z))
def hole(s,x,y,z,d=2.9,h=40): return s.cut(cyl(x,y,z,d/2,h))
def nut(s,x,y,z,af=5.35,h=2.45):
    n=cq.Workplane('XY').polygon(6,af/math.cos(math.pi/6)).extrude(h).translate((x,H-y,z))
    return s.cut(n)
def boss(s,x,y,z,h,r=4): return s.union(cyl(x,y,z,r,h))

# Rear shell: R2 geometry retained except battery-door screw bosses are replaced
# by locating ledges, two lower hooks and one broad shallow top snap catch.
b=block(0,0,0,W,H,12,6).cut(block(2.6,2.6,2.6,W-5.2,H-5.2,10,4))
caseholes=[(6,6),(90,6),(6,178),(90,178)]
for x,y in caseholes:
    b=boss(b,x,y,2.6,9.4); b=hole(b,x,y,-.1,h=13); b=b.cut(cyl(x,y,-.1,2.6,2.1))
pcbholes=[(12,67),(84,67),(12,125),(84,125)]
for x,y in pcbholes:
    b=boss(b,x,y,2.6,4.4); b=hole(b,x,y,2.5,h=8); b=nut(b,x,y,4.55,h=2.45)
# Existing shell anti-warp ribs.
for x in [19,77]: b=b.union(block(x,10,2.5,1.2,122,1.8))
for y in [30,58,100]: b=b.union(block(10,y,2.5,76,1.2,1.8))
# Pololu 1144 holder envelope and access cavity.
for x in [20,74.8]: b=b.union(block(x,139,2.5,1.2,39,11))
b=b.union(block(20,138,2.5,56,1.2,11)).union(block(20,178,2.5,56,1.2,11))
b=b.cut(block(13,137,-.1,70,45,2.15,2)).cut(block(19,140,-.1,58,39,3))
# Screwless door mating features.
b=b.union(block(12.95,139.0,1.65,1.35,40.2,1.15,.25))
b=b.union(block(81.70,139.0,1.65,1.35,40.2,1.15,.25))
for x in [25.0,67.0]: b=b.union(block(x-6.0,179.05,1.55,12.0,1.35,1.35,.25))
b=b.union(block(42.0,136.45,1.55,12.0,1.55,1.35,.25))
b=b.cut(block(39.5,134.9,-.1,17.0,3.0,2.3,1.2))
for x in [39.0,55.7]: b=b.union(block(x,136.2,1.55,1.2,4.0,2.0,.25))
rear_shell=b

# Screwless battery cover. Base clearance is intentionally loose for cured resin.
cover=block(13.35,137.35,0,69.30,44.25,1.80,1.8)
# Shallow internal rib grid to fight warping without crowding the AAA holder.
for x in [26.0,47.4,68.8]: cover=cover.union(block(x-.55,140.0,1.78,1.10,37.2,.75,.25))
for y in [148.0,160.0,172.0]: cover=cover.union(block(18.0,y-.55,1.78,59.9,1.10,.75,.25))
# Bottom hooks engage first.
for x in [25.0,67.0]:
    cover=cover.union(block(x-5.2,178.0,1.72,10.4,2.65,1.05,.35))
    cover=cover.union(block(x-4.6,179.65,2.20,9.2,1.05,.65,.25))
# Long, broad cantilever latch for ABS-like resin: low strain, shallow tooth.
cover=cover.union(block(43.0,138.15,1.78,10.0,24.0,1.15,.45))
cover=cover.cut(block(41.9,138.0,1.65,1.0,22.3,1.55,.25))
cover=cover.cut(block(53.1,138.0,1.65,1.0,22.3,1.55,.25))
cover=cover.union(block(44.0,137.25,2.55,8.0,1.20,.55,.25))
cover=cover.union(block(42.2,137.35,1.78,11.6,3.4,1.0,.6))
for gx in [44.2,47.0,49.8,52.6]: cover=cover.cut(block(gx,137.55,2.55,.45,2.3,.45,.15))
battery_cover=cover

# Mars 5 Ultra split exactly as the main enclosure generator.
seam=60.25
upper=rear_shell.intersect(block(-1,-1,-1,W+2,seam+1,40))
lower=rear_shell.intersect(block(-1,seam,-1,W+2,H-seam+1,40))
for x in [2.5,91.7]:
    upper=upper.union(block(x,seam-4,4,1.8,10,6))
    lower=lower.cut(block(x-.2,seam-.2,3.8,2.2,6.4,6.4))
upper=upper.union(block(4,seam-3,.8,88,6,1))
lower=lower.cut(block(3.8,seam-.2,.6,88.4,3.4,1.4))

parts={'battery_cover':battery_cover,'rear_shell_whole_reference':rear_shell,'mars_rear_upper':upper,'mars_rear_lower':lower}
checks=[]
for name,part in parts.items():
    sh=part.val(); bb=sh.BoundingBox(); solids=len(sh.Solids())
    checks.append({'part':name,'valid':sh.isValid(),'solid_count':solids,'volume_mm3':sh.Volume(),'bbox':[bb.xmin,bb.ymin,bb.zmin,bb.xmax,bb.ymax,bb.zmax]})
    if not sh.isValid() or solids!=1: raise RuntimeError(f'{name}: invalid/disconnected')
    printable=part.translate((-bb.xmin,-bb.ymin,-bb.zmin))
    dest=(ROOT/'cad'/'rear_shell_whole_reference.stl') if name=='rear_shell_whole_reference' else (ROOT/'stl'/f'{name}.stl')
    cq.exporters.export(printable,str(dest),tolerance=.035,angularTolerance=.12)
    if name.startswith('mars_rear_'):
        oriented=printable.rotate((0,0,0),(0,1,0),65).rotate((0,0,0),(0,0,1),90)
        ob=oriented.val().BoundingBox(); oriented=oriented.translate((-ob.xmin,-ob.ymin,-ob.zmin))
        cq.exporters.export(oriented,str(ROOT/'stl'/'mars5_ultra_oriented'/f'{name}.stl'),tolerance=.035,angularTolerance=.12)

(ROOT/'validation'/'battery_r3_checks.json').write_text(json.dumps(checks,indent=2))
print(json.dumps(checks,indent=2))
