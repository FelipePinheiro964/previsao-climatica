"""
Checa valores ausentes e inconsistencias fisicas no arquivo recortado
do Brasil. Primeira variavel: pr (precipitacao).
"""

import argparse
import xarray as xr
from recortar_brasil import recortar_brasil



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
        print(f"Atenção na variavel{nome_variavel}: {qtd_fora} valores fora de [{minimo}, {maximo}]")
        print(f"  min encontrado: {float(da.min())}, max encontrado: {float(da.max())}")
    else:
        print(f"Variavel ok {nome_variavel}: nenhum valor fora de [{minimo}, {maximo}]")
    return qtd_fora


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--arquivo", required=True, help="Caminho do .nc local")
    parser.add_argument("--variavel", required=True)
    parser.add_argument("--minimo", type=float, required=True)
    parser.add_argument("--maximo", type=float, required=True)
    args = parser.parse_args()
   
    ds = xr.open_dataset(args.arquivo)
    ds_brasil = recortar_brasil(ds)
    da = ds_brasil[args.variavel]

    ausentes, total, pct = checar_ausentes(da)
    print(f"Valores ausentes (NaN): {ausentes} de {total} ({pct:.4f}%)")

    checar_faixa_fisica(da, args.minimo, args.maximo, args.variavel)

    dias_esperados = 365
    dias_reais = ds_brasil.sizes["time"]
    if dias_reais != dias_esperados:
        print(f"Menor numero de dias encontrados no dataset: dias esperados {dias_esperados}, dias encontrados {dias_reais}")
