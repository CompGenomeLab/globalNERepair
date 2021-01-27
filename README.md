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

# Research Protocol

You should know what sam, bam, and bed files are. [Too learn click](http://software.broadinstitute.org/software/igv/?q=book/export/html/16)
To retrieve all the NGS data utilzied in the research please see the _Data_ section [below].

1. Run XR-seq, ChIP-seq, DNase-seq, and damage-seq pipelines with appropriate PATH and file names.

* In each pipeline, should be run from top to bottom for once to create the outputs. Then, the second run should performed but this time just before getting read count numbers (before the _bedtools intersect_) subsample your corresponding file according to the minimum read number which should be determined by looking through all the sequencing files' read numbers. Here, you need to check all XR-seq, ChIP-seq, DNase-seq, and damage-seq raw reads to see which file has the smallest read coverage in other words number of reads.

2. Downsampling should be applied on all the files except the one having the lowest read count (see Python_scripts directory and _Work with your own data_ headings at the [README](https://github.com/CompGenomeLab/globalNERepair/edit/master/README.md) page). The number of read sampling value should equal to the file including the smallest number of reads.
 
* After downsampling the corresponding ".BED" file, find read overlaps using the subsampled data and continue to apply exact same steps as your first run.
 
3. Convert read count values to RPKM values.

4. Collect the outputs of the each sequencing pipeline for filtering and normalizing.

* Remove rows which are having zero RPKM value from the  damage-seq files, then normalize repair by damage.
* Each row of XR-seq RPKM value should be divided by its corresponding RPKM row of the related damage-seq file.
** Each repair and its relavent damage type (UV damage types: Cisplatin, (6-4)PP) must be filtered and normalized during the filtering step.
** e.g    XR-seq-(6-4)PP-repA / damage-seq-(6-4)PP-repA    XR-seq-(6-4)PP-repB / damage-seq-(6-4)PP-repB    XR-seq-Cisplatin-repA / damage-seq-Cisplatin-repA   and etc.

5. Lastly, create a dataframe in which each column will be chromosome_name, position_start, position_end, XR-seq, damage-seq, ChIP-seq, and DNase-seq RPKM values, sequentially.

* In most cases, there will be technical and/or biological repliciates of each sequencing in this case they should be sequentially followed. 
** e.g    (6-4)PP_Repair_damage_normalized_repA   (6-4)PP_Repair_damage_normalized_RepB   (6-4)PP_Repair_damage_normalized_RepC   and so on.


# Gene Annotation
For retrieveing the hg19 gtf file manually please go to the link below:
ftp://ftp.ensembl.org/pub/grch37/release-98/gtf/homo_sapiens/

and download the file with a name:

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

# [create an anchor](#Data)
The ChIP-seq data used in the project can be retrieved using the given ENCODE IDs.

_Image_

In GM12878, damage-seq and XR-seq 1.5hr data can be retrieved from GSE98025 and GSE82213, respectively. NHF1 cell line’s XR-seq data generated after one-hour UV exposure are from GSE67941 and DNA repair after four hours XR-seq data are from GSE76391. The both 1- and 4-hours UV treatment data on NHF1 cells line could be accessed at GSE98025.

The DNaseseq data for the HeLa and GM12878 cell lines can be accessed from GSE32970 and GSE32970, sequentially. The DNase-seq datum for the normal skin fibroblast cell
line (NHDF) can be retrieved from GEO ID GSE2969.

# Caution
The pipelines and scripts were not for general usage purposes, they have been developed for achieving specific purpose hence, the line of codes can vary depending on the purpose.

Even for reproducing the same experiements, you should be carefull to apply same pipelines or scripts for different sort of cell lines types. Although, four pipelines were used in the preprocessing of four NGS data (Xr-seq, damage-seq, DNase-seq, and ChIP-seq), within each pipeline the parameters for the tool commands varied. For example, you should aware whether the NGS datum layout is paired-ended or single-ended. Besides, you need to know wheter you should trimm or remove the adaptors completely from the data. 

Also, depending on the sequencing data quality, deduplicates might need to be removed and for those who would like to test the reprocubility of our work, please try to apply the same steps as much as possible. The most important difference could emerge at performing the subsampling step. Please read "Work wşth you owd data" section above to get the idea.

##  Authors
Arda Cetin
