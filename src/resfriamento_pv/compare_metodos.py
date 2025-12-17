import os
import sys
from dataclasses import replace

import matplotlib.pyplot as plt

from .configuracoes import SimulationConfig, carregar_config_yaml
from .fisica.solver_1d import rodar_simulacao_1d
from .parametros import calcular_parametros

DEFAULT_CONFIG = "configs/caso_base.yaml"


def preparar_config(base: SimulationConfig, metodo: str) -> SimulationConfig:
    """Retorna uma cópia do config com o método temporal ajustado."""
    sim = replace(base)
    sim.metodo_tempo = metodo
    sim.sim_name = f"{base.sim_name}_{metodo}"
    return sim


def rodar_simulacao(sim: SimulationConfig):
    """Calcula parâmetros derivados e executa a simulação 1D."""
    sim = _ajustar_dt_para_explicito(sim)
    params = calcular_parametros(sim)
    times, T_hist, eta_hist, _, _ = rodar_simulacao_1d(sim, params)

    t_min = times / 60.0
    T_C = T_hist - 273.15
    eta_pct = eta_hist * 100.0
    return t_min, T_C, eta_pct


def _ajustar_dt_para_explicito(sim: SimulationConfig) -> SimulationConfig:
    """
    Se o esquema for explícito, reduz dt automaticamente para satisfazer Fo<=0.5.

    Isso evita que `compare_metodos` pare com ValueError ao usar configurações
    pensadas para o solver implícito.
    """

    if sim.metodo_tempo != "explicito":
        return sim

    dz = sim.dominio.L / (sim.dominio.nz - 1)
    alpha = sim.material.k / (sim.material.rho * sim.material.cp)
    dt_limite = 0.5 * dz**2 / alpha

    if sim.dt <= dt_limite:
        return sim

    print(
        "[aviso] dt para o esquema explícito era grande demais; "
        f"reduzindo de {sim.dt:.3e} s para {dt_limite:.3e} s para atender Fo<=0.5."
    )
    return replace(sim, dt=dt_limite)


def main():
    cfg_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CONFIG
    if not os.path.exists(cfg_path):
        raise FileNotFoundError(f"Arquivo de config não encontrado: {cfg_path}")

    base_sim = carregar_config_yaml(cfg_path)

    cenarios = [
        ("Implicito (Backward Euler)", "implicito"),
        ("Explicito (Forward Euler)", "explicito"),
    ]

    resultados = []
    for label, metodo in cenarios:
        print(f"Rodando {label} com {cfg_path}")
        sim = preparar_config(base_sim, metodo)
        t_min, T_C, eta_pct = rodar_simulacao(sim)
        resultados.append((label, t_min, T_C, eta_pct))

    os.makedirs("resultados", exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    ax_T = axes[0]
    for label, t_min, T_C, _ in resultados:
        ax_T.plot(t_min, T_C, label=label)
    ax_T.set_title("Temperatura média da placa")
    ax_T.set_xlabel("Tempo (min)")
    ax_T.set_ylabel("T média (°C)")
    ax_T.grid(True)
    ax_T.legend()

    ax_eta = axes[1]
    for label, t_min, _, eta_pct in resultados:
        ax_eta.plot(t_min, eta_pct, label=label)
    ax_eta.set_title("Eficiência média da célula")
    ax_eta.set_xlabel("Tempo (min)")
    ax_eta.set_ylabel("Eficiência (%)")
    ax_eta.grid(True)
    ax_eta.legend()

    plt.tight_layout()
    out_path = "resultados/comparacao_metodos.png"
    plt.savefig(out_path, dpi=200)
    print(f"Figura salva em {out_path}")
    plt.show()


if __name__ == "__main__":
    main()
