import json
import sys

fpath = sys.argv[1]
#fpath = "/gws/nopw/j04/cedaproc/astephens/KERCHUNK-CACHE/kc-indexes/ESACCI-LST-L3C-LST-MODISA-0.01deg_1DAILY_DAY-20031225000000-fv3.00.nc.json"
j = json.load(open(fpath))

