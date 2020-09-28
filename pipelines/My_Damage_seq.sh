#!/bin/bash

#   $2 is the SRA to fastq converted input given to the pipeline, respectively. ın this code the fastq and cutadapt tools were utilized for paired-ended sample so, 
# if the datum is single-ended change the parameters accordingly.
#   The $1 is using for naming directory, file.

DIR="/cta/users/ardacetin/globalRepair/MelanomaPrediction/damageseq/damage-seqProtocolFile"
# Users should use their own fastq file location (PATH) instead of above exemplified DIR ("/cta/users/ardacetin/globalRepair/MelanomaPrediction/damageseq/damage-seqProtocolFile").

echo "Create directory at a given "DIR"
mkdir -p $DIR/$1

echo "Discard reads with adapter"
cutadapt --discard-trimmed -g GACTGGTTCCAATTGAAAGTGCTCTTCCGATCT -G GACTGGTTCCAATTGAAAGTGCTCTTCCGATCT -o $DIR/$1/1_${2}_cutadapt_1.fastq -p $DIR/$1/1_${2}_cutadapt_2.fastq /cta/users/ardacetin/globalRepair/MelanomaPrediction/damageseq/Raw_data/${2}_1.fastq /cta/users/ardacetin/globalRepair/MelanomaPrediction/damageseq/Raw_data/${2}_2.fastq

echo "Align with the reference genome"
bowtie2 -p 4 -x /cta/groups/adebali/data/reference_genomes/human/gencode/19/Bowtie2/genome -1 $DIR/$1/1_${2}_cutadapt_1.fastq -2 $DIR/$1/1_${2}_cutadapt_2.fastq -S $DIR/$1/2_${1}_cutadapt.sam

echo "Convert to bam"
samtools view -q 20 -b -o $DIR/$1/3_${1}_cutadapt.bam $DIR/$1/2_${1}_cutadapt.sam

echo "Convert to bed"
bedtools bamtobed -i $DIR/$1/3_${1}_cutadapt.bam > $DIR/$1/4_${1}_cutadapt.bed

echo "Remove undesired chromosome sets from the sample bed file"
grep -r chr $DIR/$1/4_${1}_cutadapt.bed | grep -v "chrY" > $DIR/$1/5_${1}_filtered.bed

echo "Sort bed file. Use -u to remove duplicates if necessary. Otherwide just use sort -k1,1 -k2,2n -k3,3n"
sort -u -k1,1 -k2,2n -k3,3n $DIR/$1/5_${1}_filtered.bed > $DIR/$1/6_${1}_cutadapt_sorted.bed

echo "Remove undesired chromosome sets from the reference genome"
grep -r chr /cta/groups/adebali/data/reference_genomes/human/gencode/19/5kb2_copy_sorted.bed | grep -v "chrY" > $DIR/$1/5kb2_copy_edited.bed

echo "Sort reference genome bed file"
sort -k1,1 -k2,2n $DIR/$1/5kb2_copy_edited.bed > $DIR/$1/5kb2_newsorted_genome.bed

echo "Remove old 5kb divided not sorted reference genome"
rm $DIR/$1/5kb2_copy_edited.bed

echo "Include only the reads having chromosomes in the sample data"
grep "chr" $DIR/$1/6_${1}_cutadapt_sorted.bed > $DIR/$1/7_${1}_cutadapt_sorted_chr.bed

echo "Getting plus and minus strands information"
awk '{if($6=="+"){print}}' $DIR/$1/7_${1}_cutadapt_sorted_chr.bed > $DIR/$1/7_${1}_cutadapt_sorted_plus.bed
awk '{if($6=="-"){print}}' $DIR/$1/7_${1}_cutadapt_sorted_chr.bed > $DIR/$1/7_${1}_cutadapt_sorted_minus.bed

echo "Finding exact damage position within 10bp long genome segment in three steps"
bedtools flank -i $DIR/$1/7_${1}_cutadapt_sorted_plus.bed -g /cta/groups/adebali/data/reference_genomes/human/gencode/19/genome.fa.fai -l 6 -r 0 > $DIR/$1/8_${1}_cutadapt_flanked_plus.bed
bedtools flank -i $DIR/$1/7_${1}_cutadapt_sorted_minus.bed -g /cta/groups/adebali/data/reference_genomes/human/gencode/19/genome.fa.fai -l 0 -r 6 > $DIR/$1/8_${1}_cutadapt_flanked_minus.bed

echo "Step 1"
bedtools slop -i $DIR/$1/8_${1}_cutadapt_flanked_plus.bed -g /cta/groups/adebali/data/reference_genomes/human/gencode/19/genome.fa.fai -l 0 -r +4 > $DIR/$1/8_${1}_cutadapt_slopped_plus.bed
bedtools slop -i $DIR/$1/8_${1}_cutadapt_flanked_minus.bed -g /cta/groups/adebali/data/reference_genomes/human/gencode/19/genome.fa.fai -l +4 -r 0 > $DIR/$1/8_${1}_cutadapt_slopped_minus.bed

echo "Step 2"
awk '{ if ($3-$2 == 10) { print } }' $DIR/$1/8_${1}_cutadapt_slopped_plus.bed > $DIR/$1/9_${1}_cutadapt_sorted_plus_10.bed
awk '{ if ($3-$2 == 10) { print } }' $DIR/$1/8_${1}_cutadapt_slopped_minus.bed > $DIR/$1/9_${1}_cutadapt_sorted_minus_10.bed

echo "Step 3"
bedtools getfasta -fi /cta/groups/adebali/data/reference_genomes/human/gencode/19/genome.fa -bed $DIR/$1/9_${1}_cutadapt_sorted_plus_10.bed -fo $DIR/$1/9_${1}_cutadapt_sorted_plus_10.fa -s
bedtools getfasta -fi /cta/groups/adebali/data/reference_genomes/human/gencode/19/genome.fa -bed $DIR/$1/9_${1}_cutadapt_sorted_minus_10.bed -fo $DIR/$1/9_${1}_cutadapt_sorted_minus_10.fa -s

echo "Keeping dipyrimidines in sample bed file"
/cta/users/ardacetin/NGStoolkit/bin/fa2bedByChoosingReadMotifs.py -i $DIR/$1/9_${1}_cutadapt_sorted_plus_10.fa -o $DIR/$1/10_${1}_cutadapt_sorted_plus_dipyrimidines.bed -r ".{4}(c|t|C|T){2}.{4}"
/cta/users/ardacetin/NGStoolkit/bin/fa2bedByChoosingReadMotifs.py -i $DIR/$1/9_${1}_cutadapt_sorted_minus_10.fa -o $DIR/$1/10_${1}_cutadapt_sorted_minus_dipyrimidines.bed -r ".{4}(c|t|C|T){2}.{4}"

#	    Downsampling

#	    The 10_${1}_cutadapt_sorted_plus_dipyrimidines.bed and 10_${1}_cutadapt_sorted_minus_dipyrimidines.bed are downsampled externally using a python script.

# adding more information 
moreinfo="$(grep $1 /cta/groups/adebali/data/repair/HeLa/DS/samples.csv | sed 's/,/\t/g')"
mappedReads="$(grep -c '^' $DIR/$1/6_${1}_cutadapt_sorted.bed)"

echo "Sort plus and minus sample bed files"
sort -k1,1 -k2,2n $DIR/$1/SPO_${1}_9M_plus_Melsubsampled.bed > $DIR/$1/10_${1}_cutadapt_doublesorted_plus_dipyrimidines.bed
sort -k1,1 -k2,2n $DIR/$1/SPO_${1}_9M_minus_Melsubsampled.bed > $DIR/$1/10_${1}_cutadapt_doublesorted_minus_dipyrimidines.bed

echo "Map plus and minus sample bed files on 5kb binned reference genome"
bedtools intersect -a $DIR/$1/5kb2_newsorted_genome.bed -b $DIR/$1/10_${1}_cutadapt_doublesorted_plus_dipyrimidines.bed $DIR/$1/10_${1}_cutadapt_doublesorted_minus_dipyrimidines.bed -wa -c -F 0.5 > $DIR/$1/11_${1}_cutadapt_sorted_dipyrimidines_1.bed

echo "Remove undesired chromosome sets from the sample mappled bed file if necessary"
grep -r chr $DIR/$1/11_${1}_cutadapt_sorted_dipyrimidines_1.bed | grep -v "chrY" > $DIR/$1/11_${1}_cutadapt_sorted_deleted_dipyrimidines.bed

echo "Add the NGS method and sample name labels"
/cta/users/ardacetin/NGStoolkit/bin/addColumns.py -i $DIR/$1/11_${1}_cutadapt_sorted_deleted_dipyrimidines.bed -o $DIR/$1/12_${1}_cutadapt_sorted_deleted_added_dipyrimidines.bed -c "Damage-seq" "$1"

# echo "To change the naming of a sample file to make it easily distinguisable one while still holding the old file"
cp  $DIR/$1/12_${1}_cutadapt_sorted_deleted_added_dipyrimidines.bed > $DIR/$1/13_${1}_cutadapt_plus-minus_mergedstrands.bed

echo "Count number of mapped reads"
grep -c "^" $DIR/$1/13_${1}_cutadapt_plus-minus_mergedstrands.bed > $DIR/$1/99_${1}_readCounts.bed
