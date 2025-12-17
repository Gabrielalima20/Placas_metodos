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


def plot_temperature_map(times, T_profile_history, sim: SimulationConfig):
    """Cria um mapa tempo x espessura da temperatura (°C)."""

    if T_profile_history is None or len(T_profile_history) == 0:
        return

    times = np.array(times)
    T_profile_history = np.array(T_profile_history)

    times_min = times / 60.0
    depth_mm = np.linspace(0, sim.dominio.L * 1000, T_profile_history.shape[1])
    temp_C = T_profile_history - 273.15

    fig, ax = plt.subplots(figsize=(10, 6))
    mesh = ax.pcolormesh(
        depth_mm,
        times_min,
        temp_C,
        shading="auto",
        cmap="inferno",
    )
    cbar = plt.colorbar(mesh, ax=ax)
    cbar.set_label("Temperatura (°C)")

    ax.set_title("Mapa de temperatura na espessura")
    ax.set_xlabel("Posição na espessura (mm)")
    ax.set_ylabel("Tempo (min)")

    plt.tight_layout()
    out_path = f"resultados/mapa_temperatura_{sim.sim_name}.png"
    plt.savefig(out_path, dpi=200)
    print(f"Mapa de temperatura salvo em {out_path}")
    plt.show()
