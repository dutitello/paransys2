def deriv_cantilever():
    import paransys2
    import pandas 
    import matplotlib.pyplot as plt
    
    # Print some explanations
    print('\n\nEvaluating the derivatives of a cantilever beam using derivatives() function.\n\n')

    # Create ANSYS connection object
    ansys = paransys2.ANSYS()

    # Find APDL script path that is located at examples folder
    apdlloc = '{}\\examples\\'.format(paransys2.__path__[0])

    # Set ANSYS APDL script 
    ansys.setAPDLmodel('cant.inp', location=apdlloc)

    #------
    # Evaluate the derivatives for b=4, h=1, l=60 and q=1.15 (default parameters) using
    # forward finite difference method. 
    print("\nEvaluating derivatives for default b, h, l and q parameters. Adopting forward finite difference method.")
    deriv = ansys.derivatives(dh=0.05, method='forward', b=4, h=1, l=60, q=1.15)
    print('deriv dictionary:\n', deriv)
    print('\nVariation of STRESS with respect to B:', deriv['STRESS', 'B'])
    print('\nVariation of STRESS with respect to H:', deriv['STRESS', 'H'])
    print('\nVariation of STRESS with respect to L:', deriv['STRESS', 'L'])
    print('\nVariation of STRESS with respect to Q:', deriv['STRESS', 'Q'])
    print('\n\n')


    #------
    # Evaluate the derivatives when b=4, h=1, l=60 and q=1.15 (default parameters), but just with respect to b.
    print("\nEvaluating derivatives for default parameters with respect to b. Adopting forward finite difference method.")
    deriv = ansys.derivatives(dh=0.05, method='forward', b=4, h=1, l=60, q=1.15, onlyfor=['b'])
    print('deriv dictionary:\n', deriv)
    print('\nVariation of STRESS with respect to B:', deriv['STRESS', 'B'])
    print('Note that just parameter b was derivated.')
    print('\n\n')


    #------
    # Evaluate the derivatives when b=4, h=1, l=60 and q=1.15 (default parameters), but not with respect to b and q.
    print("\nEvaluating derivatives for default parameters but not with respect to b and q. Adopting central finite difference method.")
    deriv = ansys.derivatives(dh=0.05, method='central', b=4, h=1, l=60, q=1.15, notfor=['b', 'q'])
    print('deriv dictionary:\n', deriv)
    print('\nVariation of STRESS with respect to H:', deriv['STRESS', 'H'])
    print('\nVariation of STRESS with respect to L:', deriv['STRESS', 'L'])
    print('Note that parameters b and q were ignored.')
    print('\n\n')

    # Close ANSYS
    ansys.exit()
