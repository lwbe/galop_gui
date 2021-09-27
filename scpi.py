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

import time
import pools, getapi, conf_strings

try:
    from __main__ import submod
except:
    pass

# CLASS ##########################################################

class scpi(object):
    def __init__(self,module_name):
        self.module_name=module_name
        self.scpi_pool=pools.pool(module_name)

    def init(self,scpi_id,conf_string):
        try:
            conf=conf_strings.parse(conf_string)
        except Exception as e:
            return 0,str(e)
        if conf.name!=self.scpi_pool.name:
            return 0,"Invalid module name %s in conf_string. Should be %s"%(conf.name,self.scpi_pool.name)
        if not conf.has("bus"):
            return 0,"Missing bus parameter in conf_string"
        if not conf.has("chan"):
            if len(self.channels)>1:
                return 0,"Missing chan parameter in conf_string"
            else:
                channel=self.channels[0]
        else:
            channel=conf.params["chan"]
        if channel not in self.channels:
            return 0,"Invalid chan in conf_string"
        try:
            conf_bus=conf_strings.parse(conf.params["bus"])
        except Exception as e:
            return 0,str(e)
        # Initialize link
        bus_id="bus_%s"%(scpi_id)
        retcode,res=submod.execcmd("init@"+conf_bus.name,bus_id,conf.params["bus"])
        if retcode==0:
            return 0,"Error initializing link <- %s"%(res)
        # Add to the pool
        self.scpi_pool.new(scpi_id,{"bus":conf_bus.name,"bus_id":bus_id,"channel":channel})
        return 1,"ok"

    def deinit(self,scpi_id):
        try:
            scpi=self.scpi_pool.get(scpi_id)
        except Exception as e:
            return 1,str(e)
        # Deinitialize link
        retcode,res=submod.execcmd("deinit@"+scpi["bus"],scpi["bus_id"])
        if retcode==0:
            return 0,"Error deinitializing link %s <- %s"%(scpi["bus_id"],res)
        # Remove scpi from the pool
        try:
            self.scpi_pool.remove(scpi_id)
        except Exception as e:
            return 0,str(e)
        return 1,"ok"

    def config(self,scpi_id,command="",cmd_delay=0):
        try:
            scpi=self.scpi_pool.get(scpi_id)
        except Exception as e:
            return 0,str(e)
        if "configured" in scpi:
            return 1,"already configured"
        # Configure link
        retcode,res=submod.execcmd("config@"+scpi["bus"],scpi["bus_id"])
        if retcode==0:
            return 0,"Error configuring link <- %s"%(res)
        scpi["cmd_delay"]=float(cmd_delay)
        # Optional configuration commands
        if command!="" and command!="undef":
            retcode,res=submod.execcmd("write@"+scpi["bus"],scpi["bus_id"],command+r"\n")
            if retcode==0:
                self.inval(scpi_id)
                return 0,"Error writing to link <- %s"%(res)
        scpi["configured"]=1
        return 1,"ok"

    def inval(self,scpi_id):
        try:
            scpi=self.scpi_pool.get(scpi_id)
        except Exception as e:
            return 0,str(e)
        if "configured" not in scpi:
            return 1,"not configured"
        # Invalidate link
        retcode,res=submod.execcmd("inval@"+scpi["bus"],scpi["bus_id"])
        if retcode==0:
            return 0,"Error configuring link <- %s"%(res)
        del scpi["cmd_delay"]
        del scpi["configured"]
        return 1,"ok"

    def simple_query(self,scpi_id,query):
        try:
            scpi=self.scpi_pool.get(scpi_id)
        except Exception as e:
            return 0,str(e)
        # Send the command
        response=""
        qy=query.format(channel=scpi["channel"])
        retcode,res=self.send_query(scpi,qy)
        if retcode==0:
            return 0,res
        response+=res+";"
        return 1,response[:-1]

    def simple_command(self,scpi_id,command):
        try:
            scpi=self.scpi_pool.get(scpi_id)
        except Exception as e:
            return 0,str(e)
        # Send the command
        cmd=command.format(channel=scpi["channel"])
        return self.send_command(scpi,cmd)

    def free_command(self,scpi_id,command):
        try:
            scpi=self.scpi_pool.get(scpi_id)
        except Exception as e:
            return 0,str(e)
        return self.send_command(scpi,command)

    def free_query(self,scpi_id,query):
        try:
            scpi=self.scpi_pool.get(scpi_id)
        except Exception as e:
            return 0,str(e)
        return self.send_query(scpi,query)

    def reset(self,scpi_id):
        try:
            scpi=self.scpi_pool.get(scpi_id)
        except Exception as e:
            return 0,str(e)
        command="*RST"
        return self.send_command(scpi,command)

    def set_param(self,scpi_id,name,value):
        try:
            scpi=self.scpi_pool.get(scpi_id)
        except Exception as e:
            return 0,str(e)
        scpi[name]=value
        return 1,"ok"

    def get_param(self,scpi_id,name):
        try:
            scpi=self.scpi_pool.get(scpi_id)
        except Exception as e:
            return 0,str(e)
        return 1,scpi[name]

    def set_fw_version(self,scpi_id,fw_version):
        return self.set_param(scpi_id,"fw_version",fw_version)

    def get_fw_version(self,scpi_id):
        return self.get_param(scpi_id,"fw_version")

    def set_voltage(self,scpi_id,voltage,command):
        try:
            scpi=self.scpi_pool.get(scpi_id)
        except Exception as e:
            return 0,str(e)
        # Check parameters
        if voltage=="undef":
            return 1,"Did nothing !"
        # Send the command
        if "current_limit"+scpi["channel"] not in scpi:
            return 0,"Set current limit first"
        current=scpi["current_limit"+scpi["channel"]]
        voltage=float(voltage)
        cmd=command.format(channel=scpi["channel"],current=current,voltage=voltage)
        retcode,res=self.send_command(scpi,cmd)
        if retcode==0:
            return 0,"Error setting voltage on channel %s: %s"%(scpi["channel"],res)
        return 1,"ok"

    def set_current(self,scpi_id,current,command):
        try:
            scpi=self.scpi_pool.get(scpi_id)
        except Exception as e:
            return 0,str(e)
        # Check parameters
        if current=="undef":
            return 1,"Did nothing !"
        # Send the command
        if "voltage_limit"+scpi["channel"] not in scpi:
            return 0,"Set voltage limit first"
        voltage=scpi["voltage_limit"+scpi["channel"]]
        current=float(current)
        cmd=command.format(channel=scpi["channel"],current=current,voltage=voltage)
        retcode,res=self.send_command(scpi,cmd)
        if retcode==0:
            return 0,"Error setting current on channel %s: %s"%(scpi["channel"],res)
        return 1,"ok"

    def set_voltage_limit(self,scpi_id,voltage_limit,command):
        try:
            scpi=self.scpi_pool.get(scpi_id)
        except Exception as e:
            return 0,str(e)
        # Check parameters
        if voltage_limit=="undef":
            return 1,"Did nothing !"
        voltage_limit=float(voltage_limit)
        # Send the command
        cmd=command.format(channel=scpi["channel"],voltage_limit=voltage_limit)
        retcode,res=self.send_command(scpi,cmd)
        if retcode==0:
            return 0,"Error setting voltage limit on channel %s: %s"%(scpi["channel"],res)
        scpi["voltage_limit"+scpi["channel"]]=voltage_limit
        return 1,"ok"

    def set_current_limit(self,scpi_id,current_limit,command):
        try:
            scpi=self.scpi_pool.get(scpi_id)
        except Exception as e:
            return 0,str(e)
        # Check parameters
        if current_limit=="undef":
            return 1,"Did nothing !"
        current_limit=float(current_limit)
        # Send the command
        cmd=command.format(channel=scpi["channel"],current_limit=current_limit)
        retcode,res=self.send_command(scpi,cmd)
        if retcode==0:
            return 0,"Error setting current limit on channel %s: %s"%(scpi["channel"],res)
        scpi["current_limit"+scpi["channel"]]=current_limit
        return 1,"ok"

    def measure(self,scpi_id,range,resolution,conf_command,measure_command):
        try:
            scpi=self.scpi_pool.get(scpi_id)
        except Exception as e:
            return 0,str(e)
        # Send the command
        if conf_command not in ["","undef"]:
            cmd=conf_command.format(channel=scpi["channel"],range=range,resolution=resolution)
            if not ("last_measure_conf"+scpi["channel"] in scpi and scpi["last_measure_conf"+scpi["channel"]]==cmd):
                retcode,res=self.send_command(scpi,cmd)
                if retcode==0:
                    return 0,"Error configuring measurement on channel %s: %s"%(scpi["channel"],res)
                scpi["last_measure_conf"+scpi["channel"]]=cmd
        cmd=measure_command.format(channel=scpi["channel"],range=range,resolution=resolution)
        print("cmd=%s"%(cmd))
        retcode,res=self.send_query(scpi,cmd)
        if retcode==0:
            return 0,"Error performing measurement on channel %s: %s"%(scpi["channel"],res)
        return 1,res

    def get_error_queue(self,scpi_id):
        try:
            scpi=self.scpi_pool.get(scpi_id)
        except Exception as e:
            return 0,str(e)
        if "configured" not in scpi:
            return 0,"not configured"
        return self.get_errors(scpi)

    #################
    # INTERNAL FUNCTIONS (do not take scpi_id)
    #################

    def get_errors(self,scpi):
        command="SYST:ERR?"
        errors=""
        while True:
            time.sleep(0.005)
            retcode,res=submod.execcmd("wrnrd_until@"+scpi["bus"],scpi["bus_id"],command+r"\n",r"\n")
            if retcode==0:
                return 0,res
            try:
                if int(res.split(",",1)[0])!=0:
                    errors += res if errors=="" else "; "+res
                else:
                    break
            except Exception as e:
                return 0,"Read wrong response while getting error queue: %s"%(res)
        return 1,errors

    def send_command(self,scpi,command):
        if "configured" not in scpi:
            return 0,"not configured"
        if command=="":
            return 1,"ok"
        if scpi["cmd_delay"]!=0:
            command=command.split(r"\n")
        else:
            command=[command]
        for cmd in command:
            retcode,res=submod.execcmd("write@"+scpi["bus"],scpi["bus_id"],cmd+r"\n")
            if retcode==0:
                return 0,"Error writing to link <- %s"%(res)
            if scpi["cmd_delay"]!=0:
                time.sleep(scpi["cmd_delay"])
        return 1,"ok"

    def send_query(self,scpi,query):
        if "configured" not in scpi:
            return 0,"not configured"
        if scpi["cmd_delay"]!=0:
            query=query.split(r"\n")
        else:
            query=[query]
        for i,q in enumerate(query):
            if i!=len(query)-1: # previous commands
                retcode,res=submod.execcmd("write@"+scpi["bus"],scpi["bus_id"],q+r"\n")
            else: # the final query command
                retcode,res=submod.execcmd("wrnrd_until@"+scpi["bus"],scpi["bus_id"],q+r"\n",r"\n")
            if retcode==0:
                return 0,"Error querying link <- %s"%(res)
            # cmd_delay is a delay to be applied between commands
            if scpi["cmd_delay"]!=0:
                time.sleep(scpi["cmd_delay"])
        return 1,res

    def check_range(self,range,ranges=[]):
        range=range.lower()
        if range not in ["auto","min","max"]:
            try:
                if ranges!=[] and float(range) not in ranges:
                    raise Exception()
            except:
                return 0,"Invalid range. Valid values are: " + " ".join(map(str,ranges))
        if range in ["auto"]:
            return 1,None
        return 2,range

    def check_resolution(self,resolution,units):
        resolution=resolution.lower()
        if resolution.endswith(units):
            resolution=resolution[:-len(units)]
            retcode=2 # with units
        else:
            retcode=3 # without units
        if resolution not in ["max","min"]:
            try:
                float(resolution)
            except:
                return 0,"Invalid resolution"
        else:
            # make it equivalent to "with units"
            # so that "max"/"min" refer to maximum/minimum resolution
            # e.g: maximum/minimum number of PLC integration
            retcode=2
        return retcode,resolution

