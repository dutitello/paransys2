import paransys2.utils as utils


def dict_to_upper(mydict):
    """
    Put every key of an dictionary in UPPER CASE.

    Args:
        mydict (dict)
    """
    
    def to_upper(what):
        if type(what) is str:
            return what.upper()
        else:
            upped = []
            for each in what:
                upped.append(to_upper(each))
            return tuple(upped)

    upped_dict = {}

    for key in mydict:
        upped_dict[to_upper(key)] = mydict[key]

    return upped_dict



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
