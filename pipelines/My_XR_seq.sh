#!/bin/bash

NAME=${1?Error: no name given}
NAME2=${2?Error: no name given}
# The NAME and NAME2 are the inputs for the pipeline, respectively. The NAME is using for Naming directory, file name and labelling whereas NAME2 is just for either labelling or raw file naming.

DIR="/cta/users/ardacetin/globalRepair/MelanomaPrediction/repair/XR-seqProtocolFile"

echo $(cd $DIR && mkdir $NAME)

cutadapt -a TGGAATTCTCGGGTGCCAAGGAACTCCAGTNNNNNNACGATCTCGTATGCCGTCTTCTGCTTG -o $DIR/$NAME/1_${NAME}_cutadapt.fastq /cta/users/ardacetin/globalRepair/MelanomaPrediction/repair/Merged_Raw_data/${NAME2}.fastq

bowtie2 -p 4 -x /cta/groups/adebali/data/reference_genomes/human/gencode/19/Bowtie2/genome -U $DIR/$NAME/1_${NAME}_cutadapt.fastq -S $DIR/$NAME/2_${NAME}_cutadapt.sam

samtools view -q 20 -b -o $DIR/$NAME/3_${NAME}_cutadapt.bam $DIR/$NAME/2_${NAME}_cutadapt.sam

bedtools bamtobed -i $DIR/$NAME/3_${NAME}_cutadapt.bam >$DIR/$NAME/4_${NAME}_cutadapt.bed

grep -r chr /cta/groups/adebali/data/reference_genomes/human/gencode/19/5kb2_copy_sorted.bed | grep -v "chrY" > $DIR/$NAME/5kb2_copy_edited.bed

sort -k1,1 -k2,2n $DIR/$NAME/5kb2_copy_edited.bed > $DIR/$NAME/5kb2_newsorted_genome.bed

rm $DIR/$NAME/5kb2_copy_edited.bed

grep -r chr $DIR/$NAME/4_${NAME}_cutadapt.bed | grep -v "chrY" > $DIR/$NAME/5_${NAME}_cutadapt_edited.bed

sort -u -k1,1 -k2,2n -k3,3n $DIR/$NAME/5_${NAME}_cutadapt_edited.bed >$DIR/$NAME/6_${NAME}_filtered_sorted.bed

awk '{print $3-$2}' $DIR/$NAME/6_${NAME}_filtered_sorted.bed | sort -k1,1n | uniq -c | sed 's/\s\s*/ /g' | awk '{print $2"\t"$1}'

#	Optional Step 1 to select reads having length 26: 
# Otherwise contiune with the 6_${NAME}_filtered_sorted.bed

awk '{ if ($3-$2 == 26) { print } }' $DIR/$NAME/6_${NAME}_filtered_sorted.bed > $DIR/$NAME/7_${NAME}_cutadapt_sorted_26.bed

#	Downsampling

#	The 7_${NAME}_cutadapt_sorted_26.bed is downlampled externally.

sort -k1,1 -k2,2n $DIR/$NAME/SPO_${NAME}_18M_Melsubsampled.bed > $DIR/$NAME/7_${NAME}_resorted.bed

bedtools intersect -sorted -a $DIR/$NAME/5kb2_newsorted_genome.bed -b $DIR/$NAME/7_${NAME}_resorted.bed -wa -c -F 0.5 > $DIR/$NAME/8_${NAME}_count-results.bed

grep -r chr $DIR/$NAME/8_${NAME}_count-results.bed | grep -v "chrY" > $DIR/$NAME/8_${NAME}_counts_edited.bed

sort -V -k1,1 -k2,2 $DIR/$NAME/8_${NAME}_counts_edited.bed > $DIR/$NAME/9_${NAME}_counts_doublesorted.bed

/cta/users/ardacetin/NGStoolkit/bin/addColumns.py -i $DIR/$NAME/9_${NAME}_counts_doublesorted.bed -o $DIR/$NAME/99_${NAME}_counts_edited_added.bed -c "XR-seq" "$1"

grep -c "^" $DIR/$NAME/99_${NAME}_counts_edited_added.bed > $DIR/$NAME/99_${NAME}_readCounts.bed
