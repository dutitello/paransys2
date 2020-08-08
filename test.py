from paransys2 import ANSYS
ans = ANSYS()
ans.setAPDLmodel('cant.inp')
res = ans.solve()
print(res)
grad1 = ans.grad(b=4, h=1, e=90000, l=60)
grad2 = ans.grad(b=4, h=1, e=90000, l=60, onlyfor=['b','h','e'], notfor=['e'])
grad3 = ans.grad(b=4, h=1, e=90000, l=60, notfor=['b','h'])
