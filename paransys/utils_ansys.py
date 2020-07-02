"""
Useful function for ANSYS
"""

import re
import os
import utils
import time

def find_exec(self):
    """
    Try to find ANSYS executable location by enviroment variables

    Returns:
        str: ANSYS executable location
    """
    ansys_version = 0
    for var in os.environ:
        result = re.search(r'(?<=ANSYS)[0-9]+(?=_DIR)', var, re.IGNORECASE)
        if result:
            ansys_version = max(int(result.group(0)), ansys_version)

    if ansys_version > 0:
        exec_loc = os.getenv(fr'ANSYS{ansys_version}_DIR')
        exec_loc = fr'{exec_loc}\bin\winx64\ANSYS{ansys_version}.exe'

    if os.path.isfile(exec_loc):
        utils.messages.cprint(self, fr'Using ANSYS v{ansys_version} found at "{exec_loc}".')
        return exec_loc
    else:
        utils.messages.cerror(self, r'ANSYS installation not found, please define it with "exec_loc=".')


def start(self):
    """
    Start ANSYS if it isn't already running
    """
    
    if not is_running(self):
        utils.files.create_monitor(self)
        utils.files.override_lockfile(self)
        utils.files.write_control(self)
        
        flags = '-b -i monitor.paransys -o paransys.log -smp -np {nproc} -j {jobname} -dir \"{run_location}\" {add_flags} '.format(**self._ANSYS)
        _ = os.spawnl(os.P_NOWAIT, self._ANSYS['exec_loc'], flags)
    
    #


def kill(self):
    """
    Close ANSYS
    """
    while is_running(self):
        utils.files.write_control(self, kill=True)
        time.sleep(1)
    else:
        utils.messages.cprint(self, 'ANSYS closed.')



def is_running(self):
    """
    Test if ANSYS is running. It also tests if current jobname is right.

    Returns:
        bool: Is it running?
    """
    # Running start as False
    running = False

    # Is running and current jobname is right?
    try:
        expectedlockfile = '{}\\{}.lock'.format(self._ANSYS['run_location'], self._ANSYS['jobname'])
        f = open(expectedlockfile, 'w')
    except:
        # Ok, it couldn't open the file, something is running at that
        running = True
    else:
        # The file doesn't exists or ANSYS not running
        f.close()
        # Look all .lock files in the folder
        for fname in os.listdir(self._ANSYS['run_location']):
            result = re.search(r'.*(?=\.lock)', fname, re.IGNORECASE)
            if result:
                newjobname = result.group(0)
                lockfile = '{}\\{}.lock'.format(self._ANSYS['run_location'], newjobname)
                try:
                    f = open(lockfile, 'w')
                except:
                    running = True
                    self._ANSYS['jobname'] = newjobname
                    break
                else:
                    f.close()
    return running





