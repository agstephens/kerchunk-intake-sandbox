#!/usr/bin/env python
import kerchunk_tools.utils as kcu
import sys
for p in sys.argv[1:]:
    print(kcu.map_archive_path(p))

