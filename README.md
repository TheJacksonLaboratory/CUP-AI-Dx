# ai4cancer

Description Placeholder

## Getting Started
These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes. 

## Prerequisites

The python environment required to run these scripts is listed in `conda.txt`.
You can recreate it with
```
conda create -f conda.txt -n tcga-gpu
```

Note that this requires the use of a computer system with NVIDIA GPUs and the
appropriate CUDA libraries available.

## Running the primary classifier code

Currently, the only available code is external validation with pre-built
models.  To run the external validation from the script directory, you can do
the following:
```
python3 external_validation.py metastatic
```
In general, this script accepts a few commandline arguments:
```
python3 external_validation.py \
    metastatic \ # you can specify multiple external validation datasets listed with `--help`
    --data-dir "path/to/data" \ # default is `$(pwd)/data`
    --model inception \ # default is `inception`
    --models-dir "path/to/models" \ # default is `$(pwd)/models`
```

## Running the subtype classifier code

TBD

## Source data

TBD
