#!/bin/bash

mode=$1
input_file=$2
project=$3

if [[ ! "$mode" =~ (cloud|files) ]]; then
    echo "[ERROR] First argument must be 'cloud' or 'files'"
    exit
fi

if [ ! -f "$input_file" ]; then
    echo "[ERROR] Second argument must a valid CSV file."
    exit
fi


#input_file=datasets-prepared.csv
file_list_dir=file-lists
max_bytes=500
#prefix="outputs/kc-indexes/cloud"

prefix=kc-indexes-${project}
kc_paths_file=kc-paths.txt
cache_dir=/gws/nopw/j04/cedaproc/astephens/KERCHUNK-CACHE-CLOUD
creds_file=../s3_config.json
#rm -f $kc_paths_file


while read ROW; do

    if [[ $ROW =~ rec_id, ]] ; then #|| [[ ! $ROW =~ POC ]]; then # || [[ $ROW =~ 9km ]] || [[ $ROW =~ BICEP-PC-MERGED-MONTHLY ]] ; then
        echo "[DEBUG] Ignoring row: ${ROW}"
        continue
    fi

    echo "[INFO] Working on: $ROW"
    rec_id=$(echo $ROW | cut -d, -f1 | sed 's/ //g')

    file_list_file=${file_list_dir}/${rec_id}-file-list.txt

    creds_args=""

    if [ $mode == "cloud" ]; then
        file_uris_file=${file_list_dir}/${rec_id}-uri-list.txt
        ./map-paths-from-list.py $file_list_file $file_uris_file

        creds_arg="-c $creds_file"
    fi

    echo "[INFO] Found: $(wc -l $file_list_file) files"
    dsid=$rec_id

    kc_file="${dsid}.json"

    _cmd="kerchunk_tools create -p $prefix -o $kc_file -b $max_bytes $creds_arg -C $cache_dir -f $file_uris_file"

    time $_cmd

    if [ $? -eq 0 ]; then
        echo "[INFO] Adding index path to: $kc_paths_file"
        echo ${prefix}/${kc_file} >> $kc_paths_file
    fi

done < $input_file

echo 
echo "[INFO] Wrote the following kerchunk files to: $kc_paths_file"

