import numpy as np
from matplotlib.path import Path

def generate_points(x0,x1,dx,y0,y1,dy,z0,z1,dz):
    X = np.arange(x0, x1, dx)
    Y = np.arange(y0, y1, dy)
    Z = np.arange(z0, z1, dz)
    x, y, z = np.meshgrid(X, Y, Z)
    l = x.size
    return np.array([(i, j, k) for i, j, k in zip(x.reshape(l,), y.reshape(l,), z.reshape(l,))])

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

def generate_path(sizes, order):
    # order is a string containing the order of the scan xyz means scanning x then y then z
    # sizes contains the sizes for x,y,z
    map_string_to_index = {
        'x': 0,
        'y': 1,
        'z': 2
    }
    # order the sizes
    l = [sizes[map_string_to_index[d]] for d in order]

    coords = [[],[],[]]
    for p in range(l[0]*l[1]*l[2]):
        k = int(p / (l[0]*l[1]))
        j = int((p-k*l[1]*l[0]) / l[0])
        i = p - k*l[1]*l[0] - j*l[0]

        ti = i if (int(p / l[0]) % 2 == 0) else (l[0]-1 - i)
        tj = j if (int(p / (l[0]*l[1])) % 2 == 0) else (l[1]-1 - j)

        coords[0].append(ti)
        coords[1].append(tj)
        coords[2].append(k)
    new_coords = [[],[],[]]
    for i, j in enumerate([map_string_to_index[d] for d in order]):
        new_coords[j] = coords[i]
    return new_coords

def generate_path2(sizes, order):
    # order is a string containing the order of the scan xyz means scanning x then y then z
    # sizes contains the sizes for x,y,z
    map_string_to_index = {
        'x': 0,
        'y': 1,
        'z': 2
    }
    # order the sizes
    l = [sizes[map_string_to_index[d]] for d in order]
    coords = [[], [], []]
    f_asc = False
    m_asc = False
    for s in range(l[2]):
        m_asc = not m_asc
        for m in range(l[1]):
            f_asc = not f_asc
            for f in range(l[0]):
                coords[0].append(f if f_asc else l[0] - 1 - f)
                coords[1].append(m if m_asc else l[1] - 1 - m)
                coords[2].append(s)

    new_coords = [[],[],[]]
    for i, j in enumerate([map_string_to_index[d] for d in order]):
        new_coords[j] = coords[i]

    return np.array(new_coords).T



if __name__ == "__main__":
    # define a 2d polygone
    #points = np.array([[0., 0.],
    #                   [2., 2.],
    #                   [4., 0.],
    #                   [2.,-2.]])
    points = np.array([[25., 5.],
                       [27., 7.],
                       [29., 5.],
                       [27.,3.]])
    extrusion = [11, 13]
    steps = np.array([0.5, 0.5, 1])

    # precompute the data for generating the lattice
    x_min = np.min(points[:, 0])
    x_max = np.max(points[:, 0])
    y_min = np.min(points[:, 1])
    y_max = np.max(points[:, 1])

    print(x_min,x_max,y_min,y_max)

    origin = np.ndarray(3)
    origin[0:2] = points[0]
    origin[2] = extrusion[0]

    print(origin)
    nx = int((x_max - x_min) / steps[0]) + 1
    ny = int((y_max - y_min) / steps[1]) + 1
    nz = int((extrusion[1] - extrusion[0]) / steps[2]) + 1
    print("nb points",nx,ny,nz)

    raw_lattice = generate_path2([nx, ny, nz],'zxy')

    lattice = origin + raw_lattice*steps

    p = Path(points)
    for i,j in zip(lattice,raw_lattice):
        print("%20s %20s %6s %6s" % (str(i),str(j),
                                     str(p.contains_point(i[0:2], radius=0.05)),
                                     str(p.contains_point(i[0:2], radius=-0.05))))


    #print("Points")
    #
    #print(points)
    #for i in lattice:
    #    if p.contains_point(i[0:2]):
    #        print(i, "inside")
    #    else:
    #        print(i)


#origin = np.array([2.1,3.4,1.0])

#
#print(np.min(lattice[:,0]))
#print(np.max(lattice[:,0]))

#print(generate_path2([2,3,4],'xyz'))
#print(generate_path2([2,3,4],'zxy'))
#a=generate_path2([2,3,4],'xyz')
#b = a*np.array([0.1,0.5,1])#+np.array([3,4,5])
#print(b[1])
#for i in b:
#    print(i)