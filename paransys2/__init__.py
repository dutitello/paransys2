"""
A new version of PARANSYS library.
"""

from paransys2.ansys import ANSYS
from time import sleep

if __name__ == '__main__':
    ans = ANSYS()
    ans.solve()
    sleep(5)
    ans.close()
