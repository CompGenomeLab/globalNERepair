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
To reach the original page for NGStoolkit, you can visit [Ogun Adebali Github page](https://github.com/adebali/NGStoolkit).

##  Work with your own data
Below, instructions are exemplified based on "XR-seq pipeline editing" but they are also valid for other three NGS methods as well.

Irrespective of the any NGS methods (XR-seq, damage-seq, DNase-seq, or ChIP-seq) for preprocessing you should move your .fastq file into the data directory.

Edit the My_XR-seq.sh and replace the SAMPLE variable with the base sample name in your file. For example if you file is named as myFile.fastq the base name will be myFile.

If you want to retrieve the existing data set from SRA please see the fastq-dump command and replace the SRA acccession number with the one of interest. If you use your own file please comment out that two lines in My_XR-seq.sh.

In the project, un-subsampled and subsampled version of the data were used. The subsampling threshold was determined based on the total number of reads coming from the raw sequencing data and subsampling performed completely randomly. The python package "random" was used. Since each line represents a genomic coordinate and corresponding genetic information inside the .BED files, a python script selecting random rows was run and new subsampled_BED files was used for for the further experiements.

_"sample"_ is a build-in python package which accepts dataframe.

```
seed_num = 1
sampling = 2458200

ran_sampled = data.sample(n=sampling, random_state=seed_num)

```
To reach the original page for  random package, you can visit [Python Documantation page](https://docs.python.org/3/library/random.html).

# Gene Annotation
For retrieveing the hg19 gtf file manually [link] (ftp://ftp.ensembl.org/pub/grch37/release-98/gtf/homo_sapiens/Homo_sapiens.GRCh37.87.gtf.gz)

File name is _Homo_sapiens.GRCh37.87.gtf.gz_

There are various ways to retrieve the data but personally best bets in terms of easiness and conciseness would be:

Using wget:
```
import wget

gtf_link = 'ftp://ftp.ensembl.org/pub/grch37/release-98/gtf/homo_sapiens/Homo_sapiens.GRCh37.87.gtf.gz'
wget.download(gtf_link)

```

Using urllib2:
```
import urllib2

gtf_req = urllib2.Request('ftp://ftp.ensembl.org/pub/grch37/release-98/gtf/homo_sapiens/Homo_sapiens.GRCh37.87.gtf.gz')
web_response = urllib2.urlopen(gtf_req)
the_page = response.read()

```

After downloading or directly reading the gtf file at the desired _"PATH"_, if necessary extract the gtf file using:

```
from sh import gunzip

gunzip('/content/Homo_sapiens.GRCh37.87.gtf.gz')
```

Then, you can apply the _Genes_Intergenes_ python script in order to get the exact data we have obtained and used for data analysis in the research or you can use this script and chage it depending on your research purpose. 

The script has an extension _".ipynb"_ meaning that it was written in the Jupyter Notebooks using google coolab. The purpose of usng the google coolab was its convenience in storing data at Google Drive and avaialability of writting and running codes seperately and seeing outputs nicely and continously.

If you want to work on the "_Genes_Intergenes.ipynb_" as a python file, you can convert it using:

First install required packages and follow the guide:
```
pip install ipynb-py-convert
```

Then run the below line of code:
```
ipynb-py-convert examples/plot.ipynb examples/plot.py
```

Or you may want to convert python script into a Jupyter Notebook file use:
```
ipynb-py-convert examples/plot.py examples/plot.ipynb
```


This will turn markdown text into multiline strings ' _'''_ ' format. Moreover, after the conversion each Jupyter Notebooks cell as a "normal" python code line will have a marker "_# %%_". This indicates that until reaching another marker, all the codes within two markers previously belong in a single Jupyter Notebook cell.

# Caution
The pipelines and scripts were not for general usage purposes, they have been developed for achieving specific purpose hence, the line of codes can vary depending on the purpose.

Even for reproducing the same experiements, you should be carefull to apply same pipelines or scripts for different sort of cell lines types. Although, four pipelines were used in the preprocessing of four NGS data (Xr-seq, damage-seq, DNase-seq, and ChIP-seq), within each pipeline the parameters for the tool commands varied. For example, you should aware whether the NGS datum layout is paired-ended or single-ended. Besides, you need to know wheter you should trimm or remove the adaptors completely from the data. 

Also, depending on the sequencing data quality, deduplicates might need to be removed and for those who would like to test the reprocubility of our work, please try to apply the same steps as much as possible. The most important difference could emerge at performing the subsampling step. Please read "Work wşth you owd data" section above to get the idea.

##  Authors
Arda Cetin
