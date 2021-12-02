import numpy as np
import sys
from matplotlib.path import Path


def generate_points(x0,x1,dx,y0,y1,dy,z0,z1,dz):
    nx = int((10*x1-10*x0)/(10.*dx))+1
    ny = int((10*y1-10*y0)/(10.*dy))+1
    nz = int((10*z1-10*z0)/(10.*dz))+1
    X = np.linspace(x0,x1,nx)
    Y = np.linspace(y0,y1,ny)
    Z = np.linspace(z0,z1,nz)
    x, y, z = np.meshgrid(X,Y,Z)
    l = x.size
    return np.array([(i,j,k) for i,j,k in zip(x.reshape(l,),y.reshape(l,),z.reshape(l,))])

def generate_path(poly_points, extrusion_axis, extrusion_limits, steps, path_order, path_type, path_directions):
    #map_string_to_index = {'x': 0, 'y': 1, 'z': 2}

    # l'axe d'extrusion définit le polygone (orthogonal à l'axe d'extrusion)
    if extrusion_axis == "x":
        c0, c1, c2 = 1, 2, 0
    elif extrusion_axis == "y":
        c0, c1, c2 = 2, 0, 1
    elif extrusion_axis == "z":
        c0, c1, c2 = 0, 1, 2

    order_i = [int(i)-1 for i in path_order]
    # le volume à scanner est un polyèdre défini par un polygone extrudé suivant une direction.
    # par construction les coordonées x,y correspondent au polygone et la coordonnees z à l'extrusion

    # on commence par définir le volume englobant le polygone, c'est à dire la phase à extruder.
    # les données sont un polygone 2D
    x_min = np.min(poly_points[:, 0])
    x_max = np.max(poly_points[:, 0])
    y_min = np.min(poly_points[:, 1])
    y_max = np.max(poly_points[:, 1])

    # on va utiliser matplotlib pour caculer les points dans le polygone
    polygone = Path(poly_points)

    # on calcule le nombre de pas dans toute les directions
    coords = [(x_min, x_max), (y_min, y_max), extrusion_limits]
    nb_steps = [int((10 * c[1] - 10 * c[0]) / (10. * s)) + 1 for c, s in zip(coords, steps)]

    # on crée le nuage de points et on récupére ceux qui sont dans la
    # zone de mesure.
    inside_points = []

    for x in np.linspace(coords[0][0], coords[0][1], nb_steps[0]):
        for y in np.linspace(coords[1][0], coords[1][1], nb_steps[1]):
            for z in np.linspace(coords[2][0], coords[2][1], nb_steps[2]):
                point = [x, y, z]
                poly_points = (point[c0], point[c1])

                if polygone.contains_point(poly_points, radius=0.05) or polygone.contains_point(poly_points, radius=-0.05):
                    inside_points.append(point)

    # on definit si on scan en croissant ou en decroissant
    s_factor = 1 if path_directions[0] == "p" else -1
    m_factor = 1 if path_directions[1] == "p" else -1
    f_factor = 1 if path_directions[1] == "p" else -1
    a = np.array(inside_points)
    all_points = []
    
    s = sorted(set(a[:, order_i[2]]))
    sv = s if s_factor == 1 else reversed(s)
    for s in sv:
        b = a[np.where(a[:, order_i[2]] == s)]

        m = sorted(set(b[:, order_i[1]]))
        mv = m if m_factor == 1 else reversed(m)
        for m in mv:
            c = b[np.where(b[:, order_i[1]] == m)]
        
            f = sorted(set(c[:, order_i[0]]))
            fv = f if f_factor == 1 else reversed(f)
            for f in fv:
                all_points.append(c[np.where(c[:,order_i[0]] == f)][0])
            # on inverse l'ordre de scan si on fait des meandres
            if path_type[0] == "m":
                f_factor *= -1
        if path_type[1] == "m":
            m_factor *= -1

    return np.array(all_points)

def generate_path_pyrame(poly_points, extrusion_axis, extrusion_limits, steps, path_order, path_type, path_directions):
    path = generate_path(poly_points, extrusion_axis, extrusion_limits, steps, path_order, path_type, path_directions)
    print(path.shape,path[:,0])
    return len(path),";".join(["%s,%s,%s" % (p[0], p[1], p[2]) for p in path])


if __name__ == "__main__":
    import matplotlib as mpl
    from mpl_toolkits.mplot3d import Axes3D
    import numpy as np
    import matplotlib.pyplot as plt
    mpl.rcParams['legend.fontsize'] = 10

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")


    # define a 2d polygone
    points = np.array([[0., 10.],
                       [2., 12.],
                       [4., 10.],
                       [2.,8.]])
    extrusion = [20, 24]
    steps = np.array([4, 4, 4])


    steps = [1, 1, 1]
    print(generate_path_pyrame(points, "z", extrusion, steps, '321', 'mm', 'ppp'))
    pp = generate_path(points, "z", extrusion, steps, '321', 'mm', 'ppp')

    x = pp[:, 0]
    y = pp[:, 1]
    z = pp[:, 2]

    ax.plot(x, y, z, "x-", label="zxy")

    pp = generate_path(points, "z", extrusion, steps, '321', 'rr', 'ppp')

    x = pp[:, 0]
    y = pp[:, 1]
    z = pp[:, 2]
    ax.plot(x, y, z, "o-", label="zxy")

    ax.legend()
    plt.show()

