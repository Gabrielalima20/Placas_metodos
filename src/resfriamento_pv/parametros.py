from dataclasses import dataclass
from .configuracoes import SimulationConfig


@dataclass
class ParametrosDerivados:
    dz: float
    alpha: float
    Fo: float
    Bi_top: float
    Bi_bottom: float
    n_steps: int


def calcular_parametros(sim: SimulationConfig) -> ParametrosDerivados:
    """
    Calcula parâmetros derivados a partir da configuração:
      - dz, alpha, Fo, Bi_top, Bi_bottom, n_steps
    """
    L = sim.dominio.L
    nz = sim.dominio.nz

    k = sim.material.k
    rho = sim.material.rho
    cp = sim.material.cp

    dt = sim.dt
    h_top = sim.cc.h_top
    h_bottom = sim.cc.h_bottom

    dz = L / (nz - 1)
    alpha = k / (rho * cp)
    Fo = alpha * dt / dz**2

    Bi_top = h_top * dz / k
    Bi_bottom = h_bottom * dz / k

    n_steps = int(sim.t_final / dt)

    if sim.metodo_tempo == "explicito" and Fo > 0.5:
        raise ValueError(
            f"Método explícito instável com Fo={Fo:.3f}; reduza dt ou aumente nz."
        )

    return ParametrosDerivados(
        dz=dz,
        alpha=alpha,
        Fo=Fo,
        Bi_top=Bi_top,
        Bi_bottom=Bi_bottom,
        n_steps=n_steps,
    )
