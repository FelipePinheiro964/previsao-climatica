"""
Explora o bucket público do NEX-GDDP-CMIP6 na AWS (Amazon S3).

Acesso ANÔNIMO (--no-sign-request / signature_version=UNSIGNED):
não usa, não precisa e não deve receber nenhuma credencial da AWS.
Por isso este script pode ir pro GitHub sem risco de vazar chave nenhuma
— não há chave em lugar nenhum do código.

Estrutura real do bucket (descoberta explorando com Delimiter="/"):
    s3://nex-gddp-cmip6/NEX-GDDP-CMIP6/<modelo>/<cenario>/r1i1p1f1/<variavel>/*.nc
"""

import argparse
import boto3
from botocore import UNSIGNED
from botocore.config import Config

BUCKET = "nex-gddp-cmip6"
BASE_PREFIX = "NEX-GDDP-CMIP6/" # Pasta raiz real dentro do bucket

def get_client():
  # UNSIGNED = sem credenciais
  return boto3.client("s3", config=Config(signature_version=UNSIGNED))

def listar_modelos(client):
  
  """
  Docstring for listar_modelos
  (ex: ACESS-CM2) dentro do bucket
  """

  resp = client.list_objects_v2(Bucket=BUCKET, Prefix=BASE_PREFIX, Delimiter="/")
  return [p["Prefix"] for p in resp.get("CommonPrefixes", [])]

def listar_arquivos(client, model, scenario, variable, max_itens=20):

  """
  Lista os arquivos .nc de um modelo/cenario/variavel especifico
  """

  prefix = f"{BASE_PREFIX}{model}/{scenario}/r111p1f1/{variable}/"
  resp = client.list_objects_v2(Bucket=BUCKET, Prefix=prefix, MaxKeys=max_itens)
  return [obj["Key"] for obj in resp.get("Contents", [])]


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--model", default=None, help="Ex: ACCESS-CM2")
  parser.add_argument("--scenario", default="historical")
  parser.add_argument("--variable", default="pr")
  args = parser.parse_args()

  client = get_client()

  if not args.model:
    print("Modelo disponiveis: ")
    for m in listar_modelos(client):
      print(" -", m)

  else:
    print(f"Arquivos para {args.model}/{args.scenario}/{args.variable}:") 
    for key in listar_arquivos(client, args.model, args.scenario, args.variable):
      print(" -", key) 