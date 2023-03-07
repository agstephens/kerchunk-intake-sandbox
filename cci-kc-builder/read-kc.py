import sys
import warnings
warnings.filterwarnings("ignore")
import json
import numpy as np
import kerchunk_tools.xarray_wrapper as wrap_xr

sys.argv.append("")
index_uri = sys.argv[1] or "/home/users/astephens/kerchunk-intake-sandbox/cci-kc-builder/kc-indexes-cci-v2/BICEP-OC-L3S-PP-MERGED-1M_MONTHLY_9km_mapped-1998-2020-fv4.2.zstd"
ds = wrap_xr.wrap_xr_open(index_uri)

mx = ds.pp.sel(lat=slice(0, 40), lon=slice(0, 80), time=slice("1998-01-01", "1998-03-01")).max()
assert np.round(float(mx), 2) == 4671.38

print("[TEST PASSED] Tested and asserted data looks okay in Xarray!")

