def cantilever():
    import paransys2
    import pandas 
    import matplotlib.pyplot as plt

    # Print some explanations
    print('\n\nRunning a cantilever APDL script using solve() function.\n\n')

    # Create ANSYS connection object
    ansys = paransys2.ANSYS()

    # Find APDL script path that is located at examples folder
    apdlloc = '{}\\examples\\'.format(paransys2.__path__[0])

    # Set ANSYS APDL script 
    ansys.setAPDLmodel('cant.inp', location=apdlloc)

    #------
    # Run current script in it's default set. 
    print("\nSolving for script in it\'s default set (without any arguments).")
    parout, p26df = ansys.solve()
    print('Output parameters dictionary: ', parout)
    print('POST26 dataframe: ', p26df)
    print('\n\n')

    #------
    # Run current script in it's default set, but asking for POST26 variables 2 and 3.
    print("\nSolving for script in it\'s default set, but asking for POST26 variables 2 and 3.")
    parout, p26df = ansys.solve(P26vars=[2, 3])
    print('Output parameters dictionary:', parout)
    print('(same as before)')
    print('POST26 dataframe:\n', p26df)
    print('\n')
    print('Now we got a DataFrame! Lets plot it!')
    p26df.plot()
    plt.title('POST26 variables for default set')
    plt.legend(title='POST26 variables')
    plt.show()
    print('\n\n')

    #------
    # Run current script adopting b=5 and h=2, and then asking for POST26 variables 2 and 3.
    print("\nSolving script adopting b=5 and h=2, and then asking for POST26 variables 2 and 3.")
    parout, p26df = ansys.solve(b=5, h=2, P26vars=[2, 3])
    print('Output parameters dictionary:', parout)
    print('POST26 dataframe:\n', p26df)
    print('\n')
    p26df.plot()
    plt.title('POST26 variables when b=5 and h=2')
    plt.legend(title='POST26 variables')
    plt.show()
    print('\n\n')

    # All done. Close ANSYS
    ansys.exit()

    # Another explanations
    print('''\n\nThis example used solve() function.
    You should also take a look at the deriv_cantilever example, where the derivatives() function is presented.\n\n''')