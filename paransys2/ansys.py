"""
The main class of the library
"""

import re 
import os
import time
import atexit
import paransys2.utils as utils

class ANSYS:
    """
    This class make the connection betwen Python and the ANSYS software.
     
    """
    
    def __init__(self, exec_loc=None, run_location='.\\workingdir', jobname='file', nproc=2, cleardir=False, add_flags=''):
        """
        Configure the connection betwen Python and ANSYS setting ANSYS configuration.

        Args:
            exec_loc (str, optional): ANSYS executable location (like ANSYS194.exe). Defaults to None, then PARANSYS will try to find it.
            run_location (str, optional): Folder where ANSYS will work. Defaults to '.\\workingdir\\'.
            jobname (str, optional): ANSYS jobname. Defaults to 'file'.
            nproc (int, optional): number of processor cores used. Defaults to 2.
            cleardir (bool, optional): clear all files in the working directory before running. Defaults to False.
            add_flags (str, optional): additional ANSYS execution flags. Do not use `-b -i -o`. Defaults to ''.
        """

        atexit.register(self.exit)

        # Define default variables
        self._print = True
        self._log = False

        self._settings = {
            'monitor_wait':     0.5,    # Seconds
            'starter_max_wait':  30,    # Seconds
            'starter_sleep':    1.0     # Seconds

        }

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
            'exec_loc': exec_loc,
            'run_location': run_location,
            'jobname': jobname,
            'nproc': nproc,
            'cleardir': cleardir,
            'add_flags': add_flags
        }


    def setAPDLmodel(self, main, extrafiles=[], location='.'):
        """
        Sets APDL model script and other necessary files.

        Args:
            main (str): main APDL script (who will run)
            extrafiles (list of strings, optional): list with files that will complete the model. Defaults to [].
            location (str, optional): Folder where the main script and another files are. Defaults to '.' (current folder).
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


    def solve(self, P26vars=[], **parin):
        """
        Solve ANSYS model with parameters set as `solve(parA=1, B=2, c=5)` or by a dictionary with names and values set by **parin.

        Args:
            **parin (dict): each model parameter in the form `name=value` or a dictionary with names and values set by **dictname. 
            P26vars (list of integers): A list of POST26 (time history postproccess) variables numbers. This POST26 variables will be exported in a pandas.DataFrame.
            

        Returns:
            dict: An dictionary with all parameters values at the end of the analysis.
            pandas.DataFrame: A pandas DataFrame with asked POST26 variables.
        """
        
        utils.ansys.start(self)
        utils.messages.cprint(self, 'Setting solver.')

        utils.files.write_parin(self, parin)
        utils.files.write_ask_post26(self, P26vars)
        utils.files.copy_model(self, parin)

        utils.files.write_control(self, go=True)
        utils.messages.cprint(self, '   Solving...')

        tstart = time.time()
        time.sleep(1)
        while utils.files.read_control(self)['PARANSYS_DONE'] == 0:
            time.sleep(1)

        utils.messages.cprint(self, 'Solved in {:.3f} minutes.'.format((time.time()-tstart)/60))
        
        parameters = utils.files.read_parout(self)
        if len(P26vars) > 0:
            p26df = utils.files.read_post26(self)
        else:
            p26df = None

        return parameters, p26df
        

    def grad(self, dh=0.05, method='forward', onlyfor=[], notfor=[], **parin):
        """
        Evaluate the gradient of all output parameters in relation to input parameters using the finite difference method.

        By default the gradient is evaluate in relation of all input parameters, if you need to evaluate just for some specific
        parameters you can put it's names in `onlyfor` list. In the other hand, if you need all but not for some 
        specific you can put it's name on `notfor` list. It looks confuse, I know... So there are more explanations  
        and examples at `/examples/grad.ipynb`.


        There are 3 possible difference methods here, in all it's adopted that: `h = x.dh`

        The forward method: `f\'(x) = (f(x+h)-f(x))/h`

        The backward method: `f\'(x) = (f(x)-f(x-h))/h`

        The central method: `f\'(x) = (f(x+h/2)-f(x-h/2))/h`

        The forward and backward methods need to evaluate the function at `f(x)`, so in this cases this result is appendend in the dictionary.

        Args:
            dh (float, optional): Relative step size in relation to the variable value. Defaults to 0.05.
            method (str, optional): Finite difference method. Defaults to 'forward'.
            onlyfor (list of strings, optional): A list with the exclusive parameters that model will be derivated for.
            notfor (list of strings, optional): A list with the parameters that model will not be derivated for.
            **parin (dict): each model parameter in the form `name=value` or a dictionary with names and values set by **parin.

        Returns:
            dict: A dictionary with the gradient of all output parameters in relation to here inputed parameters.

        The gradient returned is in the form `grad('parameter','variable')`, that is, the variation of `parameter` in relation to `variable`. 
        
        Some examples are:
        > `dy/dx` = `y'(x)` = `grad('y','x')`

        > `dStress/dh` = `Stress'(h)` = `grad('Stress','h')`

        """

        # Everything need to be in UPPER CASE or it will be a mess
        parin = utils.anothers.to_upper(parin)
        onlyfor = utils.anothers.to_upper(onlyfor)
        notfor = utils.anothers.to_upper(notfor)

        tstart = time.time()
        utils.messages.cprint(self, f'Evaluating gradient using {method} method and dh={dh}.')
        
        if len(onlyfor) > 0:
            evalfor = onlyfor.copy()
        else:
            evalfor = []
            for parameter in parin:
                evalfor.append(parameter)
        if len(notfor) > 0:
            for parameter in notfor:
                if parameter in evalfor:
                    evalfor.remove(parameter)
        utils.messages.cprint(self, 'Evaluating gradient in relation to: {}.'.format(', '.join(evalfor)))
        
        # h couldn't be 0
        def hnotnull(par):
            if par == 0.00: par = 1
            return dh*par

        # Forward and Backward is the same thing just change dh to negative
        if method in ['forward', 'backward']:
            if method == 'backward': dh = -dh
            # base = f(x)
            utils.messages.cprint(self, 'Solving base function.')
            base, _ = self.solve(**parin)
            grad = base.copy() # Append f(x)
            for parameter in evalfor:
                parcur = parin.copy()
                h = hnotnull(parin[parameter])
                parcur[parameter] += h
                utils.messages.cprint(self, f'Solving for {parameter}.')
                this, _ = self.solve(**parcur)
                for each in this:
                    grad[each, parameter] = (this[each]-base[each])/h
                utils.anothers.grad_progress(self, parameter, evalfor)


        # Central method
        elif method == 'central':
            grad = {}
            for parameter in evalfor:
                parinf = parin.copy()
                parsup = parin.copy()
                h = hnotnull(parin[parameter])
                parinf[parameter] -= h/2
                parsup[parameter] += h/2
                utils.messages.cprint(self, f'Solving minor limit for {parameter}.')
                minor, _ = self.solve(**parinf)
                utils.messages.cprint(self, f'Solving major limit for {parameter}.')
                major, _ = self.solve(**parsup)
                for each in minor:
                    grad[each, parameter] = (major[each]-minor[each])/h
                utils.anothers.grad_progress(self, parameter, evalfor)

        # Sometimes life isn't like we expect   
        else:
            utils.messages.cerror(self, "Unkown method.")


        # Thats the end    
        utils.messages.cprint(self, 'Gradient evaluated in {:.3f} minutes.'.format((time.time()-tstart)/60))
        return grad


    def exit(self):
        """
        Close ANSYS
        """
        utils.ansys.kill(self)
