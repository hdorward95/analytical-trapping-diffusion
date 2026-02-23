from functions.diffusion_functions import (flux_analytical, 
                                           breakthrough_analytical,
                                           calc_D_eff,
                                           zeta_function_diffusion)
from argparse import ArgumentParser

# Define the CLI arguments
def parse_arguments():
    parser = ArgumentParser(
        description="Compute the analytical solution for flux.",
        fromfile_prefix_chars='@')      # Specify character in command line to call inputs from a file.
    parser.add_argument("--l",
                        help='The length from the left boundary to right boundary. (m)',
                        type=float,
                        default=1.0)
    parser.add_argument("--D",
                        help='The diffusivity of the dissolved gas in the medium. (m^2/s)',
                        type=float,
                        default=1.0)
    parser.add_argument("--C_0",
                        help='The constant dissolved gas concentration at the left boundary. (atoms/m^2)',
                        type=float,
                        default=3.1622e18)
    parser.add_argument("--t_start",
                        help='The initial time to report. (s)',
                        type=float,
                        default=0.0)
    parser.add_argument("--t_end",
                        help='The final time to report. (s)',
                        type=float,
                        default=1.0)
    parser.add_argument("--t_step",
                        help='The number of time steps. (-)',
                        type=int,
                        default=10)
    parser.add_argument("--tau",
                        help='The breakthrough time. (s). If =0 then breakthrough time calculated analytically.',
                        type=float,
                        default = 0)
    parser.add_argument("--m",
                        help='Order at which to truncate the (Fourier series?) solution',
                        type=int,
                        default=9)
    parser.add_argument("--D_eff",
                        help='Effective diffusivity with traps. (m^2/s). If =0 then calculated analytically.',
                        type=float,
                        default=0)
    parser.add_argument("--zeta",
                        help='The zeta function defining the modification to the diffusivty given the problem trapping parameters.',
                        type=float,
                        default=0)
    parser.add_argument("--lattice",
                        help='Lattice parameter. (m)',
                        type=float,
                        default=3.1623e-8)
    parser.add_argument("--nu",
                        help='Debeye frequency. (s^-1)',
                        type=float,
                        default=1e13)
    parser.add_argument("--C_t0",
                        help='Fraction of host sites that can trap. (-)',
                        type=float,
                        default=0.1)
    parser.add_argument("--E_d",
                        help='Diffusion activation energy. (J)',
                        type=float,
                        default=0.0)
    parser.add_argument("--epsilon",
                        help='Trap energy. (J)',
                        type=float,
                        default=100.0)
    parser.add_argument("--k",
                        help='Boltzmann constant. (J/K)',
                        type=float,
                        default=1.0)
    parser.add_argument("--T",
                        help='Temperature. (K)',
                        type=float,
                        default=1000.0)    
    parser.add_argument("-v",
                        "--verbose",
                        help='Verbose outputs from simulation.',
                        type=bool,
                        default=False)
    
    return parser.parse_args()

    
# Define main script execution
def main():
    args = parse_arguments()

    # Compute zeta function if not provided
    if args.zeta == 0:
        zeta = zeta_function_diffusion(lattice = args.lattice,
                        nu = args.nu,
                        C_t0 = args.C_t0,
                        D = args.D,
                        E_d = args.E_d,
                        epsilon = args.epsilon,
                        k = args.k,
                        T = args.T,
                        )
        print("Calculating zeta function from user inputs and/or function defaults") if args.verbose else None
        
    else:
        zeta = args.zeta
        print("Using user defined zeta function.") if args.verbose else None

    # Compute effective diffusion if not provided
    if args.D_eff == 0:
        D_eff = calc_D_eff(zeta=zeta,
                        D=args.D)
        print("Calculating effective diffusivity (D_eff) from user inputs and/or function defaults") if args.verbose else None
        
    else:
        D_eff = args.D_eff
        print("Using user defined effective diffusivity (D_eff). Note: this makes zeta value redundant.") if args.verbose else None

    # Compute breakthrough time if not provided
    if args.tau == 0:
        tau = breakthrough_analytical(l=args.l,
                                    D_eff=D_eff)
        print("Calculating breakthrough time from user inputs and/or function defaults") if args.verbose else None
        
    else:
        tau = args.tau
        print("Using user defined breakthrough time. Note: this makes zeta value and effective diffusivity redundant.") if args.verbose else None

    # Calculate flux at given time incrememnts
    time, out_flux = flux_analytical(C_0=args.C_0, 
                        D= args.D,
                        l = args.l,
                        t_start = args.t_start,
                        t_end = args.t_end,
                        t_step = args.t_step,
                        tau_b_e = tau,
                        m = args.m)

    print('Time incrememnts')
    print(time)

    print('Flux at boundary')
    print(out_flux)


# Execute python programme
if __name__=="__main__":
    main()
