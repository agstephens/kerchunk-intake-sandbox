import fsspec
import xarray as xr

output_uri = "kc3.json"

if 1:
  mapper = fsspec.get_mapper("reference://", fo=output_uri)
  ds = xr.open_zarr(mapper)
  print(list(ds.variables.keys()))
  assert len(ds.time) == 12
  print(f"[INFO] Data looks okay in Xarray")
