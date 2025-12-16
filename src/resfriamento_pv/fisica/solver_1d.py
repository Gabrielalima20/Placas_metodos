import numpy as np
from ..configuracoes import SimulationConfig
from ..parametros import ParametrosDerivados
from .pv_power_model import calculate_heat_generation, calculate_efficiency


def solve_implicit_step(
    T_n: np.ndarray,
    sim: SimulationConfig,
    params: ParametrosDerivados,
) -> np.ndarray:
    """
    Avança um passo de tempo usando Método Implícito (Backward Euler)
    com convecção + radiação nas faces.
    """
    k = sim.material.k
    rho = sim.material.rho
    cp = sim.material.cp
    T_inf = sim.cc.T_inf

    dz = params.dz
    Fo = params.Fo
    Bi_top = params.Bi_top
    Bi_bottom = params.Bi_bottom
    Ny = len(T_n)

    # ============================================================
    # 1) Construção da matriz A (Backward Euler)
    # ============================================================
    A = np.zeros((Ny, Ny))

    # Nós internos
    for i in range(1, Ny - 1):
        A[i, i - 1] = -Fo
        A[i, i]     = 1 + 2 * Fo
        A[i, i + 1] = -Fo

    # Borda inferior (y=0)
    A[0, 0] = 1 + 2 * Fo * (1 + Bi_bottom)
    A[0, 1] = -2 * Fo

    # Borda superior (y=L)
    A[-1, -2] = -2 * Fo
    A[-1, -1] = 1 + 2 * Fo * (1 + Bi_top)

    # ============================================================
    # 2) Termo radiativo nas bordas (explícito)
    # ============================================================
    sigma_sb = 5.670374419e-8  # Stefan-Boltzmann

    eps_top = sim.cc.epsilon_top
    eps_bottom = sim.cc.epsilon_bottom

    T_bottom = T_n[0]
    T_top = T_n[-1]

    q_rad_bottom = eps_bottom * sigma_sb * (T_bottom**4 - T_inf**4)  # W/m²
    q_rad_top    = eps_top    * sigma_sb * (T_top**4    - T_inf**4)  # W/m²

    # Converte para incremento de temperatura (K)
    rad_term_bottom = q_rad_bottom * sim.dt / (rho * cp * dz)
    rad_term_top    = q_rad_top    * sim.dt / (rho * cp * dz)

    # ============================================================
    # 3) Montagem do vetor B
    # ============================================================
    q_dot = calculate_heat_generation(T_n, sim)  # W/m³
    source_term = q_dot * sim.dt / (rho * cp)

    B = T_n + source_term

    # perdas radiativas explícitas
    B[0]  -= rad_term_bottom
    B[-1] -= rad_term_top

    # termos convectivos (como antes)
    B[0]  += 2 * Fo * Bi_bottom * T_inf
    B[-1] += 2 * Fo * Bi_top * T_inf

    # ============================================================
    # 4) Resolve o sistema linear A * T^{n+1} = B
    # ============================================================
    T_new = np.linalg.solve(A, B)

    return T_new


def rodar_simulacao_1d(sim: SimulationConfig, params: ParametrosDerivados):
    """
    Loop temporal completo 1D.

    Retorna:
      times          : array de tempos [s]
      T_history      : temperatura média da placa ao longo do tempo [K]
      eta_history    : eficiência média da célula ao longo do tempo [-]
      T_final        : perfil final de temperatura na espessura [K]
    """
    Ny = sim.dominio.nz

    # Condição inicial: toda a placa em T_inf
    T = np.ones(Ny) * sim.cc.T_inf

    history_time = []
    history_T_avg = []
    history_eta_avg = []

    current_time = 0.0

    for step in range(params.n_steps):
        T = solve_implicit_step(T, sim, params)
        current_time += sim.dt

        T_avg = T.mean()
        eta_avg = calculate_efficiency(T, sim).mean()

        history_time.append(current_time)
        history_T_avg.append(T_avg)
        history_eta_avg.append(eta_avg)

    return (
        np.array(history_time),
        np.array(history_T_avg),
        np.array(history_eta_avg),
        T,
    )
