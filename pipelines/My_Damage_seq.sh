#!/bin/bash

#	$1 and $2 are the inputs given to the pipeline, respectively.

DIR="/cta/users/ardacetin/globalRepair/MelanomaPrediction/damageseq/damage-seqProtocolFile"

mkdir -p $DIR/$1

cutadapt --discard-trimmed -g GACTGGTTCCAATTGAAAGTGCTCTTCCGATCT -G GACTGGTTCCAATTGAAAGTGCTCTTCCGATCT -o $DIR/$1/1_${2}_cutadapt_1.fastq -p $DIR/$1/1_${2}_cutadapt_2.fastq /cta/users/ardacetin/globalRepair/MelanomaPrediction/damageseq/Raw_data/${2}_1.fastq /cta/users/ardacetin/globalRepair/MelanomaPrediction/damageseq/Raw_data/${2}_2.fastq

bowtie2 -p 4 -x /cta/groups/adebali/data/reference_genomes/human/gencode/19/Bowtie2/genome -1 $DIR/$1/1_${2}_cutadapt_1.fastq -2 $DIR/$1/1_${2}_cutadapt_2.fastq -S $DIR/$1/2_${1}_cutadapt.sam

samtools view -q 20 -b -o $DIR/$1/3_${1}_cutadapt.bam $DIR/$1/2_${1}_cutadapt.sam

bedtools bamtobed -i $DIR/$1/3_${1}_cutadapt.bam > $DIR/$1/4_${1}_cutadapt.bed

grep -r chr $DIR/$1/4_${1}_cutadapt.bed | grep -v "chrY" > $DIR/$1/5_${1}_filtered.bed

sort -u -k1,1 -k2,2n -k3,3n $DIR/$1/5_${1}_filtered.bed > $DIR/$1/6_${1}_cutadapt_sorted.bed

grep -r chr /cta/groups/adebali/data/reference_genomes/human/gencode/19/5kb2_copy_sorted.bed | grep -v "chrY" > $DIR/$1/5kb2_copy_edited.bed

sort -k1,1 -k2,2n $DIR/$1/5kb2_copy_edited.bed > $DIR/$1/5kb2_newsorted_genome.bed

rm $DIR/$1/5kb2_copy_edited.bed

grep "chr" $DIR/$1/6_${1}_cutadapt_sorted.bed > $DIR/$1/7_${1}_cutadapt_sorted_chr.bed

awk '{if($6=="+"){print}}' $DIR/$1/7_${1}_cutadapt_sorted_chr.bed > $DIR/$1/7_${1}_cutadapt_sorted_plus.bed
awk '{if($6=="-"){print}}' $DIR/$1/7_${1}_cutadapt_sorted_chr.bed > $DIR/$1/7_${1}_cutadapt_sorted_minus.bed

bedtools flank -i $DIR/$1/7_${1}_cutadapt_sorted_plus.bed -g /cta/groups/adebali/data/reference_genomes/human/gencode/19/genome.fa.fai -l 6 -r 0 > $DIR/$1/8_${1}_cutadapt_flanked_plus.bed
bedtools flank -i $DIR/$1/7_${1}_cutadapt_sorted_minus.bed -g /cta/groups/adebali/data/reference_genomes/human/gencode/19/genome.fa.fai -l 0 -r 6 > $DIR/$1/8_${1}_cutadapt_flanked_minus.bed

bedtools slop -i $DIR/$1/8_${1}_cutadapt_flanked_plus.bed -g /cta/groups/adebali/data/reference_genomes/human/gencode/19/genome.fa.fai -l 0 -r +4 > $DIR/$1/8_${1}_cutadapt_slopped_plus.bed
bedtools slop -i $DIR/$1/8_${1}_cutadapt_flanked_minus.bed -g /cta/groups/adebali/data/reference_genomes/human/gencode/19/genome.fa.fai -l +4 -r 0 > $DIR/$1/8_${1}_cutadapt_slopped_minus.bed

awk '{ if ($3-$2 == 10) { print } }' $DIR/$1/8_${1}_cutadapt_slopped_plus.bed > $DIR/$1/9_${1}_cutadapt_sorted_plus_10.bed
awk '{ if ($3-$2 == 10) { print } }' $DIR/$1/8_${1}_cutadapt_slopped_minus.bed > $DIR/$1/9_${1}_cutadapt_sorted_minus_10.bed

bedtools getfasta -fi /cta/groups/adebali/data/reference_genomes/human/gencode/19/genome.fa -bed $DIR/$1/9_${1}_cutadapt_sorted_plus_10.bed -fo $DIR/$1/9_${1}_cutadapt_sorted_plus_10.fa -s
bedtools getfasta -fi /cta/groups/adebali/data/reference_genomes/human/gencode/19/genome.fa -bed $DIR/$1/9_${1}_cutadapt_sorted_minus_10.bed -fo $DIR/$1/9_${1}_cutadapt_sorted_minus_10.fa -s

/cta/users/ardacetin/NGStoolkit/bin/fa2bedByChoosingReadMotifs.py -i $DIR/$1/9_${1}_cutadapt_sorted_plus_10.fa -o $DIR/$1/10_${1}_cutadapt_sorted_plus_dipyrimidines.bed -r ".{4}(c|t|C|T){2}.{4}"
/cta/users/ardacetin/NGStoolkit/bin/fa2bedByChoosingReadMotifs.py -i $DIR/$1/9_${1}_cutadapt_sorted_minus_10.fa -o $DIR/$1/10_${1}_cutadapt_sorted_minus_dipyrimidines.bed -r ".{4}(c|t|C|T){2}.{4}"

#	Downsampling

#	The 10_${1}_cutadapt_sorted_plus_dipyrimidines.bed and 10_${1}_cutadapt_sorted_minus_dipyrimidines.bed are downlampled externally.

# adding more information 

moreinfo="$(grep $1 /cta/groups/adebali/data/repair/HeLa/DS/samples.csv | sed 's/,/\t/g')"
mappedReads="$(grep -c '^' $DIR/$1/6_${1}_cutadapt_sorted.bed)"

# intersecting 5kb windows 
#	Continue with downsapled data bed files.

sort -k1,1 -k2,2n $DIR/$1/SPO_${1}_9M_plus_Melsubsampled.bed > $DIR/$1/10_${1}_cutadapt_doublesorted_plus_dipyrimidines.bed

sort -k1,1 -k2,2n $DIR/$1/SPO_${1}_9M_minus_Melsubsampled.bed > $DIR/$1/10_${1}_cutadapt_doublesorted_minus_dipyrimidines.bed

bedtools intersect -a $DIR/$1/5kb2_newsorted_genome.bed -b $DIR/$1/10_${1}_cutadapt_doublesorted_plus_dipyrimidines.bed $DIR/$1/10_${1}_cutadapt_doublesorted_minus_dipyrimidines.bed -wa -c -F 0.5 > $DIR/$1/11_${1}_cutadapt_sorted_dipyrimidines_1.bed

grep -r chr $DIR/$1/11_${1}_cutadapt_sorted_dipyrimidines_1.bed | grep -v "chrY" > $DIR/$1/11_${1}_cutadapt_sorted_deleted_dipyrimidines.bed

# Labelling Columns

/cta/users/ardacetin/NGStoolkit/bin/addColumns.py -i $DIR/$1/11_${1}_cutadapt_sorted_deleted_dipyrimidines.bed -o $DIR/$1/12_${1}_cutadapt_sorted_deleted_added_dipyrimidines.bed -c "Damage-seq" "$1"

# combining both strands in a bed and txt file

cp  $DIR/$1/12_${1}_cutadapt_sorted_deleted_added_dipyrimidines.bed > $DIR/$1/13_${1}_cutadapt_plus-minus_mergedstrands.bed

grep -c "^" $DIR/$1/13_${1}_cutadapt_plus-minus_mergedstrands.bed > $DIR/$1/99_${1}_readCounts.bed