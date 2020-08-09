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
        

def deriv_progress(self, parameter, parin):
    """
    Found how much of derivatives is complete.

    Args:
        parameter (str): Current parameter.
        parin (dict): All input parameters.
    """
    i = 0
    for each in parin:
        i += 1
        if each == parameter:
            done = i/len(parin)
            utils.messages.cprint(self, 'Derivatives {:.2%} evaluated.'.format(done))


def str2num(strin):
        try:
            ans = float(strin)
            if ans == int(ans):
                ans = int(ans)
        except:
            ans = strin
        return ans


monitor_apdl = """
/NOPR
*CREATE,rewctrl.paransys
/OUTPUT,control,paransys
*VWRITE,'PARANSYS_GO=%PARANSYS_GO%'
%C
*VWRITE,'PARANSYS_RUNS=%PARANSYS_RUNS%'
%C
*VWRITE,'PARANSYS_DONE=%PARANSYS_DONE%'
%C
*VWRITE,'PARANSYS_KILL=%PARANSYS_KILL%'
%C
/OUTPUT
*END
*CREATE,P26EXP.paransys.mac
_P26_PAR=ARG1
*IF,_P26_PAR,EQ,0,THEN
*GET,_P26_SIZE,VARI,1,NSETS
*DIM,_P26_EXPORT,TABLE,_P26_SIZE,1
VGET,_P26_EXPORT(1,0),1
/OUTPUT,'P26_out','paransys','.'
*GET,_P26_SIZE,VARI,1,NSETS
*DIM,_P26_EXPORT,TABLE,_P26_SIZE,1
VGET,_P26_EXPORT(1,0),1
*VWRITE,'!---PARANSYS---!'
%C
/OUTPUT,TERM
*ELSE
*GET,_P26_SIZE,VARI,_P26_PAR,NSETS
*DEL,_P26_EXPORT
*DIM,_P26_EXPORT,TABLE,_P26_SIZE,1
VGET,_P26_EXPORT(1,0),_P26_PAR
/OUTPUT,'P26_out','paransys',,APPEND
*VWRITE,'*P26VAR=%_P26_PAR%'
%C
*VWRITE,_P26_EXPORT(1,0)
%G
*VWRITE,'*P26END'
%C
/OUTPUT,TERM
*ENDIF
*END
PARANSYS_LOOP=1
PARANSYS_RUNS=0
*DOWHILE,PARANSYS_LOOP
/INPUT,control.paransys
*IF,PARANSYS_GO,GE,1,THEN
PARANSYS_GO=0
PARANSYS_RUNS=PARANSYS_RUNS
PARANSYS_DONE=0
PARANSYS_KILL=0
/INPUT,rewctrl,paransys
/DELETE,par_out.paransys,,,BOTH
/CLEAR,start.ans
/INPUT,par_in.paransys
/GOPR
/INPUT,{main}
/NOPR
PARSAV,ALL,par_out.paransys
/INPUT,rP26.paransys
/INPUT,control.paransys
PARANSYS_GO=0
PARANSYS_RUNS=PARANSYS_RUNS+1
PARANSYS_DONE=1
PARANSYS_KILL=0
/INPUT,rewctrl,paransys
*ELSEIF,PARANSYS_KILL,GE,1,THEN
/DELETE,control.paransys,,,BOTH
*EXIT
*ENDIF
PARANSYS_LOOP=1
/WAIT,{wait}
*ENDDO"""
