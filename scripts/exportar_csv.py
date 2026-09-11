import argparse
import xarray as xr
from recortar_brasil import recortar_brasil #Pra pegar so a parte que a gente quer

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--arquivo", required=True)
  parser.add_argument("--variavel", required=True)
  parser.add_argument("--saida", required=True)
  args = parser.parse_args()

  ds = xr.open_dataset(args.arquivo)
  ds_brasil = recortar_brasil(ds)
  da = ds_brasil[args.variavel]

  df = da.to_dataframe().reset_index()

  antes = len(df)
  df = df.dropna(subset=[args.variavel])
  depois = len(df)

  df.to_csv(args.saida, index=False)

  print(f"Linhas antes do dropna: {antes}")
  print(f"Linhas depois (sem o oceano): {depois}")
  print(f"CSV salvo em: {args.saida}")
