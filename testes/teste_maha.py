from src.resfriamento_pv.configuracoes import DominioConfig
from src.resfriamento_pv.malha.malha_1d import criar_malha_1d


def test_criar_malha_1d():
    dominio = DominioConfig(L=0.01, nz=11)
    z, dz = criar_malha_1d(dominio)

    assert len(z) == 11
    assert abs(z[0] - 0.0) < 1e-12
    assert abs(z[-1] - 0.01) < 1e-12
    assert abs(dz - 0.001) < 1e-12
