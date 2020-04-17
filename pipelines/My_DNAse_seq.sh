#!/bin/bash

DIR="/cta/users/ardacetin/globalRepair/MelanomaPrediction/DNAseI/DNAse-seqProtocolFiles"

#	The NAME and NAME2 are the inputs for the pipeline, respectively. The NAME is using for Naming directory, file name and labelling whereas NAME2 is just for either labelling or raw file naming.

NAME=${1?Error: Nothing has been given as an input!}
NAME2=${2?Error: Nothing has been given as an input!}

echo $(cd $DIR && mkdir $NAME)

bowtie2 -p 4 -x /cta/groups/adebali/data/reference_genomes/human/gencode/19/Bowtie2/genome -U /cta/users/ardacetin/globalRepair/MelanomaPrediction/DNAseI/Raw_Data/$NAME/$NAME -S $DIR/$NAME/2_${NAME}.sam

samtools view -q 20 -b -o $DIR/$NAME/3_${NAME}.bam $DIR/$NAME/2_${NAME}.sam

bedtools bamtobed -i $DIR/$NAME/3_${NAME}.bam > $DIR/$NAME/4_${NAME}.bed

grep -r chr $DIR/$NAME/4_${NAME}.bed | grep -v "chrY" > $DIR/$NAME/4_${NAME}_edited.bed

grep -r chr /cta/groups/adebali/data/reference_genomes/human/gencode/19/5kb2_copy_sorted.bed | grep -v "chrY" > $DIR/$NAME/5kb2_copy_edited.bed

sort -k1,1 -k2,2n $DIR/$NAME/5kb2_copy_edited.bed > $DIR/$NAME/5kb2_newsorted_genome.bed

rm $DIR/$NAME/5kb2_copy_edited.bed

sort -u -k1,1 -k2,2n -k3,3n $DIR/$NAME/4_${NAME}_edited.bed > $DIR/$NAME/4_${NAME}_edited_sorted.bed

#	Downsampling

#	The 4_${NAME}_edited_sorted.bed is downlampled externally.

sort -k1,1 -k2,2n $DIR/$NAME/SPO_${NAME}_18M_Melsubsampled.bed > $DIR/$NAME/SPO_${NAME}_sorted_18M_Melsubsampled.bed

bedtools intersect -sorted -a $DIR/$NAME/5kb2_newsorted_genome.bed -b $DIR/$NAME/SPO_${NAME}_sorted_18M_Melsubsampled.bed -wa -c -F 0.5 > $DIR/$NAME/5_${NAME}_counts.bed

grep -r chr $DIR/$NAME/5_${NAME}_counts.bed | grep -v "chrY" > $DIR/$NAME/6_${NAME}_edited_counts.bed

sort -V -k1,1 -k2,2 $DIR/$NAME/6_${NAME}_edited_counts.bed > $DIR/$NAME/7_${NAME}_sorted.bed # This line is lastly added.
/cta/users/ardacetin/NGStoolkit/bin/addColumns.py -i $DIR/$NAME/7_${NAME}_sorted.bed -o $DIR/$NAME/8_${NAME}_edited_counts_added.bed -c "${NAME2}" "${NAME}"

grep -c "^" $DIR/$NAME/8_${NAME}_edited_counts_added.bed > $DIR/$NAME/9_${NAME}_readCounts.bed
