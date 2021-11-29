import numpy as np
import sys
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

def generate_path2(sizes, order,path_type):
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
    if path_type[0] == "r":
        f_asc = False
    else:
        f_asc = True
    if path_type[1] == "r":
        m_asc = False
    else:
        m_asc = True
    for s in range(l[2]):
        if path_type[0] == "r":
            m_asc = not m_asc
        for m in range(l[1]):
            if path_type[0] == "r":
                f_asc = not f_asc
            for f in range(l[0]):
                coords[0].append(f if f_asc else l[0] - 1 - f)
                coords[1].append(m if m_asc else l[1] - 1 - m)
                coords[2].append(s)

    new_coords = [[],[],[]]
    for i, j in enumerate([map_string_to_index[d] for d in order]):
        new_coords[j] = coords[i]

    return np.array(new_coords).T



def generate_path_3(points,extrusion,steps,path_order,path_type,path_direction):
    x_min = np.min(points[:, 0])
    x_max = np.max(points[:, 0])
    y_min = np.min(points[:, 1])
    y_max = np.max(points[:, 1])

    coords=[(x_min,x_max),(y_min,y_max),extrusion]

    nb_steps = [int((10*c[1]-10*c[0])/(10.*s))+1 for c,s in zip(coords,steps)]

    poly_path = Path(points)

    map_string_to_index = {
        'x': 0,
        'y': 1,
        'z': 2
    }
    # order the sizes
    l = [map_string_to_index[d] for d in path_order]
    print("l: ",l)
    f_asc = True
    m_asc = True
    s_asc = True
    points_in_path = []

    if s_asc:
        s_values = np.linspace(coords[l[2]][0], coords[l[2]][1], nb_steps[l[2]])
    else:
        s_values = np.linspace(coords[l[2]][1], coords[l[2]][0], nb_steps[l[2]])
    if path_type[0] == "r":
        s_asc = not s_asc
    for s in s_values:
        if m_asc:
            m_values = np.linspace(coords[l[1]][0], coords[l[1]][1], nb_steps[l[1]])
        else:
            m_values = np.linspace(coords[l[1]][1], coords[l[1]][0], nb_steps[l[1]])
        if path_type[0] == "r":
            m_asc = not m_asc

        for m in m_values:
            if f_asc:
                f_values = np.linspace(coords[l[0]][0], coords[l[0]][1], nb_steps[l[0]])
            else:
                f_values = np.linspace(coords[l[0]][1], coords[l[0]][0], nb_steps[l[0]])
            if path_type[1] == "r":
                f_asc = not f_asc

            for f in f_values:

                p = [0,0,0]
                p[l[0]] = f
                p[l[1]] = m
                p[l[2]] = s
                print(p)
                if poly_path.contains_point(p[0:2], radius=0.05) or poly_path.contains_point(p[0:2], radius=-0.05):
                    points_in_path.append(p)

    return np.array(points_in_path)

def generate_path_4(points,extrusion,steps,path_order,path_type,path_direction):
    x_min = np.min(points[:, 0])
    x_max = np.max(points[:, 0])
    y_min = np.min(points[:, 1])
    y_max = np.max(points[:, 1])

    coords = [(x_min,x_max),(y_min,y_max),extrusion]

    nb_steps = [int((10*c[1]-10*c[0])/(10.*s))+1 for c,s in zip(coords,steps)]

    poly_path = Path(points)

    map_string_to_index = {
        'x': 0,
        'y': 1,
        'z': 2
    }
    # order the sizes
    points_in_path={}
    for s in np.linspace(coords[0][0], coords[0][1], nb_steps[0]):
        for m in np.linspace(coords[1][0], coords[1][1], nb_steps[1]):
            if poly_path.contains_point((s,m), radius=0.05) or poly_path.contains_point((s,m), radius=-0.05):
                if points_in_path.get(s):
                    points_in_path[s].append(m)
                else:
                    points_in_path[s]=[m]
    all_points = []
    w_p = False
    x_p = False
    for k,v in points_in_path.items():
        nv = sorted(v)
        if w_p:
            nv = nv[::-1]
        if path_type[0] == "m":
            w_p= not w_p
        print("v=",v,nv)
        for w in nv:
            if x_p:
                nx = np.linspace(coords[2][0], coords[2][1], nb_steps[2])
            else:
                nx = np.linspace(coords[2][1], coords[2][0], nb_steps[2])
            if path_type[1] == "m":
                x_p = not x_p
            for x in nx:
                all_points.append((k,w,x))

    return np.array(all_points)


if __name__ == "__main__":
    # define a 2d polygone
    points = np.array([[0., 10.],
                       [2., 12.],
                       [4., 10.],
                       [2.,8.]])
    #points = np.array([[25., 5.],
    #                   [27., 7.],
    #                   [29., 5.],
    #                   [27.,3.]])
    extrusion = [20, 24]
    steps = np.array([4, 4, 4])

    # precompute the data for generating the lattice
    steps = [1,1,1]
    #pp = generate_path_3(points,extrusion,steps,'xyz','rr','ppp')
    pp = generate_path_4(points,extrusion,steps,'xyz','mm','ppp')

    x=pp[:,0]
    y=pp[:,1]
    z=pp[:,2]

    import matplotlib as mpl
    from mpl_toolkits.mplot3d import Axes3D
    import numpy as np
    import matplotlib.pyplot as plt
    mpl.rcParams['legend.fontsize'] = 10

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
    #z = np.linspace(-2, 2, 100)
    #r = z**2 + 1
    #x = r * np.sin(theta)
    #y = r * np.cos(theta)
    ax.plot(x, y, z,"o-", label='parametric curve')

    #plt.show()
    #sys.exit(0)

    points = np.array([[0., 8.],
                       [4., 8.],
                       [4., 12.],
                       [0.,12.]])

    pp = generate_path_4(points,extrusion,steps,'xyz','mm','ppp')
    #pp = generate_path_3(points,extrusion,steps,'zxy','rr','ppp')
    print(pp.shape)
    x=pp[:,0]
    y=pp[:,1]
    z=pp[:,2]
    ax.plot(x, y, z,"x-")
    ax.legend()

    plt.show()

    sys.exit(0)



    print(x_min,x_max,y_min,y_max)

    origin = np.ndarray(3)
    origin[0:2] = points[0]
    origin[2] = extrusion[0]

    print(origin)
    nx = int((x_max - x_min) / steps[0]) + 1
    ny = int((y_max - y_min) / steps[1]) + 1
    nz = int((extrusion[1] - extrusion[0]) / steps[2]) + 1
    print("nb points",nx,ny,nz)

    raw_lattice = generate_path2([nx, ny, nz],'xyz',"rr")

    lattice = origin + raw_lattice*steps

    p = Path(points)
    for i,j in zip(lattice,raw_lattice):
        print("%20s %20s %6s %6s" % (str(i),str(j),
                                     str(p.contains_point(i[0:2], radius=0.05)),
                                     str(p.contains_point(i[0:2], radius=-0.05))))


    #print("Points")
    #
    #print(points)import matplotlib as mpl
    from mpl_toolkits.mplot3d import Axes3D
    import numpy as np


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
