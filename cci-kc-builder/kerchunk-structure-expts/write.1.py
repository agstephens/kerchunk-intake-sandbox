import json
import kerchunk.hdf
from kerchunk.combine import MultiZarrToZarr

file_uris = ["pre.nc"]
output_uri = "kc1.json"
inline_threshold = TD = 10

do_write = True

if do_write:
        single_indexes = []

        for file_uri in file_uris:
            print(f"[INFO] Processing: {file_uri}")
            single_indexes.append(
                kerchunk.hdf.SingleHdf5ToZarr(file_uri, file_uri, inline_threshold=TD).translate()
            )

        kwargs = {}
        concat_dims = ["time"]
        json_content = MultiZarrToZarr(single_indexes, concat_dims=concat_dims, **kwargs).translate()
        json_to_write = json.dumps(json_content, sort_keys=True, indent=4).encode()
        #import pdb; pdb.set_trace()

        with open(output_uri, "wb") as kc_file:
            kc_file.write(json_to_write)
            #json.dump(json_content, kc_file, sort_keys=True, indent=4)

        print(f"[INFO] Written file: {output_uri}")

