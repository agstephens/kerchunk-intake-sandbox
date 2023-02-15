#!/usr/bin/env python
import kerchunk_tools.utils as kcu
import sys

fin, fout = sys.argv[1:3]
files = open(fin).read().strip().split()

with open(fout, "w") as writer:
    for p in files:
        uri = kcu.map_archive_path(p)
        writer.write(uri + "\n")



