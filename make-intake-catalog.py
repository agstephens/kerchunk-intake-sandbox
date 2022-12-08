#!/usr/bin/env python 

import os
import sys
import pandas as pd

columns = [
        "project",
        "activity_id",
        "source_id",
        "institution_id",
        "experiment_id",
        "member_id",
        "table_id",
        "variable_id",
        "grid_label",
        "version",
        "uri",
        "format"
]


def parse_args():
    kc_paths_file, intake_file = sys.argv[1:]
    return kc_paths_file, intake_file

def prepare_dir(dr):
    if not os.path.isdir(dr):
        os.makedirs(dr)

def create_intake():
    kc_paths_file, intake_file = parse_args() 
    # eg: kc-indexes/files/CMIP6.CMIP.CCCma.CanESM5.historical.r1i1p1f1.Oyr.o2.gn.latest.json

    kc_paths = open(kc_paths_file).read().strip().split()
    data = [os.path.basename(kc_path).split(".")[:-1] + [kc_path, "reference"] for kc_path in kc_paths]
 
    df = pd.DataFrame(data, columns=columns)
    prepare_dir(os.path.dirname(intake_file))
    df.to_csv(intake_file, index=False)

    print(f"[INFO] Wrote: {intake_file}")


if __name__ == "__main__":
    create_intake()

