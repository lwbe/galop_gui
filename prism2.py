#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# 
# Copyright 2012-2017 Frédéric Magniette, Miguel Rubio-Roy
# This file is part of Pyrame.
# 
# Pyrame is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Pyrame is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrame.  If not, see <http://www.gnu.org/licenses/>
from matplotlib.path import Path

TEST_GLOBAL = None

def init_prism(face_to_extrude, axis_to_extrude, start, end):
    global TEST_GLOBAL
    print("in init_prism TEST_GLOBAL: ", TEST_GLOBAL)
    TEST_GLOBAL="set"

    max_coord = [None,None,None]
    min_coord = [None,None,None]
    
    c2 = ["x","y","z"].index(axis_to_extrude)
    face_axis = [0,1,2]
    face_axis.remove(c2)

    max_coord[c2] = max(float(start),float(end))
    min_coord[c2] = min(float(start),float(end))

    c0, c1 = face_axis
    coord_c0 =[]
    coord_c1 = []
    # extract the points from the face_to_extrude
    for i in face_to_extrude.split(";")[:-1]:
        p0,p1 = [float(j) for j in i.split(",")]
        #polygone_points.append((point[c0], point[c1]))
        coord_c0.append(p0)
        coord_c1.append(p1)

    max_coord[c0] = max(coord_c0)
    min_coord[c0] = min(coord_c0)
    max_coord[c1] = max(coord_c1)
    min_coord[c1] = min(coord_c1)
                                
    volume = {
        "polygone": face_to_extrude,
        "axis_to_extrude": axis_to_extrude,
        "axis_to_extrude_index": c2,
        "extrusion_max" : max_coord[c2],
        "extrusion_min" : min_coord[c2],
        "c0": c0,
        "c1": c1,
        "c2": c2,
        # necessaire pour cmd_motion
        "max_0" : max_coord[0],
        "min_0" : min_coord[0],
        "max_1" : max_coord[1],
        "min_1" : min_coord[1],
        "max_2" : max_coord[2],
        "min_2" : min_coord[2],        
    }
    return volume

def prism(volume,errors,point):
    global TEST_GLOBAL
    print("in prism TEST_GLOBAL: ", TEST_GLOBAL)
    
    c0 = volume["c0"]
    c1 = volume["c1"]
    c2 = volume["c2"]

    
    # on teste si on est bien dans la zone le long de l'axe d'extrusion
    if not (volume["extrusion_min"] <= point[c2]  <= volume["extrusion_max"]) :
        return False

    # sinon on crée le polygone
    poly_coords = []
    for i in volume["polygone"].split(";")[:-1]:
        poly_coords.append([float(j) for j in i.split(",")])


    polygone = Path(poly_coords)

    poly_points = (point[c0], point[c1])
    if polygone.contains_point(poly_points, radius=0.05) or polygone.contains_point(poly_points, radius=-0.05):
        return True
    else:
        return False
