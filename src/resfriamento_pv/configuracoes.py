from dataclasses import dataclass
from importlib.util import find_spec
from typing import Literal

if find_spec("yaml") is None:
    raise ModuleNotFoundError(
        "Dependência 'pyyaml' não encontrada. Instale com `pip install -r requirements.txt` ou `pip install pyyaml`."
    )

import yaml


@dataclass
class DominioConfig:
    L: float   # espessura total da placa (m)
    nz: int    # número de nós na direção y


@dataclass
class MaterialConfig:
    k: float   # W/m.K
    rho: float # kg/m³
    cp: float  # J/kg.K


@dataclass
class PVCellConfig:
    ref_efficiency: float   # eta_ref
    temp_coeff_beta: float  # beta (1/K)
    ref_temp_K: float       # T_ref (K)
    absorbing_thickness: float  # espessura efetiva da região que absorve G (m)



@dataclass
class BoundaryConditionsConfig:
    T_inf: float    # Temperatura ambiente (K)
    h_top: float    # W/m².K
    h_bottom: float # W/m².K
    G: float        # Irradiância solar (W/m²)
    epsilon_top: float = 0.85      # emissividade face superior
    epsilon_bottom: float = 0.85   # emissividade face inferior



@dataclass
class SimulationConfig:
    sim_name: str
    model_dim: int
    metodo_tempo: Literal["explicito", "implicito", "crank_nicolson"]
    t_final: float
    dt: float

    dominio: DominioConfig
    material: MaterialConfig
    pv_cell: PVCellConfig
    cc: BoundaryConditionsConfig


def carregar_config_yaml(path: str) -> SimulationConfig:
    """
    Lê um arquivo YAML e devolve um SimulationConfig
    compatível com os outros módulos.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    geral = data["GENERAL"]
    grid = data["GRID"]
    bc = data["BOUNDARY_CONDITIONS"]
    pv = data["PV_CELL"]
    mat = data["MATERIAL"]

    dominio = DominioConfig(
        L=grid["length_y"],
        nz=grid["nodes_y"],
    )

    material = MaterialConfig(
        k=mat["k"],
        rho=mat["rho"],
        cp=mat["cp"],
    )

    pv_cell = PVCellConfig(
        ref_efficiency=pv["ref_efficiency"],
        temp_coeff_beta=pv["temp_coeff_beta"],
        ref_temp_K=pv["ref_temp_K"],
        absorbing_thickness=pv.get("absorbing_thickness", grid["length_y"]),  # fallback = L
    )

    cc = BoundaryConditionsConfig(
        T_inf=bc["ambient_temp_K"],
        h_top=bc["h_top"],
        h_bottom=bc["h_bottom"],
        G=bc["irradiance_G"],
        epsilon_top=bc.get("epsilon_top", 0.85),
        epsilon_bottom=bc.get("epsilon_bottom", 0.85),
    )
    sim = SimulationConfig(
        sim_name=geral["sim_name"],
        model_dim=geral["model_dim"],
        metodo_tempo=geral.get("time_scheme", "implicito"),
        t_final=geral["final_time"],
        dt=geral["time_step_dt"],
        dominio=dominio,
        material=material,
        pv_cell=pv_cell,
        cc=cc,
    )

    return sim
