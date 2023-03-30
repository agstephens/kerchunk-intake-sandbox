import json
import sys
from collections import Counter
import time

f = (sys.argv[1:] or ["cci-cloud-v2-BICEP-OC-L3S-PP-MERGED-1M_MONTHLY_9km_mapped-1998-2020-fv4.2.json"])[0]

s = time.time()
with open(f) as reader:
    data = json.load(reader)

print(f"Parsed JSON file in: {(time.time() - s):.01f} seconds.")

refs = data["refs"]

print(f"Number of refs: {len(refs)}\n")

prefixes = Counter([ref.split("/")[0] for ref in refs])

print("Counts of prefixes in refs...")
for prefix, count in prefixes.most_common():
  print(f"{prefix}: {count}")


