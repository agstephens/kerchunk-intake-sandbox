import fsspec
import xarray as xr

uris = ["kc1.json", "kc3.json"]

def load(fpath):
  mapper = fsspec.get_mapper("reference://", fo=fpath)
  ds = xr.open_zarr(mapper)
  return ds

ds1, ds2 = [load(uri) for uri in uris]
assert ds1.equals(ds2)
print(f"[INFO] Data matches.")

