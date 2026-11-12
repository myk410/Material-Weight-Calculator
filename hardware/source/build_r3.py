"""Create R3 from the preserved R2.1 board; no manufacturing exports.
Run with KiCad 9's Python and numpy/scipy/shapely. See R3_REVIEW.md.
"""
from pathlib import Path
import json, shutil, math, heapq, itertools, sys
import numpy as np
from scipy.ndimage import distance_transform_edt
import shapely
from shapely.geometry import box, Point, LineString
from shapely.affinity import rotate, translate
import pcbnew as k
from refresh_schematics import refresh
ROOT=Path(__file__).resolve().parents[1]
ADAPTER='--adapter' in sys.argv
BASE=ROOT/'pcb'/'display_adapter' if ADAPTER else ROOT/'pcb'
OUT=ROOT/'pcb'/'r3'/'display_adapter' if ADAPTER else ROOT/'pcb'/'r3'; OUT.mkdir(exist_ok=True,parents=True)
STEM='display_adapter' if ADAPTER else 'material_weight_calculator'
DATAFILE='r3_adapter_electrical_design.json' if ADAPTER else 'r3_electrical_design.json'
LIB=Path('/usr/share/kicad/footprints')
MM=k.FromMM
V=lambda x,y:k.VECTOR2I(MM(x+50),MM(y+50))
b=k.LoadBoard(str(BASE/(STEM+'.kicad_pcb')))
plugin=k.PCB_IO_KICAD_SEXPR(); keep=[]
data=json.loads((ROOT/'source'/('adapter_electrical_design.json' if ADAPTER else 'electrical_design.json')).read_text())
parts={c['ref']:c for c in data['components']}
# Reroute both layers; retain the connector, MCU and mounting-hole coordinates.
for track in list(b.GetTracks()):
    keep.append(track); b.Remove(track)
for ref in (['C1','C2','C3','C4','C5','R1'] if ADAPTER else ['U2','D1','C1','C2','C3','C4','C5','R1','R2','Q1']):
    old=next(f for f in b.GetFootprints() if f.GetReference()==ref)
    keep.append(old); b.Remove(old); parts.pop(ref)
local=OUT/'mw-footprints.pretty'; local.mkdir(exist_ok=True)
for p in (BASE/'mw-footprints.pretty').glob('*.kicad_mod'): shutil.copyfile(p,local/p.name)
nets={str(n.GetNetname()):n for n in b.GetNetsByName().values()}
def net(name):
    if name not in nets:
        nets[name]=k.NETINFO_ITEM(b,name); b.Add(nets[name])
    return nets[name]
def add(ref,value,lib,fp,x,y,pins,mpn='',angle=0,names=None):
    src=local if lib=='MW' else LIB/(lib+'.pretty')
    if src!=local: shutil.copyfile(src/(fp+'.kicad_mod'),local/(fp+'.kicad_mod'))
    f=plugin.FootprintLoad(str(local),fp,False)
    f.SetFPIDAsString('MW_footprints:'+fp);f.SetReference(ref);f.SetValue(value)
    f.SetPosition(V(x,y));f.SetOrientationDegrees(angle);b.Add(f)
    f.Value().SetVisible(False)
    f.Reference().SetTextSize(k.VECTOR2I(MM(.8),MM(.8)));f.Reference().SetTextThickness(MM(.12))
    for p in f.Pads():p.SetNet(net(pins[p.GetNumber()]))
    parts[ref]={'ref':ref,'value':value,'footprint':'MW_footprints:'+fp,'x':x,'y':y,'angle':angle,
                'pins':pins,'pin_names':names or {},'manufacturer_part_number':mpn,'mounting_side':'F.Cu'}
    return f
if not ADAPTER:
    # ADI MS drawing 05-08-1661 Rev F: 3x3 body, 4.9 +/-0.15 lead span, .5 pitch.
    # KiCad stock footprint already extends to x=+/-2.925, providing an accessible toe.
    add('U2','LTC3440EMS#PBF','Package_SO','MSOP-10_3x3mm_P0.5mm',25,16,
        {'1':'RT','2':'MODE','3':'SW1','4':'SW2','5':'GND','6':'+3V3','7':'VIN','8':'VIN','9':'FB','10':'VC'},
        'LTC3440EMS#PBF',names={'1':'RT','2':'MODE_SYNC','3':'SW1','4':'SW2','5':'GND','6':'VOUT','7':'VIN','8':'SHDN_SS','9':'FB','10':'VC'})
    # Sumida land drawing: inner gap 2.0, 2.65x7.3 lands. Extend only outside toes .65.
    fp='L_CDRH6D38_HandSolder'
    (local/(fp+'.kicad_mod')).write_text('''(footprint "L_CDRH6D38_HandSolder" (version 20240108) (generator pcbnew) (layer "F.Cu")
     (descr "Sumida CDRH6D38: 7mm maximum body, 4mm high, extended external toes; see bundled manufacturer PDF") (attr smd)
     (property "Reference" "REF**" (at 0 -4.6) (layer "F.SilkS") (effects (font (size .8 .8) (thickness .12))))
     (property "Value" "10uH" (at 0 0) (layer "F.Fab") (effects (font (size 1 1) (thickness .1))))
     (fp_rect (start -3.5 -3.5) (end 3.5 3.5) (stroke (width .1) (type default)) (fill none) (layer "F.Fab"))
     (fp_rect (start -4.55 -3.9) (end 4.55 3.9) (stroke (width .05) (type default)) (fill none) (layer "F.CrtYd"))
     (fp_line (start -0.65 -3.65) (end 0.65 -3.65) (stroke (width .12) (type default)) (layer "F.SilkS"))
     (fp_line (start -0.65 3.65) (end 0.65 3.65) (stroke (width .12) (type default)) (layer "F.SilkS"))
     (pad "1" smd rect (at 2.65 0) (size 3.3 7.3) (layers "F.Cu" "F.Paste" "F.Mask"))
     (pad "2" smd rect (at -2.65 0) (size 3.3 7.3) (layers "F.Cu" "F.Paste" "F.Mask")))''')
    add('L1','10uH','MW',fp,17.8,18.1,{'1':'SW1','2':'SW2'},'CDRH6D38NP-100NC',90)
    add('D1','SS14','Diode_SMD','D_SMA',14,5,{'1':'VIN','2':'VBAT_LINK'},'SS14',names={'1':'K','2':'A'})
    add('C1','10uF 25V X7R','Capacitor_SMD','C_1206_3216Metric_Pad1.33x1.80mm_HandSolder',31,15.5,{'1':'VIN','2':'GND'},'GRM31CR71E106KA12L',90)
    add('C2','22uF 25V X7R','Capacitor_SMD','C_1210_3225Metric_Pad1.33x2.70mm_HandSolder',31,20,{'1':'+3V3','2':'GND'},'GRM32ER71E226KE15L')
    RFP='R_0805_2012Metric_Pad1.20x1.40mm_HandSolder'
    def resistor(ref,val,x,y,pins,mpn,angle=0):return add(ref,val,'Resistor_SMD',RFP,x,y,pins,mpn,angle)
    resistor('R3','60.4k 1%',23,7,{'1':'RT','2':'GND'},'RC0805FR-0760K4L')
    resistor('R4','340k 1%',32,8,{'1':'+3V3','2':'FB'},'RC0805FR-07340KL',90)
    resistor('R5','200k 1%',32,4,{'1':'FB','2':'GND'},'RC0805FR-07200KL',90)
    resistor('R6','15k 1%',27,7,{'1':'VC','2':'COMP_NODE'},'RC0805FR-0715KL')
    add('C6','1.5nF C0G 50V','Capacitor_SMD','C_0805_2012Metric_Pad1.18x1.45mm_HandSolder',27,10,{'1':'COMP_NODE','2':'FB'},'GRM2165C1H152JA01D')
    resistor('R8','0R',23,10,{'1':'MODE','2':'VIN'},'RC0805JR-070RL')
    # p13 of ADI datasheet: mandatory for potential VIN>4.5V and overload.
    add('D2','PMEG2010ER','Diode_SMD','Nexperia_CFP3_SOD-123W',25,22.5,{'1':'VIN','2':'SW1'},'PMEG2010ER,115',180,{'1':'K','2':'A'})
    resistor('R7','2R 1%',17,24,{'1':'SW1','2':'SNUB'},'RC0805FR-072RL')
    add('C7','1nF C0G 50V','Capacitor_SMD','C_0805_2012Metric_Pad1.18x1.45mm_HandSolder',22,26.5,{'1':'SNUB','2':'GND'},'GRM2165C1H102JA01D')
    for ref,x,y,n in [('TP1',8,17,'VIN'),('TP2',8,20,'GND'),('TP3',74,48,'+3V3')]:
        add(ref,n,'TestPoint','TestPoint_Pad_D2.0mm',x,y,{'1':n})
    CFP='C_0603_1608Metric_Pad1.08x0.95mm_HandSolder'
    RSMALL='R_0603_1608Metric_Pad0.98x0.95mm_HandSolder'
    for ref,x,y in [('C3',47,39),('C4',34,58)]:
        add(ref,'100nF 25V X7R','Capacitor_SMD',CFP,x,y,{'1':'+3V3','2':'GND'},'GRM188R71E104KA01D')
    add('C5','2.2uF 25V X5R','Capacitor_SMD',CFP,64,12,{'1':'LCD_VCC','2':'GND'},'GRM188R61E225KA12D')
    add('R1','10k 1%','Resistor_SMD',RSMALL,50,22,{'1':'LCD_PWR_CTRL','2':'LCD_BASE'},'RC0603FR-0710KL')
    add('R2','100k 1%','Resistor_SMD',RSMALL,56,7,{'1':'+3V3','2':'LCD_BASE'},'RC0603FR-07100KL')
    add('Q1','MMBT3906LT1G','Package_TO_SOT_SMD','SOT-23_Handsoldering',58,15,{'1':'LCD_BASE','2':'+3V3','3':'LCD_VCC'},'MMBT3906LT1G',names={'1':'B','2':'E','3':'C'})
else:
    CFP='C_0603_1608Metric_Pad1.08x0.95mm_HandSolder'
    for ref,x,na,nb in [('C1',41,'VB0_PLUS','VB0_MINUS'),('C2',48,'VB1_PLUS','VB1_MINUS')]:
        add(ref,'2.2uF 25V X5R','Capacitor_SMD',CFP,x,10,{'1':na,'2':nb},'GRM188R61E225KA12D')
    add('C3','330nF 25V X7R','Capacitor_SMD',CFP,55,10,{'1':'VLCD','2':'GND'},'C1608X7R1E334K080AC')
    add('C4','100nF 25V X7R','Capacitor_SMD',CFP,62,10,{'1':'LCD_VCC','2':'GND'},'GRM188R71E104KA01D')
    add('C5','10uF 25V X7R','Capacitor_SMD','C_1206_3216Metric_Pad1.33x1.80mm_HandSolder',8,7,{'1':'LCD_VCC','2':'GND'},'GRM31CR71E106KA12L')
    add('R1','10M 1%','Resistor_SMD','R_0603_1608Metric_Pad0.98x0.95mm_HandSolder',53,15,{'1':'VLCD','2':'GND'},'RC0603FR-0710ML')
# All through-hole components remain inserted from F.Cu. Stock references moved
# to non-overlapping rows by the review renderer; no reference is hidden.
for d in list(b.GetDrawings()):
    if isinstance(d,k.PCB_TEXT):b.Remove(d)
def text(t,x,y,size=.8,layer=k.F_SilkS):
    o=k.PCB_TEXT(b);o.SetText(t);o.SetPosition(V(x,y));o.SetTextSize(k.VECTOR2I(MM(size),MM(size)));o.SetTextThickness(MM(.12));o.SetLayer(layer)
    if layer==k.B_SilkS:o.SetMirrored(True)
    b.Add(o)
if not ADAPTER:
    text('MATERIAL WEIGHT R3 - HOLD',52,3,1)
    text('3xAAA / 3V3 - SEE R3_REVIEW',42,65,.9)
    for layer in [k.F_SilkS,k.B_SilkS]:
        for t,x,y in [('J1-1',8,22.5),('J1-8',8,40.3),('J3-1',74,16),('J3-8 NC',75,34.5),('J2 +',7,8),('J4-1 3V3',55,43),('U1 NOTCH',39,16.5)]:text(t,x,y,.8,layer)
    for f in b.GetFootprints():
        refpos={'C1':(34,15),'C2':(31,23),'TP1':(5.5,17),'TP2':(5.5,20),'R7':(17,26.5),'J2':(10,14.5),'J4':(52,48.5)}
        if f.GetReference() in refpos:f.Reference().SetPosition(V(*refpos[f.GetReference()]))
else:
    text('UC1701 R3 SMD - HOLD',37,6.5,.8)
    for layer in [k.F_SilkS,k.B_SilkS]:
        text('LCD-1',19,5.5,.8,layer);text('LCD-22',52,6.5,.8,layer);text('J1-1',6,16,.8,layer)
# Raster route exact pad polygons; every saved route is subsequently checked by KiCad DRC.
WIDTH,HEIGHT=data['board_size_mm']
GRID=.1;NX=round(WIDTH/GRID)+1;NY=round(HEIGHT/GRID)+1;N=NX*NY;CW=.2;CLR=.16
codes={n:i+1 for i,n in enumerate(sorted(nets))}; owners=np.zeros((2,NY,NX),dtype=np.int32)
xx,yy=np.meshgrid(np.arange(NX)*GRID,np.arange(NY)*GRID)
points=shapely.points(xx,yy)
for l in range(2): owners[l][(xx<.8)|(xx>WIDTH-.8)|(yy<.8)|(yy>HEIGHT-.8)]=-1
pads={}
def stamp(geom,l,code,margin):
    g=geom.buffer(margin)
    x0,y0,x1,y1=g.bounds
    xa=max(0,int(x0/GRID)-1);xb=min(NX,int(x1/GRID)+2);ya=max(0,int(y0/GRID)-1);yb=min(NY,int(y1/GRID)+2)
    mask=shapely.intersects(g,points[ya:yb,xa:xb]);sub=owners[l,ya:yb,xa:xb]
    sub[mask & ((sub==0)|(sub==code))]=code
    sub[mask & (sub!=code)]=-1
for f in b.GetFootprints():
    for p in f.Pads():
        pos=p.GetPosition();x,y=pos.x/1e6-50,pos.y/1e6-50
        sx,sy=p.GetSize().x/1e6,p.GetSize().y/1e6
        ang=p.GetOrientation().AsDegrees()
        # Rounded rectangles use their full bounding box, a conservative obstacle.
        g=Point(0,0).buffer(sx/2) if p.GetShape()==k.PAD_SHAPE_CIRCLE else box(-sx/2,-sy/2,sx/2,sy/2)
        g=translate(rotate(g,-ang,origin=(0,0)),x,y)
        layers=[l for l,kl in [(0,k.F_Cu),(1,k.B_Cu)] if p.IsOnLayer(kl)]
        n=p.GetNetname();code=codes.get(n,-1)
        for l in layers:stamp(g,l,code,CW/2+CLR+.025)
        pads[(f.GetReference(),p.GetNumber())]={'x':x,'y':y,'layers':layers,'net':n,'pad':p}
# Stamp any pre-routed copper as fixed obstacles.
for t in b.GetTracks():
    if isinstance(t,k.PCB_VIA):
        q=t.GetPosition();g=Point(q.x/1e6-50,q.y/1e6-50)
        for l in (0,1):stamp(g,l,codes[t.GetNetname()],t.GetWidth(k.F_Cu)/2e6+CW/2+CLR+.025)
    else:
        a=t.GetStart();c=t.GetEnd();g=LineString([(a.x/1e6-50,a.y/1e6-50),(c.x/1e6-50,c.y/1e6-50)])
        stamp(g,0 if t.GetLayer()==k.F_Cu else 1,codes[t.GetNetname()],t.GetWidth()/2e6+CW/2+CLR+.025)
def track(a,c,n,l=0,w=.2):
    if math.dist(a,c)<1e-6:return
    t=k.PCB_TRACK(b);t.SetStart(V(*a));t.SetEnd(V(*c));t.SetWidth(MM(w));t.SetLayer(k.F_Cu if l==0 else k.B_Cu);t.SetNet(net(n));b.Add(t)
    stamp(LineString([a,c]),l,codes[n],w/2+CW/2+CLR+.025)
placed_vias=set()
def via(x,y,n):
    key=(round(x,5),round(y,5),n)
    if key in placed_vias:return
    placed_vias.add(key)
    t=k.PCB_VIA(b);t.SetPosition(V(x,y));t.SetWidth(MM(.7));t.SetDrill(MM(.35));t.SetViaType(k.VIATYPE_THROUGH);t.SetLayerPair(k.F_Cu,k.B_Cu);t.SetNet(net(n));b.Add(t)
    for l in (0,1):stamp(Point(x,y),l,codes[n],.35+CW/2+CLR+.025)
# Explicit short front-only switch paths with no vias, wide after the lead exit.
if not ADAPTER:
    for n,coords in [('SW1',[(22.8875,16),(21.65,16),(20.9,15.2),(20,15.2)]),('SW2',[(22.8875,16.5),(21.76,16.5),(21.76,18),(20,20.5)])]:
        for i in range(len(coords)-1):track(coords[i],coords[i+1],n,w=[.2,.3,.6][i])
# Route a net to its nearest connected tree. Diagonal steps forbidden, preventing
# corner cutting around pad obstacles. Grid endpoints get exact copper endpoints.
def astar(a,c,n):
    code=codes[n];sx,sy=round(a['x']/GRID),round(a['y']/GRID);tx,ty=round(c['x']/GRID),round(c['y']/GRID)
    target={l*N+ty*NX+tx for l in c['layers']};q=[];cost={};prev={};count=itertools.count()
    for l in a['layers']:
        v=l*N+sy*NX+sx;cost[v]=0;heapq.heappush(q,(abs(sx-tx)+abs(sy-ty),next(count),v))
    valid=(owners==0)|(owners==code)
    # A via of .7mm requires more room than a .2mm trace; distance field is conservative.
    vd=np.minimum(distance_transform_edt(valid[0]),distance_transform_edt(valid[1]))
    vallowed=vd*GRID>=.4
    holes=[(p['x'],p['y'],p['pad'].GetDrillSize().x/2e6) for p in pads.values() if p['pad'].GetDrillSize().x]
    holes += [(hx,hy,.175) for hx,hy,_ in placed_vias]
    for hx,hy,hr in holes:
        radius=hr+.175+.27
        xa=max(0,int((hx-radius)/GRID)-1);xb=min(NX,int((hx+radius)/GRID)+2)
        ya=max(0,int((hy-radius)/GRID)-1);yb=min(NY,int((hy+radius)/GRID)+2)
        vallowed[ya:yb,xa:xb] &= np.hypot(xx[ya:yb,xa:xb]-hx,yy[ya:yb,xa:xb]-hy)>=radius
    while q:
        _,_,v=heapq.heappop(q)
        if v in target:
            out=[v]
            while v in prev:v=prev[v];out.append(v)
            return out[::-1]
        l=v//N;idx=v%N;x=idx%NX;y=idx//NX;g=cost[v]
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            u=x+dx;w=y+dy
            if not(0<=u<NX and 0<=w<NY) or not valid[l,w,u]:continue
            z=l*N+w*NX+u;ng=g+1
            if ng<cost.get(z,1e20):cost[z]=ng;prev[z]=v;heapq.heappush(q,(ng+abs(u-tx)+abs(w-ty),next(count),z))
        if vallowed[y,x]:
            z=(1-l)*N+idx;ng=g+30
            if ng<cost.get(z,1e20):cost[z]=ng;prev[z]=v;heapq.heappush(q,(ng+abs(x-tx)+abs(y-ty),next(count),z))
    raise RuntimeError(('no route',n,a['x'],a['y'],c['x'],c['y']))
def route(a,c,n):
    seq=astar(a,c,n);pts=[(v//N,((v%N)%NX)*GRID,((v%N)//NX)*GRID) for v in seq]
    pts=[(pts[0][0],a['x'],a['y'])]+pts+[(pts[-1][0],c['x'],c['y'])]
    last=anchor=pts[0];direction=None
    for p in pts[1:]:
        if p[0]!=last[0]:
            track(anchor[1:],last[1:],n,last[0]);via(last[1],last[2],n);anchor=p;direction=None
        else:
            d=(round(p[1]-last[1],6),round(p[2]-last[2],6));nd=(np.sign(d[0]),np.sign(d[1]))
            if direction is not None and nd!=direction:track(anchor[1:],last[1:],n,last[0]);anchor=last
            if nd!=(0,0):direction=nd
        last=p
    track(anchor[1:],last[1:],n,last[0])
# Route supply and analog nets first, then digital signals, then ground.
newnets=[] if ADAPTER else ['RT','MODE','VC','COMP_NODE','FB','SNUB','SW1','SW2','VIN','VBAT_LINK','VBAT_SW','+3V3','GND']
newnets = ([n for n in newnets if n!='GND']) + [n for n in sorted(nets) if n and n!='GND' and not n.startswith('unconnected-') and n not in newnets] + ['GND']
for n in newnets:
    todo=[p for p in pads.values() if p['net']==n]
    if not ADAPTER and n in ['SW1','SW2']:
        done=[pads[('U2','3' if n=='SW1' else '4')],pads[('L1','1' if n=='SW1' else '2')]]
        todo=[p for p in todo if all(p is not d for d in done)]
    else:done=[todo.pop(0)]
    while todo:
        _,i,j=min((math.hypot(a['x']-c['x'],a['y']-c['y']),i,j) for i,a in enumerate(done) for j,c in enumerate(todo))
        c=todo.pop(j);route(done[i],c,n);done.append(c)
    print('Routed',n,flush=True)
if not ADAPTER:
    zone=k.ZONE(b);zone.SetLayer(k.B_Cu);zone.SetNet(net('GND'));zone.SetLocalClearance(MM(.2));zone.SetPadConnection(k.ZONE_CONNECTION_THERMAL);zone.SetThermalReliefGap(MM(.3));zone.SetThermalReliefSpokeWidth(MM(.3));zone.SetMinThickness(MM(.2))
    poly=zone.Outline();poly.NewOutline()
    for x,y in [(1,1),(WIDTH-1,1),(WIDTH-1,HEIGHT-1),(1,HEIGHT-1)]:poly.Append(int(MM(x+50)),int(MM(y+50)))
    b.Add(zone);b.BuildConnectivity();k.ZONE_FILLER(b).Fill(b.Zones())
# The underlying project must permit the .15mm lead clearance at MSOP-10.
pro=json.loads((BASE/(STEM+'.kicad_pro')).read_text())
rules=pro['board']['design_settings']['rules'];rules.update(min_clearance=.15,min_track_width=.2,min_via_diameter=.7,min_through_hole_diameter=.3)
for c in pro['net_settings']['classes']:c.update(clearance=.15,track_width=.2,via_diameter=.7,via_drill=.35)
(OUT/(STEM+'.kicad_pro')).write_text(json.dumps(pro,indent=2)+'\n')
(OUT/'fp-lib-table').write_text('(fp_lib_table (lib (name "MW_footprints") (type "KiCad") (uri "${KIPRJMOD}/mw-footprints.pretty") (options "") (descr "Bundled reviewed footprints")))')
settings=b.GetDesignSettings();settings.m_MinClearance=MM(.15);settings.m_TrackMinWidth=MM(.2)
k.SaveBoard(str(OUT/(STEM+'.kicad_pcb')),b)
# Extract the actual board, independently of placement intent, for audit input.
data.update(revision='R3',status='FABRICATION_HOLD',trace_width_mm=.2,clearance_mm=.15,ground_plane='none; routed ground' if ADAPTER else 'B.Cu, filled with .2mm clearance and .3mm thermal spokes',components=list(parts.values()),pads=[],routes=[],vias=[])
for f in b.GetFootprints():
    for p in f.Pads():
        q=p.GetPosition();sz=p.GetSize()
        data['pads'].append({'ref':f.GetReference(),'pin':p.GetNumber(),'x':q.x/1e6-50,'y':q.y/1e6-50,'net':p.GetNetname(),'drill':p.GetDrillSize().x/1e6,'size_mm':[sz.x/1e6,sz.y/1e6],'side':'F.Cu' if p.GetAttribute()==k.PAD_ATTRIB_SMD else 'through'})
for t in b.GetTracks():
    if isinstance(t,k.PCB_VIA):
        p=t.GetPosition();data['vias'].append({'x':p.x/1e6-50,'y':p.y/1e6-50,'net':t.GetNetname(),'diameter':t.GetWidth(k.F_Cu)/1e6,'drill':t.GetDrillValue()/1e6})
    else:
        a=t.GetStart();c=t.GetEnd();data['routes'].append({'net':t.GetNetname(),'layer':0 if t.GetLayer()==k.F_Cu else 1,'a':[a.x/1e6-50,a.y/1e6-50],'b':[c.x/1e6-50,c.y/1e6-50],'width':t.GetWidth()/1e6})
(ROOT/'source'/DATAFILE).write_text(json.dumps(data,indent=2)+'\n')
refresh(adapter=ADAPTER,r3=True)
(OUT/(STEM+'.kicad_pro')).write_text(json.dumps(pro,indent=2)+'\n')
print('R3 CREATED; manufacturing output intentionally absent')

used={c['footprint'].split(':',1)[1] for c in parts.values()}
for p in local.glob('*.kicad_mod'):
    if p.stem not in used:p.unlink()
