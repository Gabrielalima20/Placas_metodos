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
Antes de rodar pela primeira vez, instale as dependências:
```bash
pip install -r requirements.txt
```
Se o comando falhar com `ModuleNotFoundError: No module named 'yaml'`,
significa que o pacote `pyyaml` não foi instalado; o passo acima resolve.

Ajuste `configs/*.yaml` para alterar propriedades ou o método temporal.

### Comparar explícito vs. implícito
Para gerar um gráfico comparando o perfil de temperatura e a eficiência obtidos
pelos dois esquemas temporais no mesmo caso base:
```bash
python -m src.resfriamento_pv.compare_metodos configs/caso_base.yaml
```
O comando cria `resultados/comparacao_metodos.png` com as curvas lado a lado.
Se o esquema explícito precisar de um passo de tempo menor para respeitar
`Fo <= 0.5`, o script reduz automaticamente `dt` para o limite estável e avisa
no terminal; para rodar apenas o solver explícito manualmente, ajuste `dt` no
YAML conforme necessário.
