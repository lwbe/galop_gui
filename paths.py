import numpy as np


def generate_points(x0,x1,dx,y0,y1,dy,z0,z1,dz):
    X = np.arange(x0,x1,dx)
    Y = np.arange(y0,y1,dy)
    Z = np.arange(z0,z1,dz)
    x, y, z = np.meshgrid(X,Y,Z)
    l = x.size
    return np.array([(i,j,k) for i,j,k in zip(x.reshape(l,),y.reshape(l,),z.reshape(l,))])

def generate_points2(x0,x1,dx,y0,y1,dy,z0,z1,dz):
    nx = int((10*x1-10*x0)/(10.*dx))+1
    ny = int((10*y1-10*y0)/(10.*dy))+1
    nz = int((10*z1-10*z0)/(10.*dz))+1
    X = np.linspace(x0,x1,nx)
    Y = np.linspace(y0,y1,ny)
    Z = np.linspace(z0,z1,nz)
    x, y, z = np.meshgrid(X,Y,Z)
    l = x.size
    return np.array([(i,j,k) for i,j,k in zip(x.reshape(l,),y.reshape(l,),z.reshape(l,))])

