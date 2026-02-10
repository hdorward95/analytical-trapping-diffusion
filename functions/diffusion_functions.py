import numpy as np

def flux_analytical(C_0=3.1622e18, 
                    D= 1,
                    l = 1,
                    t_start = 0,
                    t_end = 1,
                    t_step = 10,
                    tau_b_e = 0.05,
                    m = 10):
    '''
    Compute the flux through the far wall of a permeation barrier. See
    TMAP8 ver-1d example. This is the analytical solution for the flux
    through time.
    
    :param C_0: The constant dissolved gas concentration at the left
    boundary. (atoms/m^2)
    :param D: The diffusivity of the dissolved gas in the medium.
    (m^2/s)
    :param l: The length from the left boundary to right boundary. (m)
    :param t_start: The initial time to report. (s)
    :param t_end: The final time to report. (s)
    :param t_step: int. The number of time steps. (-)
    :param tau_b_e: The breakthrough time. (s)
    :param m: Order at which to truncate the (Fourier series?) solution
    '''

    # Create time vector
    t = np.linspace(t_start,t_end,t_step)

    # Calculate the sum over order m.
    summand = np.zeros(np.shape(t))
    for i in range(m):
        summand += ((-1)**(i+1))*np.exp(-((i+1)**2)*(t/(2*tau_b_e)))

    # Now compute and return the analytical solution for flux.       
    return ((C_0*D)/l) * (1+2*summand)



def breakthrough_analytical(l=1,
                            D_eff=1):
    '''
    Compute the analytical breakthrough time from the domain length and
    effective diffusivity.
    
    :param l: Domain length. (m)
    :param Deff: Effective diffusivity. (m^2/s)
    '''
    return ((l**2)/(2*D_eff*np.pi**2))



def calc_D_eff(zeta,D=1):
    '''
    Calculate the effective diffusivity from a given configuration.
    
    :param zeta: The zeta function defining the modification to the
    diffusivty given the problem trapping parameters.
    :param D: The unmodified diffusivity for the gas in the medium 
    under the presence of no traps. (m^2/s)
    '''
    return D/(1+(1/zeta))

def zeta_function_diffusion(lattice = np.sqrt(10**-15),
                  nu = 10**13,
                  C_t0 = 0.1,
                  D = 1,
                  E_d = 0,
                  epsilon = 100,
                  k = 1,
                  T = 1000,
                  ):
    '''
    Calculate the zeta function to modify the diffusivity to account 
    for single traps. Note, the last term in the TMAP8 documentation
    c_f/c_t0 is ignored as assumption is the diffusion is diffusion 
    limited, not trap limited.
    
    :param lattice: Lattice parameter. (m)
    :param nu: Debeye frequency. (s^-1)
    :param C_t0: Fraction of host sites that can trap. (-)
    :param D: The unmodified difufsivity for the gas in the medium. 
    (m^2/s)
    :param E_d: Diffusion activation energy. (J)
    :param epsilon: Trap energy. (J)
    :param k: Boltzmann constant. (J/K)
    :param T: Temperature. (K)
    '''
    
    exponent = (E_d-epsilon)/(k*T)
    return ((nu*lattice**2)/(C_t0*D))*np.exp(exponent)