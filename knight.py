"""Angular horse knight, beveled polygon sculpt, meshed with marching tetrahedra.
Requires numpy. Coordinates below are pre-scale millimeters. No external assets.
"""
import numpy as np

def polygon_distance(x,z,poly):
    distance=np.full_like(x,np.inf)
    inside=np.zeros_like(x,dtype=bool)
    for a,b in zip(poly,poly[1:]+poly[:1]):
        vx,vz=b[0]-a[0],b[1]-a[1]
        t=np.clip(((x-a[0])*vx+(z-a[1])*vz)/(vx*vx+vz*vz),0,1)
        distance=np.minimum(distance,(x-a[0]-t*vx)**2+(z-a[1]-t*vz)**2)
        if abs(vz)>1e-12:
            inside^=((a[1]>z)!=(b[1]>z)) & (x<(b[0]-a[0])*(z-a[1])/vz+a[0])
    return np.sqrt(distance)*np.where(inside,-1,1)

def field(points):
    x,y,z=points[...,0],points[...,1],points[...,2]
    # Angular, continuous horse silhouette, with an inset throat and sloping face.
    z=np.where(z>6,6+(z-6)/.94,z)
    silhouette=[(-8.6,5.2),(7.3,5.2),(4.7,9.3),(1.0,14.5),
        (-.1,19.6),(2.3,22.1),(5.3,21.5),(10.2,22.1),(10.7,24.8),
        (7.6,26.5),(4.3,30.0),(.4,33.2),(-3.3,33.6),(-6.1,30.0),
        (-8.7,24.2),(-9.1,17.1),(-7.0,10.0)]
    dist=polygon_distance(x,z,silhouette)
    width=np.interp(z,[5,11,20,27,34],[6.2,4.8,3.8,3.3,2.7])
    edge=np.abs(y)-width
    body=np.maximum.reduce([dist,edge,(dist+edge+.65)/np.sqrt(2)])
    # Two tapered triangular ears, with broad roots sunk into the poll.
    earpoly=[(-4.7,31.5),(-1.6,32.8),(-3.8,37.1)]
    ear=polygon_distance(x,z,earpoly)
    for side in [-1,1]:
        earwidth=np.abs(y-side*1.95)-.95
        earsolid=np.maximum.reduce([ear,earwidth,(ear+earwidth+.18)/np.sqrt(2)])
        body=np.minimum(body,earsolid)
    # Narrow angular mane ridge behind the neck.
    mane=polygon_distance(x,z,[(-8.9,12),(-10,18),(-9.4,25),(-7,31.3),(-4.8,33),(-6.3,28.5),(-7.2,22),(-7.4,15)])
    body=np.minimum(body,np.maximum(mane,np.abs(y)-1.7))
    r=np.sqrt(x*x+y*y)
    br=np.interp(z,[0,.8,3,5,6],[11.7,12.5,12.5,10.5,10.5])
    base=np.maximum.reduce([r-br,-z,z-6])
    result=np.minimum(base,body)
    # Clean facets: no eye, nostril or mouth engravings.
    return result

def make_knight(scale=1.4,step=.30):
    axes=[np.arange(-13.27,13.6,step),np.arange(-13.19,13.6,step),np.arange(-.23,36.5,step)]
    grid=np.stack(np.meshgrid(*axes,indexing='ij'),axis=-1)
    shape=grid.shape[:3];values=field(grid).ravel();points=grid.reshape(-1,3)
    ids=np.arange(len(points)).reshape(shape)
    cells=np.stack([ids[:-1,:-1,:-1],ids[1:,:-1,:-1],ids[1:,1:,:-1],ids[:-1,1:,:-1],
                    ids[:-1,:-1,1:],ids[1:,:-1,1:],ids[1:,1:,1:],ids[:-1,1:,1:]],axis=-1).reshape(-1,8)
    cv=values[cells];cells=cells[(cv.min(axis=1)<0)&(cv.max(axis=1)>0)]
    tetra=[(0,1,2,6),(0,2,3,6),(0,3,7,6),(0,7,4,6),(0,4,5,6),(0,5,1,6)]
    vertices=[];faces=[];cache={}
    def vertex(a,b):
        key=(min(a,b),max(a,b))
        if key not in cache:
            t=values[a]/(values[a]-values[b])
            cache[key]=len(vertices)
            vertices.append(points[a]+t*(points[b]-points[a]))
        return cache[key]
    for tet in tetra:
        ts=cells[:,tet];tv=values[ts];ts=ts[(tv.min(axis=1)<0)&(tv.max(axis=1)>0)]
        for row in ts:
            inside=[int(a) for a in row if values[a]<0]
            outside=[int(a) for a in row if values[a]>=0]
            # All polygons ordered so their normals point from inside to outside.
            if len(inside)==1:
                a=inside[0];poly=[vertex(a,b) for b in outside]
                tris=[poly]
            elif len(inside)==3:
                a=outside[0];poly=[vertex(a,b) for b in inside]
                tris=[poly]
            else:
                a,b=inside;c,d=outside
                ac,ad,bc,bd=vertex(a,c),vertex(a,d),vertex(b,c),vertex(b,d)
                tris=[(ac,ad,bd),(ac,bd,bc)]
            outward=points[outside].mean(axis=0)-points[inside].mean(axis=0)
            for tri in tris:
                a,b,c=(vertices[i] for i in tri)
                if np.dot(np.cross(b-a,c-a),outward)<0:tri=(tri[0],tri[2],tri[1])
                faces.append(tuple(tri))
    return [tuple(float(x*scale) for x in v) for v in vertices],faces
