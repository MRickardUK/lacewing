import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot
#from matplotlib import cm
from matplotlib.patches import Ellipse
import kinematics
import ellipse
import lacewing
import sys
from astropy.io import ascii

def traceback(argv=None):
    if argv is None:
        argv = sys.argv
        
    name,coords,era,edec,pmra,epmra,pmdec,epmdec,rv,erv,pi,epi = lacewing.csv_loader(argv[1])
    mgpname = argv[2].replace(' ','_')
    n_init = int(argv[3])
    print name,era
    era = np.asarray(era)
    edec = np.asarray(era)
    pmra = np.asarray(pmra)
    epmra = np.asarray(epmra)
    pmdec = np.asarray(pmdec)
    epmdec = np.asarray(epmdec)
    pi = np.asarray(pi)
    epi = np.asarray(epi)
    rv = np.asarray(rv)
    erv = np.asarray(erv)


    # How many stars are we fitting?
    goodlist = [x for x in range(len(pi)) if (pi[x] is not None) and (rv[x] is not None) and (pmra[x] is not None) and (pmdec[x] is not None)]

    ra = np.array(())
    dec = np.array(())
    for b in goodlist:
        ra = np.append(ra,coords[b].ra.degree)
        dec = np.append(dec,coords[b].dec.degree)

    era = era[goodlist]
    edec = edec[goodlist]
    pmra = pmra[goodlist]
    epmra = epmra[goodlist]
    pmdec = pmdec[goodlist]
    epmdec = epmdec[goodlist]
    pi = pi[goodlist]
    epi = epi[goodlist]
    rv = rv[goodlist]
    erv = erv[goodlist]

    print goodlist
    print len(goodlist)
    n_stars = len(goodlist)

    uvwlist = []
    xyzlist = []
    outfile = open("Moving_Group_{0:}.dat".format(mgpname),"wb")
    outfile.write("Time X eX Y eY Z eZ A eA B eB C eC XY eXY XZ eXZ YZ eYZ\n")
    for j in xrange(n_init):
        tra = ra + (np.random.randn(n_stars)*era)*np.cos(dec*np.pi/180.)
        tdec = dec + np.random.randn(n_stars)*edec
        tpi = pi + np.random.randn(n_stars)*epi
        tpmra = pmra + np.random.randn(n_stars)*epmra 
        tpmdec = pmdec + np.random.randn(n_stars)*epmdec 
        trv = rv + np.random.randn(n_stars)*erv
        #print j
        tu,tv,tw,tx,ty,tz = kinematics.gal_uvwxyz(ra=tra,dec=tdec,plx=tpi,pmra=tpmra,pmdec=tpmdec,vrad=trv)
        tu = np.array(tu,dtype=np.float64)
        tv = np.array(tv,dtype=np.float64)
        tw = np.array(tw,dtype=np.float64)
        tx = np.array(tx,dtype=np.float64)
        ty = np.array(ty,dtype=np.float64)
        tz = np.array(tz,dtype=np.float64)
        obj = ellipse.fitellipse(tx,ty,tz)
        xyzlist.append(obj)
        obj = ellipse.fitellipse(tu,tv,tw)
        uvwlist.append(obj)

    u = np.mean([uvwlist[m]['x'] for m in range(n_init)])
    v = np.mean([uvwlist[m]['y'] for m in range(n_init)])
    w = np.mean([uvwlist[m]['z'] for m in range(n_init)])
    uv = np.mean([uvwlist[m]['xy'] for m in range(n_init)])
    uw = np.mean([uvwlist[m]['xz'] for m in range(n_init)])
    vw= np.mean([uvwlist[m]['yz'] for m in range(n_init)])
    a = np.mean([uvwlist[m]['a'] for m in range(n_init)])
    b = np.mean([uvwlist[m]['b'] for m in range(n_init)])
    c = np.mean([uvwlist[m]['c'] for m in range(n_init)])
    eu = np.std([uvwlist[m]['x'] for m in range(n_init)],ddof=1)
    ev = np.std([uvwlist[m]['y'] for m in range(n_init)],ddof=1)
    ew = np.std([uvwlist[m]['z'] for m in range(n_init)],ddof=1)
    euv = np.std([uvwlist[m]['xy'] for m in range(n_init)],ddof=1)
    euw = np.std([uvwlist[m]['xz'] for m in range(n_init)],ddof=1)
    evw= np.std([uvwlist[m]['yz'] for m in range(n_init)],ddof=1)
    ea = np.std([uvwlist[m]['a'] for m in range(n_init)],ddof=1)
    eb = np.std([uvwlist[m]['b'] for m in range(n_init)],ddof=1)
    ec = np.std([uvwlist[m]['c'] for m in range(n_init)],ddof=1)
    x = np.mean([xyzlist[m]['x'] for m in range(n_init)])
    y = np.mean([xyzlist[m]['y'] for m in range(n_init)])
    z = np.mean([xyzlist[m]['z'] for m in range(n_init)])
    xy = np.mean([xyzlist[m]['xy'] for m in range(n_init)])
    xz = np.mean([xyzlist[m]['xz'] for m in range(n_init)])
    yz= np.mean([xyzlist[m]['yz'] for m in range(n_init)])
    d = np.mean([xyzlist[m]['a'] for m in range(n_init)])
    e = np.mean([xyzlist[m]['b'] for m in range(n_init)])
    f = np.mean([xyzlist[m]['c'] for m in range(n_init)])
    ex = np.std([xyzlist[m]['x'] for m in range(n_init)],ddof=1)
    ey = np.std([xyzlist[m]['y'] for m in range(n_init)],ddof=1)
    ez = np.std([xyzlist[m]['z'] for m in range(n_init)],ddof=1)
    exy = np.std([xyzlist[m]['xy'] for m in range(n_init)],ddof=1)
    exz = np.std([xyzlist[m]['xz'] for m in range(n_init)],ddof=1)
    eyz= np.std([xyzlist[m]['yz'] for m in range(n_init)],ddof=1)
    ed = np.std([xyzlist[m]['a'] for m in range(n_init)],ddof=1)
    ee = np.std([xyzlist[m]['b'] for m in range(n_init)],ddof=1)
    ef = np.std([xyzlist[m]['c'] for m in range(n_init)],ddof=1)

        #Output all the particulars of the moving group at this timestep T.
    outfile.write("{0:8.1f}     {1:12.3f} {2:12.3f}  {3:12.3f} {4:12.3f}  {5:12.3f} {6:12.3f}   {7:12.4f} {8:12.4f}  {9:12.4f} {10:12.4f}  {11:12.4f} {12:12.4f}   {13:12.4f} {14:12.4f}  {15:12.4f} {16:12.4f}  {17:12.4f} {18:12.4f}\n".format(0,u,v,w,a,b,c,uv,uw,vw,x,y,z,d,e,f,xy,xz,yz))
    outfile.write("{0:8.1f}     {1:12.3f} {2:12.3f}  {3:12.3f} {4:12.3f}  {5:12.3f} {6:12.3f}   {7:12.4f} {8:12.4f}  {9:12.4f} {10:12.4f}  {11:12.4f} {12:12.4f}   {13:12.4f} {14:12.4f}  {15:12.4f} {16:12.4f}  {17:12.4f} {18:12.4f}\n".format(0,eu,ev,ew,ea,eb,ec,euv,euw,evw,ex,ey,ez,ed,ee,ef,exy,exz,eyz))

    outfile.close()


if __name__ ==  "__main__":
    traceback()
