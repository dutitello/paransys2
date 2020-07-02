"""
Useful function for messages
"""

# Custom print and error messages
def cprint(self, message):
    """
    Custom print function with log to file

    Args:
        message (str): custom print message
    """
    if self._print:
        print(message)
    if self._log:
        with open(self._log, 'a+') as log:
            log.write(rf'{message}\n')

def cerror(self, error):
    """
    (For internal use)
    Custom error with raise RuntimeError with log to file

    Args:
        error (str): custom error message to raise

    Raises:
        RuntimeError: custom message
    """
    if self._log:
        with open(self._log, 'a+') as log:
            log.write(r'\n\nPARANSYS Runtime error: \n')
            log.write(rf'{error}\n')
            log.write(r'\n')
    raise RuntimeError(error)