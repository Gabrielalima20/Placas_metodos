import numpy as np
from ..configuracoes import SimulationConfig


def calculate_efficiency(T_kelvin: np.ndarray, sim: SimulationConfig) -> np.ndarray:
    pv = sim.pv_cell
    eta_ref = pv.ref_efficiency
    beta = pv.temp_coeff_beta
    T_ref = pv.ref_temp_K

    eta = eta_ref * (1.0 - beta * (T_kelvin - T_ref))
    return np.maximum(0.0, eta)


def calculate_heat_generation(T_kelvin: np.ndarray, sim: SimulationConfig) -> np.ndarray:
    """
    Geração volumétrica q''' [W/m³].

    Só há geração nos nós da região da célula (espessura L_gen).
    Fora dessa região, q''' = 0.
    """
    G = sim.cc.G

    L_total = sim.dominio.L
    L_gen = sim.pv_cell.absorbing_thickness

    eta = calculate_efficiency(T_kelvin, sim)

    Ny = len(T_kelvin)
    z = np.linspace(0.0, L_total, Ny)

    q_triple = np.zeros_like(T_kelvin)

    # só gera calor na camada da célula (0 <= z <= L_gen)
    mask = z <= L_gen
    q_triple[mask] = G * (1.0 - eta[mask]) / L_gen

    return q_triple
