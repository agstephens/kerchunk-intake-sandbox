#!/bin/bash

input_file=datasets-prepared.csv
file_list_dir=file-lists
max_bytes=50000
prefix="outputs/kc-indexes/files"
kc_paths_file=kc-paths.txt
cache_dir=/gws/nopw/j04/cedaproc/astephens/KERCHUNK-CACHE
rm -f $kc_paths_file


while read ROW; do

    if [[ $ROW =~ rec_id, ]] ; then
        echo "[DEBUG] Ignoring row: ${ROW}"
        continue
    fi

    echo "[INFO] Working on: $ROW"
    rec_id=$(echo $ROW | cut -d, -f1 | sed 's/ //g')

    file_list_file=${file_list_dir}/${rec_id}-file-list.txt
    file_uris=$(cat ${file_list_file})

    echo "[INFO] Found: $(wc -l $file_list_file) files"
    dsid=$rec_id

    kc_file="${dsid}.json"

    _cmd="kerchunk_tools create -p $prefix -o $kc_file -b $max_bytes -C $cache_dir $file_uris"
#    echo "[INFO] Running: $_cmd"

    time $_cmd

    if [ $? -eq 0 ]; then
        echo "[INFO] Adding index path to: $kc_paths_file"
        echo ${prefix}/${kc_file} >> $kc_paths_file
    fi

done < $input_file

echo 
echo "[INFO] Wrote the following kerchunk files to: $kc_paths_file"
