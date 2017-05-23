#!/bin/bash

python_dir=$PWD 

cd ../../sql/postgres/psycopg2

psycopg_dir=$PWD

for file in $psycopg_dir/*; do
    echo "Creating symlink for ${file##*/}"
    ln -s $psycopg_dir/${file##*/} $python_dir
done


