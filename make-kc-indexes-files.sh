#!/bin/bash

max_bytes=50000
prefix="outputs/kc-indexes/files"
kc_paths_file=kc-paths.txt
rm -f $kc_paths_file


while read dr; do

    echo "[INFO] Working on $dr"
    echo "[INFO] Found $(ls $dr/*.nc | wc -l) files"

    dsid=$(echo $dr | sed 's|/badc/cmip6/data/||' | sed 's|/|\.|g')

    kc_file="${dsid}.json"

#    echo "[WARN] Running on first 3 files only"
#    filepaths=$(ls $dr/*.nc | head -3)
    filepaths=${dr}/*.nc
 
    _cmd="kerchunk_tools create -p $prefix -o $kc_file -b $max_bytes -C ${HOME}/KERCHUNK-CACHE $filepaths"
    echo "[INFO] Running: $_cmd"

    time $_cmd

    if [ $? -eq 0 ]; then
        echo "[INFO] Adding index path to: $kc_paths_file"
        echo ${prefix}/${kc_file} >> $kc_paths_file
    fi

done < pathlist.txt

echo 
echo "[INFO] Wrote the following kerchunk files to: $kc_paths_file"

