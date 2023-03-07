#!/bin/bash

mode=$1
project=$2

DEFAULT_VERSION=2
version=${3:-${DEFAULT_VERSION}}

# Check arguments
[[ ! "$mode" =~ (cloud|files) ]] && echo "[ERROR] First argument must be 'cloud' or 'files'." && exit
[[ ! "$project" =~ (era5|cci) ]] && echo "[ERROR] Second argument must be one of (era5|cci)." && exit
[[ ! "$version" =~ v.* ]] && version=v${version} 

input_file=datasets-validated-${project}-${version}.csv
file_list_dir=file-lists/${project}/${version}
max_bytes=500

prefix=kc-indexes-${project}-${mode}-${version}
cache_dir=/gws/nopw/j04/cedaproc/astephens/KERCHUNK-CACHE-$(echo $mode | tr [:lower:] [:upper:])
creds_file=../s3_config.json

IGNORES=iwontmatch
IGNORES='ESACCI|BICEP-OEP|BICEP-PC|BICEP-POC'

while read ROW; do

    if [[ $ROW =~ (rec_id,|${IGNORES}) ]] ; then 
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

        creds_arg="-s $creds_file"
    else
        file_uris_file=$file_list_file
    fi

    # Set compression of kerchunk files
    compression="-c zstd"

    echo "[INFO] Found: $(wc -l $file_list_file) files"
    dsid=$rec_id

    kc_file="${dsid}.zstd"

    _cmd="kerchunk_tools create -p $prefix -o $kc_file -b $max_bytes $creds_arg $compression -C $cache_dir -f $file_uris_file"

    time $_cmd

done < $input_file

echo "[INFO] All done!"

