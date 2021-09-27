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

class parse:
    """The constructor takes a conf_string and parses it into the properties: "name" and "params". The former is a string with the name of the module receiving the conf_string. The latter is a dictionary with each of the parameters and its values.
    
    The *conf_string* is of the form::
        module_name(parameter_list)
    
    *parameter_list* is of the form::
        param1=value1,param2=value2,param3=value3,etc.
    
    Values are either strings or conf_string's. For example::
        gpib(dst_addr=3,bus=tcp(host=10.220.0.3,port=2300),adapter_addr=0)"""
        
    def __init__(self,conf_string):
        self.name = ""
        self.params = {}
        # Extract name
        obj = conf_string.strip().split("(",1)
        if len(obj)<2:
            raise Exception("conf_string: error, must be of the form \"module_name(parameter_list)\"")
        self.name = obj[0]
        if obj[1][-1]!=")":
            raise Exception("conf_string: error, must end with closing paretheses \")\"")
        # The rest are parameters
        params = obj[1][0:-1]
        # Find the first level parentheses
        L1 = []
        counter = 0
        for i,c in enumerate(params):
            if c=="(":
                counter += 1
                if counter==1:
                    L1.append(i)
            if c==")":
                counter -= 1
                if counter==0:
                    L1.append(i)
        if counter!=0:
            raise Exception("conf_string: incorrect number of closing paretheses \")\"")
        # Go through the detected parentheses ranges, take only what's outside them and parse
        for i in range(len(L1)/2+1):
            params_chunk = ""
            if len(L1)==0: # when no parentheses are present 
                params_chunk = params
            elif i==0: # first chunk
                params_chunk = params[0:L1[2*i]]
            elif i==(len(L1)/2): # last chunk
                params_chunk = params[L1[2*i-1]+1:]
            else: # middle chunk
                params_chunk = params[L1[2*i-1]+1:L1[2*i]]
            #print ("params_chunk:%s"%(params_chunk))
            if params_chunk=="":
                continue
            params_split = params_chunk.strip(",").split(",")
            for j,param in enumerate(params_split):
                split_equal = param.split("=",1)
                if len(split_equal)<2:
                    raise Exception("conf_string: name of parameter and equal sign (=) not found")
                if j==len(params_split)-1 and i!=len(L1)/2:
                    # if last of params_split but not last params_chunk, it's a compound item
                    self.params[split_equal[0]] = split_equal[1]+params[L1[2*i]:L1[2*i+1]+1]
                    #print("self.params[\"%s\"] = %s"%(split_equal[0],self.params[split_equal[0]]))
                else:
                    self.params[split_equal[0]] = split_equal[1]
                    #print("self.params[\"%s\"] = %s"%(split_equal[0],self.params[split_equal[0]]))

    def has(self,*keys):
        return all(k in self.params.keys() for k in list(keys))

def unparse(conf):
    "Take a conf_string of class conf_strings.parse and convert to string"
    conf_string = "%s(" % (conf.name)
    first = True
    for k in conf.params:
        if not first:
            conf_string += ","
        else:
            first = False
        conf_string += "%s=%s" % (k,conf.params[k])
    conf_string += ")"
    # Parse it to be sure it doesn't contain errors
    parse(conf_string)
    return conf_string
