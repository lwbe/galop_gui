# the return value of init_prism is a dictionnary contaning information to be passed to the function.

def init_prism(face_to_extrude, axis_to_extrude, start, end):
    volume = {
        "polygone": face_to_extrude,
        "extrusion_axis": axis_to_extrude,
        "extrusion_min": min(start, end),
        "extrusion_max": max(start, end)
        }
    return volume

def prism(volume,errors,point):
    extrusion_axis = volume["extrusion_axis"]
    if extrusion_axis == "x":
        c0, c1, c2 = 1, 2, 0
    elif extrusion_axis == "y":
        c0, c1, c2 = 2, 0, 1
    elif extrusion_axis == "z":
        c0, c1, c2 = 0, 1, 2

    # on teste si on est bien dans la zone le long de l'axe d'extrusion
    if not (volume["extrusion_min"] <= point[c2]  <= volume["extrusion_max"]) :
        return False

    # sinon on crée le polygone
    poly_coords = []
    for i in args[4].split(";")[:-1]:
        poly_coords.append([float(j) for j in i.split(",")])


    polygone = Path(poly_coords)
    poly_points = (point[c0], point[c1])
    if polygone.contains_point(poly_points, radius=0.05) or polygone.contains_point(poly_points, radius=-0.05):
        return True
    else:
        return False