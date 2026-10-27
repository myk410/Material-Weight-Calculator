from pathlib import Path
import json,itertools,struct,collections,xml.etree.ElementTree as E
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import build_case as design
ROOT=Path(__file__).resolve().parents[1]
parts={n:p for n,p in design.parts.items() if not n.startswith('fit_coupon') and n not in ['front_shell','rear_shell']}
collisions=[]
for (na,a),(nb,b) in itertools.combinations(parts.items(),2):
 ba=a.val().BoundingBox();bb=b.val().BoundingBox()
 if any(min(getattr(ba,ax+'max'),getattr(bb,ax+'max'))-max(getattr(ba,ax+'min'),getattr(bb,ax+'min'))<=.0001 for ax in 'xyz'):continue
 overlap=a.val().intersect(b.val()).Volume()
 if overlap>.02:collisions.append({'a':na,'b':nb,'overlap_mm3':overlap})
print('COLLISIONS',collisions,flush=True)
(ROOT/'validation'/'assembly_collision_checks.json').write_text(json.dumps({'intersections_above_0.02_mm3':collisions},indent=2))
# Confirm actual exported binary STLs have a closed, two-use mesh edge graph.
mesh=[]
for p in sorted((ROOT/'stl').rglob('*.stl')):
 raw=p.read_bytes();n=struct.unpack_from('<I',raw,80)[0];edges=collections.Counter()
 if len(raw)!=84+n*50:raise RuntimeError('Not binary STL '+p.name)
 for i in range(n):
  coords=struct.unpack_from('<12f',raw,84+i*50)[3:]
  v=[tuple(round(c,4) for c in coords[j:j+3]) for j in [0,3,6]]
  for a,b in [(v[0],v[1]),(v[1],v[2]),(v[2],v[0])]:edges[tuple(sorted((a,b)))]+=1
 bad=sum(x!=2 for x in edges.values());mesh.append({'file':p.name,'triangles':n,'non_manifold_edges':bad})
 if bad:raise RuntimeError(f'{p.name}: {bad} non-manifold edges')
(ROOT/'validation'/'stl_mesh_checks.json').write_text(json.dumps(mesh,indent=2))
# Independently compare exported Eeschema nets with pad/net records used by pcbnew.
elec=json.loads((ROOT/'source'/'electrical_design.json').read_text());xml=E.parse(ROOT/'pcb'/'material_weight_calculator.net.xml')
actual={}
for net in xml.findall('.//nets/net'):
 for node in net.findall('node'):
  name=net.get('name')
  if not name.startswith('unconnected-'):actual[(node.get('ref'),node.get('pin'))]=name.lstrip('/')
expected={(c['ref'],p):n for c in elec['components'] for p,n in c['pins'].items() if n}
assert actual==expected,{'missing':sorted(set(expected.items())-set(actual.items())),'extra':sorted(set(actual.items())-set(expected.items()))}
(ROOT/'validation'/'schematic_net_check.json').write_text(json.dumps({'matched_connected_pins':len(actual),'result':'PASS'},indent=2))
# Printer bounds verified from the actual oriented STL vertices, with 5 mm XY
# clearance on each side and 10 mm Z reserved for supports.
printer=[]
for p in sorted((ROOT/'stl'/'mars5_ultra_oriented').glob('*.stl')):
 raw=p.read_bytes();n=struct.unpack_from('<I',raw,80)[0]
 v=np.array([struct.unpack_from('<12f',raw,84+i*50)[3:] for i in range(n)]).reshape(-1,3)
 dims=v.max(axis=0)-v.min(axis=0);fits=bool(np.all(dims+np.array([10,10,10])<=np.array([153.36,77.76,165])))
 printer.append({'file':p.name,'bbox_mm':dims.tolist(),'with_support_allowance_fits':fits})
 assert fits,p.name
(ROOT/'validation'/'mars5_ultra_fit_checks.json').write_text(json.dumps(printer,indent=2))
# Actual BREP mesh previews, not generated imagery.
def draw(filename,exploded=False):
 fig=plt.figure(figsize=(7,10),facecolor='#f5f4f0');ax=fig.add_subplot(111,projection='3d');ax.set_facecolor('#f5f4f0')
 names=list(parts) if exploded else ['mars_front_upper','mars_front_lower','LCD_reference']+[n for n in parts if n.startswith('button')]
 for name in names:
  obj=parts[name].val();verts,faces=obj.tessellate(.08,.15);verts=np.array([[v.x,v.y,v.z] for v in verts]);faces=np.array(faces)
  if exploded:
   shift=60 if name.startswith('button') else 45 if name.startswith('mars_front') else 35 if name=='keypad_guide' else 25 if name=='keypad_backing' else 18 if name.startswith('display') else 0
   verts[:,2]+=shift
  triangles=verts[faces];norm=np.cross(triangles[:,1]-triangles[:,0],triangles[:,2]-triangles[:,0]);lens=np.linalg.norm(norm,axis=1);norm/=np.maximum(lens[:,None],1e-12)
  light=np.where(np.abs(norm[:,2])>.9,.9,.5);base=np.array([.75,.78,.72]) if name.startswith('button') else np.array([.72,.75,.66]) if name=='LCD_reference' else np.array([.36,.41,.43])
  colors=np.clip(base[None,:]*(.65+.35*light[:,None]),0,1)
  if name.startswith('button'):
   top=verts[:,2].max();engraved=(triangles[:,:,2].mean(axis=1)<top-.12)&(triangles[:,:,2].mean(axis=1)>top-.6);colors[engraved]=[.12,.15,.12]
  coll=Poly3DCollection(triangles,facecolors=colors,edgecolors='none',linewidths=0,antialiased=False,rasterized=True);ax.add_collection3d(coll)
 ax.set_xlim(-3,99);ax.set_ylim(-3,187);ax.set_zlim(0,100 if exploded else 36);ax.set_box_aspect((102,190,100 if exploded else 36));ax.set_proj_type('ortho');ax.view_init(elev=40 if exploded else 90,azim=-90);ax.set_axis_off()
 fig.subplots_adjust(left=0,right=1,bottom=0,top=.95);fig.suptitle('Exploded CAD assembly' if exploded else 'Actual CAD: recessed button legends',fontsize=15,color='#20332f',y=.98)
 fig.savefig(ROOT/'docs'/filename,dpi=200,bbox_inches='tight');plt.close(fig)
# Check actual component envelopes against the printed supports and shells.
envelopes={'LCD_reference':design.lcd_reference,'adapter_PCB_reference':design.adapter_reference}
envelope_checks=[]
for name,part in envelopes.items():
 for printed,solid in parts.items():
  overlap=part.val().intersect(solid.val()).Volume()
  if overlap>.02:envelope_checks.append({'component':name,'printed_part':printed,'overlap_mm3':overlap})
(ROOT/'validation'/'display_envelope_checks.json').write_text(json.dumps({'intersections_above_0.02_mm3':envelope_checks},indent=2))
assert not envelope_checks,envelope_checks
parts.update(envelopes)
draw('case_front_preview.png');draw('assembly_exploded_preview.png',True)
print('MESHES AND NETLIST PASS',len(mesh),len(actual),flush=True)
if collisions:raise RuntimeError('Assembly collisions remain')
