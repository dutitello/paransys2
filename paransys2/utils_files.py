"""
Useful functions for files

"""
import re
import os
import shutil
import paransys2.utils as utils

def copy_model(self, parameters):
    """
    Copy model files. 
    
    Script files are filtered looking for some commands and parameters, binary files are just coppied.

    Args:
        parameters (dict): analysis parameters that PARANSYS will change if it's a script
    """

    modelfiles = [self._model['main']] + self._model['extrafiles']
    destination = self._ANSYS['run_location']

    for fname in modelfiles:
        fname = '{}\\{}'.format(self._model['location'], fname)
        try:
            f = open(fname, 'r')
            f.close()
        except:
            utils.messages.cerror(self, f'PARANSYS couldn\'t copy \"{fname}\".')
        else:
            if is_text_file(fname) and len(parameters) > 0:
                copy_and_filter_scripts(fname, destination, parameters)
            else:
                shutil.copy(fname, destination)

    fname = f'{destination}\\main.paransys'
    with open(fname, 'w+') as f:
        inpstr = '/INPUT,{}'.format(self._model['main'])
        f.write(inpstr)


def copy_and_filter_scripts(fname, destination, parameters):
    """
    Copy model scripts filtering some commands and parameters.

    Args:
        fname (str): source script file
        destination (str): destionation folder
        parameters (dict): analysis parameters that PARANSYS will change

    Raises:
        RuntimeError: [description]
    """

    # Keys for simple lines
    # Commands that assigns values to variables in the form "command,variable,..."
    keys_line_assigns = [r'\*set', r'\*get', r'\*del', r'\*dim']
    # Commands that could bug the code, like /exit and /clear
    keys_line_forbidden = ['/clear', 'eof', '/exit', r'\*ask']
    # Join each key group 
    pattLineKeys = {
        'parameters':   '|'.join(parameters),
        'assigns':      '|'.join(keys_line_assigns),
        'forbidden':    '|'.join(keys_line_forbidden)
    }

    # Keys for multiple lines
    # for *PREAD,...,END PREAD : 
    # r"^[^!]*((?<=(\*PREAD))\s*,\s*(ARRAY3D|ARRAY2D)\s*,(.|\n)*(?=(END PREAD)))"
    # 

    # Compile the regex patterns 
    # 
    # Old pattern
    #pattLine = re.compile(r"^[^!]*(((?<=({assigns}))\s*({parameters})\s*(?=,))|((?<![a-zA-Z_0-9])\s*({parameters})\s*(?=[=+]))|({forbidden}))".format(**pattLineKeys), flags=re.IGNORECASE)
    pattLine = re.compile(r"^[^!]*((?<![\w])({parameters})(?![\w])\s*\=|(?<=({assigns}))\s*,\s*({parameters})\s*,|({forbidden}))".format(**pattLineKeys), flags=re.IGNORECASE)
    #pattMulti = re.compile(r"", flags=re.IGNORECASE)

    # Read original script file
    with open(fname, 'r') as f:
        script = f.readlines()
    
    # Get script name
    _, scriptname = os.path.split(fname)

    # Filter the content and save the new script
    with open(f'{destination}\\{scriptname}', 'w') as f:
        for line in script:
            # If matchs make it's conent a comment
            if pattLine.search(line):
                f.write('! Line Removed by PARANSYS, old content: ')
            f.write(line)


def is_text_file(fname):
    """
    Test if a file is binary or text

    Args:
        fname (str): file location

    Returns:
        bool: If text return True, if binary return False
    """
    try:
        with open(fname, 'r') as f:
            _ = f.read()
            return True
    except:
        return False


def create_monitor(self):
    """
    Create the APDL file that will monitor ANSYS (monitor.paransys)
    """
    monitor = {
        "main": 'main.paransys',
        "wait": self._settings['monitor_wait']
    }
    monitorsource = "/NOPR\n*CREATE,rewctrl.paransys\n/OUTPUT,control,paransys\n*VWRITE,'PARANSYS_GO=%PARANSYS_GO%'\n%C\n*VWRITE,'PARANSYS_RUNS=%PARANSYS_RUNS%'\n%C\n*VWRITE,'PARANSYS_DONE=%PARANSYS_DONE%'\n%C\n*VWRITE,'PARANSYS_KILL=%PARANSYS_KILL%'\n%C\n/OUTPUT\n*END\nPARANSYS_LOOP=1\nPARANSYS_RUNS=0\n*DOWHILE,PARANSYS_LOOP\n/INPUT,control.paransys\n*IF,PARANSYS_GO,GE,1,THEN\nPARANSYS_GO=0\nPARANSYS_RUNS=PARANSYS_RUNS\nPARANSYS_DONE=0\nPARANSYS_KILL=0\n/INPUT,rewctrl,paransys\n/DELETE,par_out.paransys,,,BOTH\n/CLEAR,start.ans\n/INPUT,par_in.paransys\n/GOPR\n/INPUT,{main}\n/NOPR\nPARSAV,ALL,par_out.paransys\n/INPUT,control.paransys\nPARANSYS_GO=0\nPARANSYS_RUNS=PARANSYS_RUNS+1\nPARANSYS_DONE=1\nPARANSYS_KILL=0\n/INPUT,rewctrl,paransys\n*ELSEIF,PARANSYS_KILL,GE,1,THEN\n/DELETE,control.paransys,,,BOTH\n*EXIT\n*ENDIF\nPARANSYS_LOOP=1\n/WAIT,{wait}\n*ENDDO"
    monitorsource = monitorsource.format(**monitor)
    fapdlmonitor = '{run_location}\\monitor.paransys'.format(**self._ANSYS)
    with open(fapdlmonitor, 'w') as f:
        f.write(monitorsource)
    utils.messages.cprint(self, '   Monitor file created.')


def write_control(self, go=False, kill=False):
    """
    Write the control file.

    Args:
        go (bool, optional): Send a run signal. Defaults to False.
        kill (bool, optional): Send an exit signal to ANSYS. Defaults to False.
    """
    parameters = read_control(self)

    parameters['PARANSYS_GO']   = int(go)
    parameters['PARANSYS_KILL'] = int(kill)
    parameters['PARANSYS_DONE'] = 0 # Always
    
    write_parameters(self, 'control.paransys', parameters)
    utils.messages.cprint(self, '   Command sent.')


def read_control(self):
    """
    Read the control file.

    Returns:
        dict: with controls values.
    """
    parameters = read_parameters(self, 'control.paransys')
    if parameters:
        parameters = {
            'PARANSYS_GO':   bool(parameters['PARANSYS_GO']),
            'PARANSYS_DONE': bool(parameters['PARANSYS_DONE']),
            'PARANSYS_KILL': bool(parameters['PARANSYS_KILL']),
            'PARANSYS_RUNS':  int(parameters['PARANSYS_RUNS'])
        }
    else:
        parameters = {
            'PARANSYS_GO':   0,
            'PARANSYS_DONE': 0,
            'PARANSYS_KILL': 0,
            'PARANSYS_RUNS': 0
        }
        
    return parameters


def write_parin(self, parameters):
    """
    Write input parameters

    Args:
        parameters (dict): dictionary with parameters and it's values.
    """
    self._parin = parameters
    fname = 'par_in.paransys'
    write_parameters(self, fname, parameters)


def write_parameters(self, fname, parameters):
    """
    Create the file with input parameters values

    Args:
        fname (str): file that will receive parameters.
        parameters (dict): dictionary with parameters and it's values.
    """
    fname = '{}\\{}'.format(self._ANSYS['run_location'], fname)
    with open(fname, 'w') as f:
        for param in parameters:
            line = '{}={}\n'.format(param, parameters[param])
            f.write(line)


def read_parout(self):
    """
    Read and verify output parameters.

    Returns:
        dict: With all parameters and their values.
    """
    parout = read_parameters(self, 'par_out.paransys')
    parin  = self._parin
    for par in parin:
        if parin[par] != parout[par.upper()]:
            msg = '** Input parameter \"{}\" was set as \"{}\" but finished as \"{}\". It should not happen, please verify it!'.format(par, parin[par], parout[par.upper()])
            utils.messages.cprint(self, msg)
    return parout


def read_parameters(self, fname):
    """
    Read and interpret parameters from files. 

    It should be defined as `parm=value` or `*SET,parm,value`.

    Args:
        fname (str): File to import parameters

    Returns:
        dict: With all parameters and their values.
    """

    def str2num(strin):
        try:
            ans = float(strin)
            if ans == int(ans):
                ans = int(ans)
        except:
            ans = strin
        return ans


    fname = '{}\\{}'.format(self._ANSYS['run_location'], fname)

    if not os.path.isfile(fname):
        return False

    try:
        with open(fname, 'r') as f:
            content = f.readlines()
    except:
        utils.messages.cerror(self, f'PARANSYS cannot open \"{fname}\".')
    else:
        params = {}
        patt1 = re.compile(r'([\w]+)\s*\=\s*([0-9\.\-ED]+)', re.IGNORECASE)
        patt2 = re.compile(r'(?<=\*SET,)\s*([\w]+)\s*,\s*([0-9\.\-ED]+)', re.IGNORECASE)
        for line in content:
            result = patt1.search(line) or patt2.search(line)
            if result:
                params[result.group(1)] = str2num(result.group(2))

    return params


def remove_control(self):
    """
    Remove PARANSYS control file
    """
    controlfile = '{run_location}\\control.paransys'.format(**self._ANSYS)
    if os.path.isfile(controlfile):
        os.remove(controlfile)
        utils.messages.cprint(self, '   Control file removed.')
