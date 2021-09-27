#!/usr/bin/env python3
"""
Basic function to bind to pyrame. It implements the pyrame protocol to communicate with pyrame's modules.
For example, to use the function onearg  with test_onearg argument function of the cmd_test module listening on port localhost:9007::
       import bindpyrame
       bindpyrame.sendcmd("localhost",9007,"onearg_test","test_onearg")
       => (1, u'onearg(test_onearg)')
"""

import socket

PYRAME_PORTS_FILE="/opt/pyrame/ports.txt"


pyrame_ports_data={}
with open(PYRAME_PORTS_FILE) as f:
    for l in f.readlines():

        # remove comments and white spaces
        nl = l.split("#")[0].strip()

        # suppress white space
        
        if len(nl) > 0 :
            k,v = nl.split("=")
            pyrame_ports_data[k]=v

def get_port(name):
    """
    we expect name to be in capital
    """
    return pyrame_ports_data.get(name+"_PORT")
    
    
    


def sendcmd(host, port, cmd, *args):
    """
    Function that send a XML string to the pyrame module
    Args:
       host (str): the hostname running pyrame
       port (int): the port number of the module
       cmd (str): the command that the pyrame module will run
       *args (str): the arguments if needed to the command
    Returns:
        (tuple): Tuple containing:
            status(int): the status of request 1 if successful 0 otherwise
            result(str): a string containing the result.
    """
    command = "<cmd name=\"%s\">" % cmd
    for i in args:
        command += "<param>%s</param>" % i
    command += "</cmd>\n"

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = socket.gethostbyname(host)
        
        s.connect((ip,port))
        s.send(command.encode('utf-8'))
        data = ""
        while True:
            
            a = s.recv(1).decode('utf-8')
            data += a
            if a == "\n":
                break

        b = data.split("=")[1]
        retcode = b.split(">")[0]
        rawmsg = b.split(">")[1]
        rawmsg2 = rawmsg.split("[")[2]
        msg = rawmsg2.split("]")[0]
        return int(retcode.replace('"','')),msg
    
    except Exception as e:
        #    print(str(e))
        return 0, "BINDPYRAME_ERR"+str(e)
