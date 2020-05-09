#!/bin/sh

image=$1

rm -rf test_dir/processing/output
mkdir -p test_dir/processing/output

docker run -v $(pwd)/test_dir:/opt/ml --rm ${image} preprocessing.py
