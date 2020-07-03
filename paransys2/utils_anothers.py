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
