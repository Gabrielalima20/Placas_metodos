import os
import matplotlib.pyplot as plt
import numpy as np

from .configuracoes import carregar_config_yaml
from .parametros import calcular_parametros
from .fisica.solver_1d import rodar_simulacao_1d


# Ajuste os caminhos caso tenha usado outros nomes de YAML
CASES = [
    ("Sem resfriamento",      "configs/caso_base.yaml"),
    ("Passivo (melhor h)",    "configs/resfriamento_passivo.yaml"),
    ("Ar forçado",            "configs/ar_forcado.yaml"),
    ("Água (resfriamento)",   "configs/agua_resfriamento.yaml"),
]


def rodar_caso(label: str, cfg_path: str):
    """Carrega config, calcula parâmetros e roda a simulação 1D."""
    if not os.path.exists(cfg_path):
        raise FileNotFoundError(f"Arquivo de config não encontrado: {cfg_path}")

    sim = carregar_config_yaml(cfg_path)
    params = calcular_parametros(sim)

    times, T_hist, eta_hist, _, _ = rodar_simulacao_1d(sim, params)

    # converter para unidades “bonitas”
    t_min = times / 60.0            # s -> min
    T_C = T_hist - 273.15           # K -> °C
    eta_pct = eta_hist * 100.0      # fração -> %

    return label, t_min, T_C, eta_pct


def main():
    resultados = []

    for label, cfg in CASES:
        print(f"Rodando caso: {label}  ({cfg})")
        label, t_min, T_C, eta_pct = rodar_caso(label, cfg)
        resultados.append((label, t_min, T_C, eta_pct))

    # garante pasta de saída
    os.makedirs("resultados", exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # --- Temperatura média ---
    ax_T = axes[0]
    for label, t_min, T_C, _ in resultados:
        ax_T.plot(t_min, T_C, label=label)
    ax_T.set_title("Temperatura média da placa")
    ax_T.set_xlabel("Tempo (min)")
    ax_T.set_ylabel("T média (°C)")
    ax_T.grid(True)
    ax_T.legend()

    # --- Eficiência média ---
    ax_eta = axes[1]
    for label, t_min, _, eta_pct in resultados:
        ax_eta.plot(t_min, eta_pct, label=label)
    ax_eta.set_title("Eficiência média da célula")
    ax_eta.set_xlabel("Tempo (min)")
    ax_eta.set_ylabel("Eficiência (%)")
    ax_eta.grid(True)
    ax_eta.legend()

    plt.tight_layout()
    out_path = "resultados/comparacao_4_casos.png"
    plt.savefig(out_path, dpi=200)
    print(f"Figura salva em {out_path}")
    plt.show()


if __name__ == "__main__":
    main()
