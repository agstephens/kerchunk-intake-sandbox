from kerchunk_tools.indexer import Indexer as IX
from kerchunk_tools import xarray_wrapper as xw

file_list_file = "file-list.txt"
file_uris = open(file_list_file).read().strip().split()
jkc = "index.json"
zkc = "index.zstd"

x = IX()
x.create(file_uris, prefix="test1", output_path=jkc, compression=None, max_bytes=-1)
x.create(file_uris, prefix="test1", output_path=zkc, compression="zstd", max_bytes=-1)

tzkc = f"test1/{zkc}"
tjkc = f"test1/{jkc}"

ds1 = xw.wrap_xr_open(tzkc, compression="zstd")
ds2 = xw.wrap_xr_open(tzkc, compression="infer")
ds3 = xw.wrap_xr_open(tjkc)
ds4 = xw.wrap_xr_open(tjkc, compression=None)

print(ds1)
print(ds2)

for n, ds in enumerate([ds2, ds3, ds4]):
    print("Comparing", n + 1)
    assert ds1.equals(ds)


