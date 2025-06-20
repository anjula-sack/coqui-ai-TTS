#!/bin/bash

# Take the script's parent's directory to prefix all the output paths
RUN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo $RUN_DIR

# Download OpenSLR Sinhala dataset
wget -q https://www.openslr.org/resources/30/si_lk.tar.gz

# Prepare dataset directory
mkdir -p sinhala_dataset/wav

# Extract the tar.gz into the wav directory
tar -xzf si_lk.tar.gz --directory sinhala_dataset/wav

# Create train-val splits
shuf sinhala_dataset/si_lk.lines.txt > sinhala_dataset/metadata_shuf.csv

# Move to recipe folder
mv sinhala_dataset "$RUN_DIR/recipes/pathnirvana/"
mv metadata_shuf.csv "$RUN_DIR/recipes/pathnirvana/sinhala_dataset/"

# Clean up
rm si_lk.tar.gz
