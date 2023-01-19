import sys
import warnings
warnings.filterwarnings("ignore")
import json
import numpy as np
import kerchunk_tools.xarray_wrapper as wrap_xr

creds_file = "../s3_config.json"
s3_config = json.load(open(creds_file))

sys.argv.append("")
index_uri = sys.argv[1] or "s3://kc-indexes/BICEP-OC-L3S-PP-MERGED-1M_MONTHLY_9km_mapped-1998-2020-fv4.2.json"
ds = wrap_xr.wrap_xr_open(index_uri, s3_config=s3_config)

mx = ds.pp.sel(lat=slice(0, 40), lon=slice(0, 80), time=slice("1998-01-01", "1998-03-01")).max()
assert np.round(float(mx), 2) == 4671.38

print("[TEST PASSED] Tested and asserted data looks okay in Xarray!")

