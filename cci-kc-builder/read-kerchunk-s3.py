import sys
import time
import warnings
warnings.filterwarnings("ignore")
import json
import numpy as np
import kerchunk_tools.xarray_wrapper as wrap_xr

creds_file = "/home/users/astephens/kerchunk-intake-sandbox/s3_config.json"
s3_config = json.load(open(creds_file))

index_uri, var_id, startyear, endyear = sys.argv[1:5]

s = time.time()
ds = wrap_xr.wrap_xr_open(index_uri, s3_config=s3_config)
print(f"[INFO] Took {(time.time() - s):0.1f} seconds to read Kerchunk file.")

s = time.time()
mx = ds[var_id].sel(lat=slice(0, 40), lon=slice(0, 80), time=slice(f"{startyear}-01-01", f"{endyear}-03-01")).max()
fmx = float(mx)
print(f"[INFO] Took {(time.time() - s):0.1f} seconds to read the time slice from NetCDFs")

assert mx > -100000 and mx < 100000

print("[TEST PASSED] Tested and asserted data looks okay in Xarray!")

