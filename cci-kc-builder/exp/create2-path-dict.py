import os
import json
import fsspec
import kerchunk.hdf
from kerchunk.combine import MultiZarrToZarr


file_list_file = "file-list.txt"
file_uris = open(file_list_file).read().strip().split()
output_uri = "kc2.json"

if 1:
        single_indexes = []

        for file_uri in file_uris:
            print(f"[INFO] Processing: {file_uri}")
            single_indexes.append(
                kerchunk.hdf.SingleHdf5ToZarr(file_uri, inline_threshold=500).translate()
            )

        #assert single_indexes[0]["templates"]["u"] == file_uris[0]
        #import pdb; pdb.set_trace()
        kwargs = {}
        concat_dims = ["time"]

        print("ARGS REQUIRE 'indicts', available from KERCHUNK 0.1.0!!!!")
        single_dicts = [{furi: index_json} for furi, index_json in zip(file_uris, single_indexes)]
        #import pdb; pdb.set_trace()

        json_content = MultiZarrToZarr(path=file_uris, indicts=single_indexes, concat_dims=concat_dims, **kwargs).translate()
        json_to_write = json.dumps(json_content).encode()

        with open(output_uri, "wb") as kc_file:
            kc_file.write(json_to_write)

        print(f"[INFO] Written file: {output_uri}")

