import numpy as np
from ..configuracoes import DominioConfig


def criar_malha_1d(dominio: DominioConfig):
    """
    Gera a malha 1D na espessura [0, L] com nz nós igualmente espaçados.
    """
    L = dominio.L
    nz = dominio.nz

    z = np.linspace(0.0, L, nz)  # inclui 0 e L
    dz = z[1] - z[0]

    return z, dz
