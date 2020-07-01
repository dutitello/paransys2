"""
Useful functions for files

"""
import re
import os
import utils
import shutil

def copy_model(self, fname, destination, parameters):
    """
    Copy model files. 
    
    Script files are filtered looking for some commands and parameters, binary files are just coppied.

    Args:
        fname (str): source file
        destination (str): destionation folder
        parameters (dict): analysis parameters that PARANSYS will change if it's a script
    """
    # Test if file is script or binary
    try:
        if is_text_file(fname):
            # Filter file looking for current parameters
            copy_and_filter_scripts(fname, destination, parameters)
        else:
            # It's binary file, just copy it
            shutil.copy(fname, destination)
    except:
        utils.messages.cerror(self, rf'PARANSYS couldn\'t copy \"{fname}\".')


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

    # Commands that assigns values to variables in the form "command,variable,..."
    keys_assigns = [r'\*set,', r'\*get,', r'\*del,']
    # Commands that could bug the code, like /exit and /clear
    keys_forbidden = ['/clear', 'eof', '/exit', r'\*ask']

    # Join each key group 
    pattKeys = {
        'parameters':   '|'.join(parameters),
        'assigns':      '|'.join(keys_assigns),
        'forbidden':    '|'.join(keys_forbidden)
    }

    # Compile the regex pattern
        # The first patch ^[^!]* run until found a ! (comment), after it doesn't matter to ANSYS
        # The seccond patch ((?<=({assigns}))\s*({parameters})\s*(?=,)) looks for "{assigns},{parameters},"
        # The third patch ((?<![a-zA-Z_0-9])\s*({parameters})\s*(?=[=+]))) looks for "{parameters}=value"
        # The fourth patch ({2}) looks for {forbidden} commands, like /clear, /exit
    patt = re.compile(r"^[^!]*(((?<=({assigns}))\s*({parameters})\s*(?=,))|((?<![a-zA-Z_0-9])\s*({parameters})\s*(?=[=+]))|({forbidden}))".format(**pattKeys), flags=re.IGNORECASE)

    # Read original script file
    with open(fname, 'r') as f:
        script = f.readlines()
    
    # Get script name
    _, scriptname = os.path.split(fname)

    # Filter the content and save the new script
    with open(f'{destination}\\{scriptname}', 'w') as f:
        for line in script:
            # If matchs make it's conent a comment
            if patt.search(line):
                f.write('! Line Removed by PARANSYS, old content: ')
            f.write(line)


def is_text(fname):
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



def import_parameters():
    pass