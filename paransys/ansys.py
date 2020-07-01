"""
The main class of the library
"""

import re 
import os
import utils

class ANSYS:
    """
    This class make the connection betwen Python and the ANSYS software.
     
    """
    
    def __init__(self, exec_loc=None, run_location='.\\workingdir', jobname='file', nproc=2, override=True, cleardir=False, add_flags=''):
        """
        Configure the connection betwen Python and ANSYS setting ANSYS configuration.

        Args:
            exec_loc (str, optional): ANSYS executable location (like ANSYS194.exe). Defaults to None, then PARANSYS will try to find it.
            run_location (str, optional): Folder where ANSYS will work. Defaults to '.\\workingdir\\'.
            jobname (str, optional): ANSYS jobname. Defaults to 'file'.
            nproc (int, optional): number of processor cores used. Defaults to 2.
            override (bool, optional): erase possible .lock file in the working directory. Defaults to True.
            cleardir (bool, optional): clear all files in the working directory before running. Defaults to False.
            add_flags (str, optional): additional ANSYS execution flags. Do not use `-b -i -o`. Defaults to ''.
        """

        # Define default variables
        self._print = True
        self._log = False

        # Define default model
        self._model = {
            'main': '',
            'extrafiles': [],
            'location': ''
        }

        # Define


        # Try to find ANSYS executable location 
        if exec_loc is None:
            exec_loc = utils.ansys.find_exec(self)

        # Try to acces run_location folder
        if not os.path.isdir(run_location):
            if run_location == '.\\workingdir':
                os.mkdir(run_location)
            else:
                utils.messages.cerror(self, f'PARANSYS could not access current run_location folder ({run_location}).')

        # Save ANSYS configuration
        self._ANSYS = {
            'exec': exec_loc,
            'run_location': run_location,
            'jobname': jobname,
            'nproc': nproc,
            'override': override,
            'cleardir': cleardir,
            'add_flags': add_flags
        }


    def setAPDLmodel(self, main, extrafiles=[], location=''):
        """
        Sets APDL model script and other necessary files.

        Args:
            main (str): main APDL script (who will run)
            extrafiles (list of strings, optional): list with files that will complete the model. Defaults to [].
            location (str, optional): Folder where the main script and another files are. Defaults to '' (current folder).
        """

        # Test location folder
        if location:
            if not os.path.isdir(location): 
                utils.messages.cerror(self, f'PARANSYS could not access current model location folder ({location}).')

        # Test all files
        curfile = f'{location}\\{main}'
        if not os.path.isfile(curfile):
            utils.messages.cerror(self, f'Main APDL script doesn\'t exist as \"{curfile}\".')
        for each in extrafiles:
            curfile = f'{location}\\{each}'
            if not os.path.isfile(curfile):
                utils.messages.cerror(self, f'Extra file {each} doesn\'t exist as \"{curfile}\".')

        # Save
        self._model['main'] = main
        self._model['extrafiles'] = extrafiles
        self._model['location'] = location

        utils.messages.cprint(self, f'APDL model scripts set as:')
        utils.messages.cprint(self, f'   Main script: {main}.')
        utils.messages.cprint(self, f'   Extra files: {extrafiles}.')
        utils.messages.cprint(self, f'   Location: {location}.')


    def _start(self):
        """
        Start ANSYS software if it isn't running yet.

        """
        pass


    def solve(self, **vars):
        """
        Solve ANSYS model with parameters set by **vars.

        Args:
            **vars: each model parameter could be set separately or could be used a dictionary with all variables names and values passed as **dictname.

        Returns:
            dict: An dictionary with all parameters values at the end of the analysis.
        """
        
        if not utils.ansys.is_running(self):
            pass



        parameters = {} 
        return parameters



    def grad(self, dh=0.05, method='forward', **vars):
        """
        Evaluate the gradient of all parameters in relation to parameters set by **vars using the finite difference method.

        There are 3 possible methods, in all it's adopted that: `h = x.dh`

        The forward method: `f\'(x) = (f(x+h)-f(x))/h`

        The backward method: `f\'(x) = (f(x)-f(x-h))/h`

        The central method: `f\'(x) = (f(x+h/2)-f(x-h/2))/h`

        Args:
            dh (float, optional): Relative step size in relation to the variable value. Defaults to 0.05.
            method (str, optional): [description]. Defaults to 'forward'.

        Returns:
            dict: [description]
        """
        grad = {}
        return grad


