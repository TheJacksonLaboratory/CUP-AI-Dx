# CUP-AI-Dx

CUP-AI-Dx is a deep-learning tool to infer a tumor's primary tissue of origin from its transcriptional signature.

## Getting Started
These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes. 

## Prerequisites

Note that the program requires the use of a computer system with NVIDIA GPUs and the
appropriate CUDA libraries available.

The python environment required to run these scripts is listed in `conda.txt`.
You can recreate the required environment with
```
conda env create -f conda.yml -n tcga-gpu
```
To activate this environment, use
```
conda activate tcga-gpu
```

## Source data

Before running, you need to `bunzip2` the datasets in the `data/` directory.
```
bzip2 -kd data/ExternalDataMeta.csv.bz2
 ```

To generate the data yourself from scratch, TBD.

## Running the primary classifier code

To run the external validation with pre-built models from the script directory, you can do
the following:
```
python3 external_test.py metastatic --model <model-name>
```
In general, this script accepts a few commandline arguments:
```
python3 external_test.py \
    metastatic \ # you can specify multiple external validation datasets listed with `--help`
    --data-dir "path/to/data" \ # default is `$(pwd)/data`
    --model inception \ # default is `inception`
    --models-dir "path/to/models" \ # default is `$(pwd)/models`
```
Once finished, the primary classifier will give the overall accuracy and top5 accuracy pridiction results on the screen directly. Other results including by class performance and confusion matrix are stored in the auto-generated `output/` directory.

## Running the subtype classifier code
For breast cancer validation, please run:

```
Rscript run_subtype_validation.R breast_cancer <output-dir>
```

For ovarian validation data, please run:
```
Rscript run_subtype_validation.R ovarian_cancer <output-dir>
```



