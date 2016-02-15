#!/bin/bash
if [[ $1 == *"created"* ]]
then
    echo "File changed: $2"

    path_alone=`echo $2 | sed -e 's/[^/]*\.py//g'`
    file_wo_path=`echo $2 | sed -e 's/.*\///g'`

    spec_file=$path_alone
    spec_file+="spec/spec_$file_wo_path"
    if [[ -e $spec_file ]]
    then
        echo "Running spec: $spec_file..."
        mamba $spec_file
    else
        echo "Running spec: $2"
        mamba $2
    fi
fi

