#!/bin/bash

input_file=datasets-prepared.csv
file_list_dir=file-lists
max_bytes=50000
#prefix="outputs/kc-indexes/cloud"

prefix=kc-indexes
kc_paths_file=kc-paths.txt
cache_dir=/gws/nopw/j04/cedaproc/astephens/KERCHUNK-CACHE
creds_file=../s3_config.json
rm -f $kc_paths_file


while read ROW; do

    if [[ $ROW =~ rec_id, ]] ; then
        echo "[DEBUG] Ignoring row: ${ROW}"
        continue
    fi

    echo "[INFO] Working on: $ROW"
    rec_id=$(echo $ROW | cut -d, -f1 | sed 's/ //g')

    file_list_file=${file_list_dir}/${rec_id}-file-list.txt
    file_uris=$(./map-paths.py $(cat ${file_list_file}))

#file_uris=$(./map-paths.py $(head -3 ${file_list_file}))
#echo $file_uris

    echo "[INFO] Found: $(wc -l $file_list_file) files"
    dsid=$rec_id

    kc_file="${dsid}.json"

    _cmd="kerchunk_tools create -p $prefix -o $kc_file -b $max_bytes -c $creds_file -C $cache_dir $file_uris"
#    echo "[INFO] Running: $_cmd"

    time $_cmd

    if [ $? -eq 0 ]; then
        echo "[INFO] Adding index path to: $kc_paths_file"
        echo ${prefix}/${kc_file} >> $kc_paths_file
    fi
    exit

done < $input_file

echo 
echo "[INFO] Wrote the following kerchunk files to: $kc_paths_file"
