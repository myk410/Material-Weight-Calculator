"""Draw numbered 1:1 top and true mirrored-underside review templates from KiCad.
This is an assembly projection, not a copper/manufacturing file.
"""
from pathlib import Path
from html import escape
import pcbnew as k
ROOT=Path(__file__).resolve().parents[1]
def render(name,path,width,height):
    board=k.LoadBoard(str(path));out=[]
    totalw=2*width+24;totalh=height+28
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{totalw}mm" height="{totalh}mm" viewBox="0 0 {totalw} {totalh}">')
    out.append('<rect width="100%" height="100%" fill="white"/><style>text{font-family:monospace;fill:#142b45} .pin{font-size:.7px;text-anchor:middle;dominant-baseline:middle} .ref{font-size:1.1px;text-anchor:middle;font-weight:bold}</style>')
    out.append('<text x="5" y="4" font-size="2">R3 FABRICATION HOLD - print 100%, measure scale, overlay actual parts</text>')
    for side,base in [('Top - components installed from F.Cu',5),('Underside - mirrored, NOT installation side',width+15)]:
        flip=base>5;ox=base;oy=12
        out.append(f'<text x="{ox}" y="9" font-size="1.6">{side}</text><rect x="{ox}" y="{oy}" width="{width}" height="{height}" fill="#f3f7fb" stroke="#142b45" stroke-width=".15"/>')
        for f in board.GetFootprints():
            ref=f.GetReference();pos=f.GetPosition();x=pos.x/1e6-50;y=pos.y/1e6-50
            if flip:x=width-x
            ry=y-3 if ref not in ['U2','R3','R4','R5','R6','R8','C6','C1'] else y-1.8
            tx=x
            if name=='main':
                positions={'C1':(34,15.5),'C2':(31,23.2),'C6':(27,11.8),'R8':(23,11.8),'U2':(25,13.8),'L1':(17.8,18.1),'R5':(34,4),'R4':(34,8),'R3':(23,5.2),'R6':(27,5.2)}
                if ref in positions:
                    tx,ry=positions[ref]
                    if flip:tx=width-tx
            out.append(f'<text class="ref" x="{ox+tx}" y="{oy+ry}">{escape(ref)}</text>')
            if ref=='U1':
                # Socket body projection and notch: visible from top; dashed from below.
                left=width-43.76 if flip else 33.86
                out.append(f'<rect x="{ox+left}" y="{oy+18.73}" width="9.9" height="35.56" fill="none" stroke="#697d90" stroke-width=".15" stroke-dasharray=".5 .4"/>')
                out.append(f'<text x="{ox+x+(-3.81 if flip else 3.81)}" y="{oy+18}" font-size=".9" text-anchor="middle">NOTCH</text>')
            for p in f.Pads():
                q=p.GetPosition();px=q.x/1e6-50;py=q.y/1e6-50;num=p.GetNumber();n=p.GetNetname()
                if flip:px=width-px
                sx,sy=p.GetSize().x/1e6,p.GetSize().y/1e6
                if round(p.GetOrientation().AsDegrees())%180==90:sx,sy=sy,sx
                color='#f9cf7a' if num=='1' else '#c8d7e6'
                if p.GetAttribute()==k.PAD_ATTRIB_SMD:
                    out.append(f'<rect x="{ox+px-sx/2}" y="{oy+py-sy/2}" width="{sx}" height="{sy}" fill="{color}" stroke="#53697f" stroke-width=".06"/>')
                else:
                    if p.GetShape()==k.PAD_SHAPE_RECT:out.append(f'<rect x="{ox+px-sx/2}" y="{oy+py-sy/2}" width="{sx}" height="{sy}" fill="{color}" stroke="#53697f" stroke-width=".07"/>')
                    else:out.append(f'<ellipse cx="{ox+px}" cy="{oy+py}" rx="{sx/2}" ry="{sy/2}" fill="{color}" stroke="#53697f" stroke-width=".07"/>')
                    d=p.GetDrillSize().x/1e6
                    if not num:out.append(f'<circle cx="{ox+px}" cy="{oy+py}" r="{d/2}" fill="white" stroke="#53697f" stroke-width=".07"/>')
                if num:
                    # MSOP lead numbers sit just outside the toe at a legible .5 mm pitch.
                    if ref=='U2':
                        tx=px+(-1.4 if int(num)<=5 else 1.4)*(-1 if flip else 1)
                        out.append(f'<text x="{ox+tx}" y="{oy+py+.17}" font-size=".55" text-anchor="middle">{num}</text>')
                    else:out.append(f'<text class="pin" x="{ox+px}" y="{oy+py}">{num}</text>')
    y=height+20
    out.append(f'<path d="M 5,{y} h 50 m -50,-1 v 2 m 50,-2 v 2" fill="none" stroke="#142b45" stroke-width=".15"/><text x="60" y="{y+.5}" font-size="1.7">50 mm scale; gold = pad 1. See orientation_pins.csv for every net.</text>')
    out.append('</svg>')
    (ROOT/'docs'/'r3'/(name+'_orientation_1to1.svg')).write_text(''.join(out))
if __name__=='__main__':
    render('main',ROOT/'pcb'/'r3'/'material_weight_calculator.kicad_pcb',82,68)
    render('adapter',ROOT/'pcb'/'display_adapter'/'display_adapter.kicad_pcb',70,18)
