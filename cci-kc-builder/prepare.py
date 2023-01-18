#!/usr/bin/env python

import sys, os, glob
import pandas as pd


DATASETS_FILE = "datasets.csv"
VALIDATED_FILE = "datasets-prepared.csv"
FILE_LIST_DIR = "file-lists"
SUPPORTED_FILE_EXTENSIONS = [".nc"]


if not os.path.isdir(FILE_LIST_DIR):
    os.makedirs(FILE_LIST_DIR)


def _parse(datasets_file="datasets.csv"):
    df = pd.read_csv(datasets_file, sep=",\s+", engine="python", keep_default_na=False)
    df.rename(columns=lambda x: x.strip())
    return df


def get_size(file_list):
    return sum([os.path.getsize(fpath) for fpath in file_list]) / 2**30


def is_supported_file(fname):
    return any([fname.endswith(ext) for ext in SUPPORTED_FILE_EXTENSIONS])


def get_file_list(rec_id, pth):
    file_list_file = get_file_list_file(rec_id)

    if os.path.isfile(file_list_file):
        return open(file_list_file).read().split()

    # Treat glob differently
    if "*" in pth:
        return sorted(glob.glob(pth))

    file_list = []

    for dr, _, files in os.walk(pth):
        for fname in files:
            if is_supported_file(fname):
                file_list.append(f"{dr}/{fname}")

    return sorted(file_list)


def get_file_list_file(rec_id):
    return os.path.join(FILE_LIST_DIR, f"{rec_id}-file-list.txt")


def write_file_list(rec_id, file_list):
    outfile = get_file_list_file(rec_id)
    if os.path.isfile(outfile): return

    with open(outfile, "w") as writer:
        writer.write("\n".join(file_list))

    print(f"[INFO] Wrote: {outfile}")
 

def validate_and_prepare(rec):
    print(f"Validating: {rec['title']}")
    pth = rec["archive_path"]
    rec_id = rec["rec_id"]

    base_dir = pth.split("*")[0].rsplit("/", 1)[0]
    if not os.path.isdir(base_dir):
        print(f"[ERROR] Not valid directory: {base_dir}")

    file_list = get_file_list(rec_id, pth)

    if len(file_list) < 1:
        print(f"[ERROR] No files found for: {pth}")
        return

    size = get_size(file_list)
    print(f"[INFO] Size: {size:.2f}GB")

    write_file_list(rec_id, file_list)

    columns = list(rec.index)
    rec["size_gb"] = round(size, 2)
    rec["n_files"] = len(file_list)

    print(", ".join([str(rec[column]) for column in columns]), file=open(VALIDATED_FILE, "a"))


def main():
    df = _parse()
    print(", ".join([column for column in list(df.columns)]), file=open(VALIDATED_FILE, "w"))

    for _, rec in df.iterrows():
        validate_and_prepare(rec)

    print(f"[INFO] Wrote: {VALIDATED_FILE}")


if __name__ == "__main__":

    main()

