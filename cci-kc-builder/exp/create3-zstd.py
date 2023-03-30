import os
import json
import ujson
import fsspec
import kerchunk.hdf
from kerchunk.combine import MultiZarrToZarr


file_list_file = "file-list.txt"
file_uris = open(file_list_file).read().strip().split()
output_uri = "kc1-zstd.json.zstd"

if 1:
        single_indexes = []

        for file_uri in file_uris:
            print(f"[INFO] Processing: {file_uri}")
            single_indexes.append(
                kerchunk.hdf.SingleHdf5ToZarr(file_uri, file_uri, inline_threshold=100).translate()
            )

        s1 = single_indexes[0]
        for si in single_indexes[1:]:
            assert s1 != si

        kwargs = {}
        concat_dims = ["time"]
        storage_options = {"compression": True}

#with fsspec.open(filename, mode="wt", **(storage_options or {})) as f:
#                ujson.dump(out, f)
        json_content = MultiZarrToZarr(single_indexes, concat_dims=concat_dims, **kwargs) \
                       .translate() #storage_options=storage_options)
#        json_to_write = json.dumps(json_content).encode()

#        for fpath in file_uris:
#            assert fpath in str(json_to_write)
 
#        with open(output_uri, "wb") as kc_file:
#            kc_file.write(json_to_write)
#.zstd
        with fsspec.open(output_uri, mode="wt", compression="zstd") as f: #, **(storage_options or {})) as f:
            ujson.dump(json_content, f)

        print(f"[INFO] Written file: {output_uri}")


import xarray as xr
#zstd_file = fsspec.open(output_uri, mode="rt", compression="zstd").open()
#mapper = fsspec.get_mapper("reference://", fo=zstd_file) #output_uri, storage_options={"compression":"zst"})
#ds = xr.open_zarr(mapper)
ds = xr.open_zarr("reference://", storage_options={"fo": output_uri, "target_options": {"compression": "zstd"}})

print(ds)
assert len(ds.time) == 165
print(f"[INFO] Data looks okay in Xarray")

