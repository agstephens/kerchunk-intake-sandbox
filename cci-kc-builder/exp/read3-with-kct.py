from kerchunk_tools import xarray_wrapper as xw

zstd_kc = "kc1-zstd.json.zstd"
json_kc = "kc1.json"

ds1 = xw.wrap_xr_open(zstd_kc)
ds2 = xw.wrap_xr_open(json_kc)

print(ds1)
print(ds2)


assert ds1.equals(ds2)

