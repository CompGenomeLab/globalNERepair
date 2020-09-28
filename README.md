This repository is developed for analyzing genome-wide four NGS datasets which I have utilized during my master's thesis. This repository is not only including preprocessing pipelines but also includes python scripts as well.

# Project Aim
Revealing one of the causes of genome-wide nucleotide excision repair heterogeneitiy mainly using histone markers.

# globalNERepair
Instead of globalRepair Repository, I am using globalNERepair repository!

###  This repository includes globalRepair project's scripts and pipelines.
For pipelines, please visit "pipelines" folder.

For Scripts, please visit "Python_Scripts" folder.

##  Setup
Custom setup assumes that you have the necessary programs installed and they are exectuble in your $PATH.

The list of the necessary programs are:

Bowtie2
cutadapt
sra toolkit
samtools
bedtools
ucsc tools
NGStoolkit

In order to download and run the NGStoolkit, the direction are taken by the author of this toolkit Ogun Adebali, PhD.
>To place the source code of this repository in your path, please follow these commands:

```
cd ~
git clone git@bitbucket.org:adebali/NGStoolkit.git
cd NGStoolkit
bash setup.sh
```
To reach the original page for NGStoolkit, you can visit [Ogun Adebali Github page] (https://github.com/adebali/NGStoolkit).

##  Work with your own data
Below, instructions are exemplified based on "XR-seq pipeline editing" but they are also valid for other three NGS methods as well.

Irrespective of the any NGS methods (XR-seq, damage-seq, DNase-seq, or ChIP-seq) for preprocessing you should move your .fastq file into the data directory.

Edit the My_XR-seq.sh and replace the SAMPLE variable with the base sample name in your file. For example if you file is named as myFile.fastq the base name will be myFile.

If you want to retrieve the existing data set from SRA please see the fastq-dump command and replace the SRA acccession number with the one of interest. If you use your own file please comment out that two lines in My_XR-seq.sh.

# Caution
The pipelines and scripts were not for general usage purposes, they have been developed for achieving specific purpose hence, the line of codes can vary depending on the purpose.

Even for reproducing the same experiements, you should be carefull to apply same pipelines or scripts for different sort of cell lines types. Although, four pipelines were used in the preprocessing of four NGS data (Xr-seq, damage-seq, DNase-seq, and ChIP-seq), within each pipeline the parameters for the tool commands varied. For example, you should aware whether the NGS datum layout is paired-ended or single-ended. 

Also, depending on the sequencing data quality, deduplicates might need to be removed.

##  Authors
Arda Cetin
