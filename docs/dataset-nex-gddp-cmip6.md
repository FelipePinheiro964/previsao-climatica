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
