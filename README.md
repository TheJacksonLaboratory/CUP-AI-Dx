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

## Running new data set prediction on a docker container

A docker container has been built so that the users can use the tool easily. The code should be runnable on any machine as long as docker is installed. Especially no package installation is required.

After installing docker, please run the following command in the terminal to pull the container from dockerhub:

```
docker pull yuz12012/ai4cancer:product
docker run -it yuz12012/ai4cancer:product
```

After container loads (probably you will see something like '(base) [root@9f6c7ef6f851 /]'), please do the following in the container:

```
conda activate tf-cpu
cd /scripts/
python RunPrediction.py --data_set=data/ExternalDataMeta.csv
```

where the 'data/ExternalDataMeta.csv' represents the new data file to predict. The data file is a csv file with the columns names of 'X' + entrez gene ids. The order doesn't matter since code will rearrange the columns based on a feature column (saved in data/features_40_median_icgc_tcga.csv of the container) predefined. 
But please include all the feature genes in the data csv file. In order to import the data into the container, one can use 'docker cp' command to copy your data into the container. If the data is too big, please consider mounting your data directory into the container. For more detailed information, please check docker documentation.
Note that the model is trained with log2(TPM+1) data, thus ideally the new data set should be preprocessed in the same way.

The prediction should take seconds and the cancer label predicted and probabilities of each prediction are saved in output/prediction_'data-file-name'.csv and output/prediction_prob_'data-file-name'.csv respectively.
For example, the output from the example command will be 'prediction_data_ExternalDataMeta.csv' and 'prediction_prob_data_ExternalDataMeta.csv'.

Good luck and have fun.









