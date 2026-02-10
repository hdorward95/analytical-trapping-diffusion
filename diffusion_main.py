from functions.diffusion_functions import (flux_analytical, 
                                           breakthrough_analytical,
                                           calc_D_eff,
                                           zeta_function_diffusion)


if __name__ == "__main__":
    out_flux = flux_analytical()

    print(' No traps')
    print(out_flux)

    print('Diffusion limited single trap type')
    zeta = zeta_function_diffusion()
    D_eff = calc_D_eff(zeta=zeta)
    tau_b_e = breakthrough_analytical(D_eff=D_eff)
    out_flux = flux_analytical(tau_b_e=tau_b_e)
    print(out_flux)

