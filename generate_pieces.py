"""Chud Chess v4. Run with Python 3 + numpy. Units: mm.
Editable ring profiles plus an implicit, sculpted horse knight.
"""
import math, struct, json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent
N = 96
SCALE = 1.4

def ring(z, rx, ry=None, cx=0, shape='ellipse', crown=0):
    ry = rx if ry is None else ry
    pts=[]
    for i in range(N):
        t=2*math.pi*i/N
        c,s=math.cos(t),math.sin(t)
        if shape=='rectangle':
            k=1/max(abs(c),abs(s))
            x,y=rx*c*k,ry*s*k
        else:
            x,y=rx*c,ry*s
        # Alternating high/low crenels, connected by narrow sloped walls.
        dz = crown if (i//8)%2==0 else 0
        pts.append((SCALE*(x+cx), SCALE*y, SCALE*(z+dz)))
    return pts

def base(r):
    return [ring(0,r-.8),ring(.8,r),ring(3,r),ring(5,r-2),ring(6,r-2)]

def pieces():
    p={}
    p['Pawn']=base(11)+[ring(7,7),ring(14,4.2),ring(16,5.5),ring(18,6),ring(21,5),ring(23,2)]
    p['Rook']=base(12.5)+[ring(7,8.5),ring(21,7.5),ring(23,10),ring(25,10),ring(27,10,crown=3),ring(27,6,crown=3),ring(24,6)]
    p['Knight']=base(12.5)+[ring(7,8.5),ring(12,6,4,cx=-1),ring(19,5,3.8,cx=-2),ring(24,5.5,3.5,cx=-1),ring(26,8,3.5,cx=2),ring(29,8,3.5,cx=2),ring(31,5,3.2,cx=-1),ring(35,2.3,2.6,cx=-3)]
    p['Bishop']=base(12.5)+[ring(7,8.5),ring(20,4.5),ring(22,7),ring(24,5.5),ring(27,7),ring(30,6),ring(36,1.2)]
    p['Queen']=base(13.5)+[ring(7,9.5),ring(24,5),ring(26,8),ring(28,6),ring(32,8),ring(34,8,crown=3),ring(34,4.5,crown=3),ring(32,4.5)]
    p['King']=base(14)+[ring(7,10),ring(26,5),ring(28,8),ring(30,6),ring(31,2,2,shape='rectangle'),ring(34,2,2,shape='rectangle'),ring(35,6,2,shape='rectangle'),ring(37,6,2,shape='rectangle'),ring(37.3,2,2,shape='rectangle'),ring(41,2,2,shape='rectangle')]
    return p

def mesh(rings):
    verts=[v for r in rings for v in r]
    faces=[]
    for k in range(len(rings)-1):
        for i in range(N):
            a=k*N+i;b=k*N+(i+1)%N;c=b+N;d=a+N
            faces.extend([(a,b,c),(a,c,d)])
    # Fan caps; last ring may cap a recessed crown floor.
    for ri,reverse in [(0,True),(len(rings)-1,False)]:
        r=rings[ri]
        center=tuple(sum(p[j] for p in r)/N for j in range(3))
        v=len(verts);verts.append(center)
        for i in range(N):
            a=ri*N+i;b=ri*N+(i+1)%N
            faces.append((v,b,a) if reverse else (v,a,b))
    return verts,faces

def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))

def validate(verts,faces):
    edges=Counter();directed=Counter();volume=0
    for f in faces:
        a,b,c=[verts[i] for i in f]
        normal=cross(sub(b,a),sub(c,a))
        assert dot(normal,normal)>1e-24,'Degenerate triangle'
        volume+=dot(a,cross(b,c))/6
        for u,v in zip(f,(f[1],f[2],f[0])):
            edges[tuple(sorted((u,v)))]+=1;directed[(u,v)]+=1
    assert set(edges.values())=={2},'Open/nonmanifold edge'
    assert all(directed[(b,a)]==n for (a,b),n in directed.items()),'Winding mismatch'
    assert len(verts)-len(edges)+len(faces)==2,'Unexpected topology'
    assert volume>0,'Negative volume'
    return {'watertight_edges':True,'consistent_winding':True,'euler_number':2,
            'volume_mm3':round(volume,1),'triangles':len(faces),
            'size_mm':[round(max(v[i] for v in verts)-min(v[i] for v in verts),2) for i in range(3)]}

def save_stl(path,verts,faces):
    with path.open('wb') as out:
        out.write(b'Chud Chess v4 | millimeters'.ljust(80,b'\0'))
        out.write(struct.pack('<I',len(faces)))
        for f in faces:
            a,b,c=[verts[i] for i in f]
            n=cross(sub(b,a),sub(c,a));length=math.sqrt(dot(n,n));n=tuple(x/length for x in n)
            out.write(struct.pack('<12fH',*n,*a,*b,*c,0))

def main():
    (ROOT/'STL').mkdir(exist_ok=True)
    report={}
    for name,rings in pieces().items():
        if name=='Knight':
            from knight import make_knight
            verts,faces=make_knight(SCALE)
        else:
            verts,faces=mesh(rings)
        report[name]=validate(verts,faces)
        save_stl(ROOT/'STL'/f'ChudChess_{name}.stl',verts,faces)
    (ROOT/'mesh_checks.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
