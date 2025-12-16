import matplotlib.pyplot as plt
import numpy as np
from ..configuracoes import SimulationConfig


def plot_results(times, T_history, eta_history, T_profile, sim: SimulationConfig):
    sim_name = sim.sim_name

    times = np.array(times)
    T_avg_C = np.array(T_history) - 273.15
    eta_pct = np.array(eta_history) * 100

    fig, ax = plt.subplots(1, 3, figsize=(18, 5))

    # 1. Temperatura média vs tempo
    ax[0].plot(times / 60.0, T_avg_C)
    ax[0].set_title("Temperatura média da placa")
    ax[0].set_xlabel("Tempo (min)")
    ax[0].set_ylabel("T média (°C)")
    ax[0].grid(True)

    # 2. Eficiência média vs tempo
    ax[1].plot(times / 60.0, eta_pct)
    ax[1].set_title("Eficiência média da célula")
    ax[1].set_xlabel("Tempo (min)")
    ax[1].set_ylabel("Eficiência (%)")
    ax[1].grid(True)

    # 3. Perfil final de temperatura na espessura
    depth_mm = np.linspace(0, sim.dominio.L * 1000, len(T_profile))
    ax[2].plot(depth_mm, T_profile - 273.15, marker="o")
    ax[2].set_title(f"Perfil T (t = {times[-1]/60:.1f} min)")
    ax[2].set_xlabel("Posição na espessura (mm)")
    ax[2].set_ylabel("T (°C)")
    ax[2].grid(True)

    plt.tight_layout()
    plt.savefig(f"resultados/resultado_{sim_name}.png", dpi=200)
    print(f"Gráfico salvo em resultados/resultado_{sim_name}.png")
    plt.show()
