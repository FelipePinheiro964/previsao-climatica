import argparse
import xarray as xr
from recortar_brasil import recortar_brasil #Pra pegar so a parte que a gente quer
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

if __name__ == "__main__":
  load_dotenv()

  parser = argparse.ArgumentParser()
  parser.add_argument("--arquivo", required=True)
  parser.add_argument("--variavel", required=True)
  parser.add_argument("--tabela", required=True, help="Nome da tabela no banco")
  args = parser.parse_args()

  ds = xr.open_dataset(args.arquivo)
  ds_brasil = recortar_brasil(ds)
  da = ds_brasil[args.variavel]

  df = da.to_dataframe().reset_index()

  antes = len(df)
  df = df.dropna(subset=[args.variavel])
  depois = len(df)

  usuario = os.environ["DB_USER"]
  senha = os.environ["DB_PASSWORD"]
  host = os.environ.get("DB_HOST", "localhost")
  porta = os.environ.get("DB_PORT", "5432")
  nome_banco = os.environ["DB_NAME"]

  url = f"postgresql+psycopg2://{usuario}:{senha}@{host}:{porta}/{nome_banco}"
  engine = create_engine(url)

  df.to_sql(args.tabela, engine, if_exists="append", index=False, chunksize=50000)

  print(f"Linhas antes do dropna: {antes}")
  print(f"Linhas depois (sem o oceano): {depois}")
  print(f"Tabela: {args.tabela}")
