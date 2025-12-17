# Resfriamento de placas fotovoltaicas 1D

Simulador 1D de transferência de calor em placas fotovoltaicas com geração interna
de calor pela célula. O código lê um arquivo YAML com propriedades físicas e
condições de contorno e integra no tempo o perfil de temperatura na espessura da
placa.

## Métodos temporais disponíveis
- **Implicito (Backward Euler)**: estável para passos maiores; `time_scheme: "implicito"`.
- **Explícito (Forward Euler)**: novo esquema que avança as equações de forma
  explícita, tratando convecção e radiação nas faces também de maneira
  explícita. Exige `Fo <= 0.5` para estabilidade. Ative com `time_scheme: "explicito"`.

## Como rodar
```bash
python -m src.resfriamento_pv.main_run configs/caso_base.yaml
```
Ajuste `configs/*.yaml` para alterar propriedades ou o método temporal.
