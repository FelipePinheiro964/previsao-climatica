"""
Checa valores ausentes e inconsistencias fisicas no arquivo recortado
do Brasil. Primeira variavel: pr (precipitacao).
"""

import numpy as np
import xarray as xr
from recortar_brasil import recortar_brasil
import matplotlib.pyplot as plt


def checar_ausentes(da):
    """Conta quantos valores sao NaN e qual % isso representa."""
    total = da.size
    ausentes = int(da.isnull().sum())
    pct = 100 * ausentes / total
    return ausentes, total, pct


def checar_faixa_fisica(da, minimo, maximo, nome_variavel):
    """
    Verifica se existem valores fora do intervalo fisico plausivel.
    Para 'pr' (precipitacao em kg/m2/s), nao deveria haver negativos.
    """
    fora_da_faixa = da.where((da < minimo) | (da > maximo), drop=False)
    qtd_fora = int((~fora_da_faixa.isnull()).sum())
    if qtd_fora > 0:
        print(f"[ALERTA] {nome_variavel}: {qtd_fora} valores fora de [{minimo}, {maximo}]")
        print(f"  min encontrado: {float(da.min())}, max encontrado: {float(da.max())}")
    else:
        print(f"[OK] {nome_variavel}: nenhum valor fora de [{minimo}, {maximo}]")
    return qtd_fora


if __name__ == "__main__":
    ds = xr.open_dataset("data/raw/amostra.nc")
    ds_brasil = recortar_brasil(ds)

    pr = ds_brasil["pr"]

    ausentes, total, pct = checar_ausentes(pr)
    print(f"Valores ausentes (NaN): {ausentes} de {total} ({pct:.4f}%)")

    # precipitacao (kg/m2/s) nunca deveria ser negativa;
    # limite superior generoso so pra pegar erro grosseiro de leitura
    checar_faixa_fisica(pr, minimo=0, maximo=0.01, nome_variavel="pr")

    # checar timestamps: 1950 tem 365 dias (nao e bissexto)
    dias_esperados = 365
    dias_reais = ds_brasil.dims["time"]
    if dias_reais != dias_esperados:
        print(f"[ALERTA] Esperava {dias_esperados} dias, encontrado {dias_reais}")
    else:
        print(f"[OK] {dias_reais} dias, como esperado para 1950")
        dia_exemplo = pr.isel(time=0)
    mascara_nan = dia_exemplo.isnull()

    plt.figure(figsize=(8, 8))
    mascara_nan.plot()
    plt.title("Mascara de valores ausentes (pr) - 1950-01-01")
    plt.savefig("data/processed/mascara_nan_exemplo.png")
    print("Grafico salvo em data/processed/mascara_nan_exemplo.png")