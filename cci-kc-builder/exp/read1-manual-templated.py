import fsspec
import xarray as xr


output_uri = "kc1-manual-templated.json"
mapper = fsspec.get_mapper("reference://", fo=output_uri)
ds = xr.open_zarr(mapper)

print(ds)
assert len(ds.time) == 165
print(f"[INFO] Data looks okay in Xarray")
