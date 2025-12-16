import sys
import time

from .configuracoes import carregar_config_yaml
from .parametros import calcular_parametros
from .fisica.solver_1d import rodar_simulacao_1d
from .visualizacao import plot_results


def main(config_path: str):
    sim = carregar_config_yaml(config_path)
    params = calcular_parametros(sim)

    print(f"Iniciando simulação: {sim.sim_name}")
    t0 = time.time()

    times, T_hist, eta_hist, T_final = rodar_simulacao_1d(sim, params)

    print(f"Simulação concluída em {time.time() - t0:.2f} s")
    plot_results(times, T_hist, eta_hist, T_final, sim)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python -m src.resfriamento_pv.main_run configs/caso_base.yaml")
    else:
        main(sys.argv[1])
