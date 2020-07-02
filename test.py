from paransys2 import ANSYS
ans = ANSYS()
ans.setAPDLmodel('cant.inp')
res = ans.solve()
print(res)
