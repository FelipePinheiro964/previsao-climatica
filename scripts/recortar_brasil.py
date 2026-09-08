import xarray as xr

def recortar_brasil(ds):
  """
  Recorta o dataset global para a area aproximada do Brasil
  """
  return ds.sel(lat=slice(-34, 6), lon=slice(286, 326))


if __name__ == "__main__":
  ds = xr.open_dataset("data/raw/amostra.nc")
  ds_brasil = recortar_brasil(ds)
  print(ds_brasil)
  print(f"Tamanho original: {ds.nbytes / 1e6:.1f} MB")
  print(f"Tamanho recortado: {ds_brasil.nbytes / 1e6:.1f} MB")
  