import bindpyrame
import sys
import types
import cmd
import os

PYRAME_PATH="/opt/pyrame"


# get the modules contained in ports.txt
def get_modules():

    filename=os.path.join(PYRAME_PATH,"ports.txt")
    if not os.path.exists(filename):
        print("%s does not exists" % filemane)
    with open(filename) as f:
        for i in f.readlines():
            if not i.startswith("#"):
                if  "=" in i:
                    mm = i.split("=")[0].replace("_PORT","").lower()
                    if os.path.exists(os.path.join(PYRAME_PATH,"cmd_%s.py" % mm)):
                        print("%-20s (%s)" %( mm,"cmd_%s.py" % mm))
                    

# class to interact with pyrame through bindpyrame.
class pyrame_module(object):

    # the __init__
    def __init__(self,module, pyr_id = False, pyrpath=PYRAME_PATH):

        self.pyrpath = pyrpath
        if not self.pyrpath in sys.path:
            sys.path.append(self.pyrpath)

        self.suffix = "_" + module
        # import the module if possible 
        try:
            self.pyr_module = __import__("cmd_"+module)
        except ImportError as e:
            raise ImportError("""You asked for %s but I couldn't find  cmd_%s.py  check that:
  you give the part  MODULE in the cmd_MODULE.py")
  the module is in %s""" % (module,module,pyrpath))
            

        self.pyr_port = int(bindpyrame.get_port(module.replace("cmd_","").replace(".py","").upper()))

        self.__pyr_id = pyr_id

        # create a list of functions to extend the instance of the class once the module has been loaded.
        # we remove the name of the module from the function names to make it simpler.
        self.imported_functions = []
        for i in dir(self.pyr_module):
            if not i.startswith("_"):
                if type(getattr(self.pyr_module,i)) == types.FunctionType:
                    self.imported_functions.append(i.replace(self.suffix,""))

    # ovverides the __getattr__ method to add the original pyrame module as a function of the 
    # class
    def __getattr__(self, attr):
        """
        
        """
        if attr in self.imported_functions:
            def to_run(*args):
                n_args = [attr + self.suffix]
                if self.__pyr_id:
                    n_args.append(self.__pyr_id)
                n_args.extend(args[:])
                return bindpyrame.sendcmd("localhost",
                                          self.pyr_port,
                                          *n_args)
            return to_run
            
        raise AttributeError("%r object has no attribute %r" %
                             (self.__class__.__name__, attr))

    # introspect the pyrame module
    def help(self):
        print("\nPyrame module : cmd%s (from file %s/cmd%s.py)\n" % (self.suffix,self.pyrpath,self.suffix))
        format="| %-20s | %-28s |   %-50s |" 
        print(format % ("internal functions","pyrame original function","arguments"))
        print("+"+22*"-"+"+"+30*"-"+"+"+54*"-"+ "+")
        for i in dir(self.pyr_module):
            if not i.startswith("_"):
                if type(getattr(self.pyr_module,i)) == types.FunctionType:
                    print(format % (i.replace(self.suffix,""),
                                    i,
                                    ", ".join(getattr(self.pyr_module,i).__code__.co_varnames)))

                    # should add the functions of the original module to the instance of the class
                    #setattr(self, i,getattr(self.pyr_module,i))
        print("\n")
    
    # function to call pyrame from the command line to use with cmd.CMD
    # typically to call a function (here get_pressure") from a module with a pressure_id (here mesvide) initialized by 
    #        pressure = pyrame_module("pf_tpg300")
    # one need to type  
    #        print(pressure.e("get_pressure","mesvide"))
    # while using the __getatr__ rewrite
    #        print(pressure.get_pressure("mesvide"))
    # Note that we use the name of the function without the name of the module. 
    def e(self,*args):
        n_args = [args[0]+self.suffix]
        if self.__pyr_id:
            n_args.append(self.__pyr_id)
        n_args.extend(args[1:])

        return bindpyrame.sendcmd("localhost",
                                  self.pyr_port,
                                  *n_args)

    # this use directly bind pyrame and one needs to pass ALL the arguments
    # HOST, MODULE_PORT, FUNCTION NAME, ARGS,....
    def raw_e(self,*args):
        return bindpyrame.sendcmd(*args)

    # properties
    # the pyr_id is the usually first argument of the function to identify the device on the bus
    def get_pyr_id(self):
        return self.__pyr_id

    def set_pyr_id(self,vid):
        self.__pyr_id = vid
    
    pyr_id = property(get_pyr_id, set_pyr_id)


# the cmd.Cmd object to interact
class pyrame_module_interactor(cmd.Cmd):
    pyr_modules={}
    prompt = "pyr_interact> "

    # utility function
    def warn(self,m):
        print("module %s is not initialized" % m)
        print("list of modules: %s" % ", ".join(self.pyr_modules.keys()))

    def g(self,line):
        return line.split()
 
    # get availaible modules
    def do_list_modules(self,line):
        get_modules()

    def help_list_modules(self):
        print("list all the available modules extracted from the ports.txt file of pyrame")



    # initialize the connection to the pyrame module
    def do_initialize_pyrame_module(self,line):
        args = self.g(line)
        if len(args) == 2:
            try:
                self.pyr_modules[args[0]] =  pyrame_module(args[1],args[0])
            except Exception as e:
                print(e)

    def help_initialize_pyrame_module(self):
        print("""

load the helper function to connect with pyrame original module
arguments are:
   - internal name (the name you will use to interact with the module )
   - pyrame module

Note that in this case the pyrame identifier which is mandatory for all commands is the same 
as the internal name and is automatically added to the command. 

For example to use the pump driven by the cmd_pf_tc110 module

   ipm mypump pf_tc110 

Then the following command will use mypump to perform action

   info mypump

to execute a pyrame command

   mypump get_rpm

Remember that a normal call to pyrame would look like

  localhost pyrame_port function_name pyrame_id function_args

here we only give

  pyrame_id function_name function_args

""")

    # Shortcuts 
    def do_ipm(self,line):
        self.do_initialize_pyrame_module(line)

    def help_ipm(self):
        self.help_initialize_pyrame_module()
         


    # info command
    def do_info(self,line):
        d = self.pyr_modules.get(line)
        if d:
            d.help()
        else:
            self.warn(line)
                        
    #shortcut for info
    def do_i(self,line):
        self.do_info(line)

    def default(self,line):
        args = self.g(line)
        if args[0] in self.pyr_modules.keys():
            #print("Calling %s with args %s"% (args[0],", ".join(args[1:])))
            r,v = self.pyr_modules[args[0]].e(*args[1:])
            if r:
                print(v)
            else:
                print("ERR: %s" % v)
        else:
            self.warn(args[0])

    def emptyline(self):
        pass


    def do_EOF(self, line):
        return True




if __name__ == "__main__":

    interactor_mode=True
    if interactor_mode:
        pyrame_module_interactor().cmdloop()
    else:
        pressure = pyrame_module("pf_tpg300")
        
        print("using method e")
        print(pressure.e("get_pressure","mesvide"))
        print("using method raw_e")
        print(pressure.raw_e("localhost",pressure.pyr_port,"get_pressure_pf_tpg300","mesvide"))
        print("using __getattr__")
        print(pressure.get_pressure("mesvide"))
        
        pressure.pyr_id = "mesvide"
        pressure.help()
        
        pump = pyrame_module("pf_tc110")
        pump.pyr_id = "pump"
        pump.help()
        print("RPM: %d " % int(pump.get_rpm()[1]))
        print("Temp: %d" % int(pump.get_motor_temp()[1]))
        print("Operating hours: %d" % int(pump.get_operating_hours()[1]))
        
        valve = pyrame_module("dio_ki_6517")
        valve.pyr_id = "valve"
        valve.help()
        

