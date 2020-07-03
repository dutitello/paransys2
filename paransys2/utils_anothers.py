import paransys2.utils as utils

def to_upper(thing):
    """
    Put whatever it is in UPPER case
    """
    if type(thing) is str:
        return thing.upper()
    elif type(thing) in [list, tuple]:
        newlist = []
        for each in thing:
            newlist.append(to_upper(each))
        if type(thing) is tuple:
            newlist = tuple(newlist)
        return newlist
    elif type(thing) is dict:
        newdict = {}
        for key in thing:
            newdict[to_upper(key)] = to_upper(thing[key])
        return newdict
    else:
        return thing
        

def grad_progress(self, parameter, parin):
    """
    Found how much of grad is complete.

    Args:
        parameter (str): Current parameter.
        parin (dict): All input parameters.
    """
    i = 0
    for each in parin:
        i += 1
        if each == parameter:
            done = i/len(parin)
            utils.messages.cprint(self, 'Gradient {:.2%} evaluated.'.format(done))
