"""
Baixa UM arquivo de amostra do NEX-GDDP-CMIP6 (S3, acesso anonimo) e
inspeciona sua estrutura com xarray. Objetivo: confirmar dimensoes,
resolucao e como aparecem valores ausentes, antes de decidir download
em maior escala.
"""

import argparse
import os
import boto3
from botocore import UNSIGNED
from botocore.config import Config
import xarray as xr

BUCKET = "nex-gddp-cmip6"

def baixar(key, destino):
  client = boto3.client("s3", config=Config(signature_version=UNSIGNED))
  os.makedirs(os.path.dirname(destino), exist_ok=True)
  client.download_file(BUCKET, key, destino)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--key", required=True, help="Caminho do arquivo bucket")
  parser.add_argument("--destino", default="data/raw/amostra.nc")
  args = parser.parse_args()

  print(f"Baixando {args.key}")
  baixar(args.key, args.destino)
  print("Download concluido. Abrindo xarray")

  ds = xr.open_dataset(args.destino)
  print(ds)