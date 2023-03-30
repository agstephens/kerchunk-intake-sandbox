import os
import json
import fsspec
import kerchunk.hdf
from kerchunk.combine import MultiZarrToZarr


file_list_file = "file-list.txt"
file_uris = open(file_list_file).read().strip().split()
output_uri = "kc1.json"

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

        #assert si["templates"]["u"] == file_uris[0]
        #import pdb; pdb.set_trace()
        kwargs = {}
        concat_dims = ["time"]
        json_content = MultiZarrToZarr(single_indexes, concat_dims=concat_dims, **kwargs).translate()
        json_to_write = json.dumps(json_content).encode()

        for fpath in file_uris:
            assert fpath in str(json_to_write)
 
        with open(output_uri, "wb") as kc_file:
            kc_file.write(json_to_write)

        print(f"[INFO] Written file: {output_uri}")


import xarray as xr
mapper = fsspec.get_mapper("reference://", fo=output_uri)
ds = xr.open_zarr(mapper)

print(ds)
assert len(ds.time) == 165
print(f"[INFO] Data looks okay in Xarray")
