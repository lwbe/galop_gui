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

import os

def load_api(pyres):
    script_filename=pyres[1]
    #print("script_filename=%s"%(script_filename))
    api_file=os.path.splitext(script_filename)[0]+".api"
    with open(api_file,"r") as api_file:
        api = api_file.read().replace("\n",";")
    return api
