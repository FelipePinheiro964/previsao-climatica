import argparse
import boto3
from botocore import UNSIGNED
from botocore.config import Config

BUCKET = "nex-gddp-cmip6"

def get_client():
  return boto3.client("s3", config=Config(signature_version=UNSIGNED))

def listar_modelos(client):
  resp = client.list_objects_v2(Bucket=BUCKET, Delimiter="/")
  return [p["Prefix"].rstrip("/") for p in resp.get("CommonPrefixes", [])]

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--model", default=None, help="Ex: ACESS-CM2")
  parser.add_argument("--scenario", default="historical")
  parser.add_argument("--variavle", default="pr")
  args = parser.parse_args()

  client = get_client()

  if not args.model:
    print("Modelo disponiveis: ")
    for m in listar_modelos(client):
      print(" -", m)

  else:
    print(f"Arquivos para {args.model}/{args.scenario}/{args.variable}:") 
    for key in listar_modelos(client, args.model, args.scenario, args.variable):
      print(" -", key) 