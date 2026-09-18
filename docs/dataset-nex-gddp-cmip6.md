### Resultado da checagem (amostra: pr, ACCESS-CM2, historical, 1950)

- 26,76% dos pontos do recorte retangular são NaN.
- Confirmado visualmente (máscara plotada) que o NaN corresponde a
  oceano (Atlântico a leste, Pacífico na faixa oeste) e não a falha
  sobre terra — o recorte usado é um retângulo lat/lon, não o contorno
  real do Brasil, então inclui território de países vizinhos e mar.
- Nenhum valor de `pr` fora do intervalo físico plausível [0, 0.01] kg/m²/s.
- Contagem de dias (365 para 1950, ano não bissexto) confere.
- Conclusão: os dados sobre terra estão íntegros; o alto % de NaN é
  esperado e não indica problema de qualidade da fonte.

## Variáveis definidas (fechado)

- `tas` — temperatura média diária (K)
- `tasmax` — temperatura máxima diária (K)
- `tasmin` — temperatura mínima diária (K)
- `pr` — precipitação (kg/m²/s)

Validado com amostra real (ACCESS-CM2, historical, 1950): tas e pr
conferidos sem inconsistências de faixa física; tasmax/tasmin assumidos
consistentes por virem da mesma pipeline/fonte, a confirmar no primeiro
download real de cada.

## Resolução espacial e temporal (fechado)

- Confirmado via amostra real: grade 0.25° (25km), 600×1440 pontos globais, frequência diária.
- Comparação entre modelos diferentes não é aplicável: o NEX-GDDP-CMIP6 usa
  bias correction/spatial disaggregation (BCSD) para reprojetar todos os 34
  modelos disponíveis para o mesmo grid de 0.25° e mesma frequência diária,
  não é uma propriedade que varia modelo a modelo dentro deste dataset.
  Fonte: documentação técnica do NEX-GDDP-CMIP6 (NASA NCCS / Thrasher et al. 2022).
- Resolução validada como consistente entre variáveis do mesmo modelo (pr e tas).

## Decisão: Earth Engine em vez de Databricks

Avaliado Databricks e descartado: no plano gratuito, o acesso de saída à
internet é restrito a domínios confiáveis (não garante acesso ao bucket S3
da NASA) e há cota de uso que pode pausar o compute no meio de um job grande.

Vamos seguir com o Google Earth Engine: o NEX-GDDP-CMIP6 já está hospedado
lá (`NASA/GDDP-CMIP6`), e a média sobre o Brasil é calculada no servidor do
Google — sem baixar os arquivos brutos, resolvendo o problema de banda/peso
na raiz.

Setup do Earth Engine ainda não foi feito, deve levar um tempo pra configurar
(conta, projeto, lib `earthengine-api`). Enquanto isso, espaço em disco local
foi liberado, então não há mais urgência de espaço — só a urgência de tempo
de download que motivou essa avaliação.
