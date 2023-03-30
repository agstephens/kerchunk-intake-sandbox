import os
import json
import ujson
import fsspec
import kerchunk.hdf
from kerchunk.combine import MultiZarrToZarr


file_list_file = "../file-lists/BICEP-OEP-MERGED-MONTHLY-v1.0-file-list.txt"
file_uris = open(file_list_file).read().strip().split()[:5]
output_uri = "kc4-zstd-BICEP.json.zstd"

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

        json_content = MultiZarrToZarr(single_indexes, concat_dims=concat_dims, **kwargs) \
                       .translate()

        with fsspec.open(output_uri, mode="wt", compression="zstd") as f:
            ujson.dump(json_content, f)

        print(f"[INFO] Written file: {output_uri}")


import xarray as xr
ds = xr.open_zarr("reference://", storage_options={"fo": output_uri, "target_options": {"compression": "zstd"}})

print(ds)
assert len(ds.time) == 5
print(f"[INFO] Data looks okay in Xarray")

