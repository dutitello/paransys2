"""
Useful function for ANSYS
"""

import re
import os
import time
import paransys2.utils as utils

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
        utils.messages.cprint(self, 'Starting ANSYS.')
        utils.files.create_monitor(self)
        utils.files.remove_control(self)
        utils.files.write_control(self)
        
        flags = '  -b -i \"{run_location}\\monitor.paransys\" -o \"{run_location}\\paransys.ansys.log\" -smp -np {nproc} -j {jobname} -dir \"{run_location}\" {add_flags} '.format(**self._ANSYS)
        _ = os.spawnl(os.P_NOWAIT, self._ANSYS['exec_loc'], flags)

        count = 0
        while (not is_running(self)) and (count <= self._settings['starter_max_wait']):
            count += self._settings['starter_sleep']
            time.sleep(self._settings['starter_sleep'])

        if is_running(self):
            utils.messages.cprint(self, '   ANSYS started.')
        else:
            utils.messages.cerror(self, '   ANSYS couldn\'t start.')
    return None


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
    Test if ANSYS is running.

    Returns:
        bool: Is it running?
    """
    running = False
    lockfile = '{}\\{}.lock'.format(self._ANSYS['run_location'], self._ANSYS['jobname'])
    if os.path.isfile(lockfile):
        try:
            os.remove(lockfile)
        except:
            running = True
    return running
