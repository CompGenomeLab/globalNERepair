#!/bin/bash

NAME=${1?Error: Nothing has been given as an input!}
NAME2=${2?Error: Nothing has been given as an input!}
# The NAME is the SRA to fastq converted inputs for the pipeline, respectively. The NAME is using for Naming directory, 
#file name and labelling whereas NAME2 is just for either labelling or raw file naming.

DIR="/cta/users/ardacetin/globalRepair/MelanomaPrediction/chipseq/ChIP-seqProtocolFile"
# Users should use their own fastq file location (PATH) instead of above exemplified DIR ("/cta/users/ardacetin/globalRepair/MelanomaPrediction/chipseq/ChIP-seqProtocolFile").

echo "Create directory at a given "DIR"
echo $(cd $DIR && mkdir $NAME)

echo "Align with the reference genome"
bowtie2 -p 4 -x /cta/groups/adebali/data/reference_genomes/human/gencode/19/Bowtie2/genome -U /cta/users/ardacetin/globalRepair/MelanomaPrediction/chipseq/Merged_Raw_data/$NAME -S $DIR/$NAME/2_${NAME}.sam

echo "Convert to bam"
samtools view -q 20 -b -o $DIR/$NAME/3_${NAME}.bam $DIR/$NAME/2_${NAME}.sam

echo "Convert to bed"
bedtools bamtobed -i $DIR/$NAME/3_${NAME}.bam > $DIR/$NAME/4_${NAME}.bed

echo "Remove undesired chromosome sets from the sample bed file"
grep -r chr $DIR/$NAME/4_${NAME}.bed | grep -v "chrY" > $DIR/$NAME/4_${NAME}_edited.bed

echo "Remove undesired chromosome sets from the reference genome"
grep -r chr /cta/groups/adebali/data/reference_genomes/human/gencode/19/5kb2_copy_sorted.bed | grep -v "chrY" > $DIR/$NAME/5kb2_copy_edited.bed

echo "Sort reference genome bed file"
sort -k1,1 -k2,2n $DIR/$NAME/5kb2_copy_edited.bed > $DIR/$NAME/5kb2_newsorted_genome.bed

echo "Remove old 5kb divided not sorted reference genome"
rm $DIR/$NAME/5kb2_copy_edited.bed

echo "Sort bed file. Use -u to remove duplicates if necessary. Otherwide just use sort -k1,1 -k2,2n -k3,3n"
sort -u -k1,1 -k2,2n $DIR/$NAME/4_${NAME}_edited.bed > $DIR/$NAME/4_${NAME}_edited_sorted.bed

#	Downsampling

#	The 4_${NAME}_edited_sorted.bed is downlampled externally using a python script.

echo "Sort sample bed file"
sort -k1,1 -k2,2n $DIR/$NAME/SPO_${NAME}_18M_Melsubsampled.bed > $DIR/$NAME/SPO_${NAME}_sorted_18M_Melsubsampled.bed

echo "Map sample bed file on 5kb binned reference genome"
bedtools intersect -sorted -a $DIR/$NAME/5kb2_newsorted_genome.bed -b $DIR/$NAME/SPO_${NAME}_sorted_18M_Melsubsampled.bed -wa -c -F 0.5 > $DIR/$NAME/5_${NAME}_counts.bed

echo "Remove undesired chromosome sets from the sample mappled bed file if necessary"
grep -r chr $DIR/$NAME/5_${NAME}_counts.bed | grep -v "chrY" > $DIR/$NAME/6_${NAME}_edited_counts.bed

echo "Sort sample bed file alphanumerically"
sort -V -k1,1 -k2,2 $DIR/$NAME/6_${NAME}_edited_counts.bed > $DIR/$NAME/7_${NAME}_sorted.bed

echo "Add the NGS method and sample name labels"
/cta/users/ardacetin/NGStoolkit/bin/addColumns.py -i $DIR/$NAME/7_${NAME}_sorted.bed -o $DIR/$NAME/8_${NAME}_edited_counts_added.bed -c "${NAME2}" "${NAME}"

echo "Count number of mapped reads"
grep -c "^" $DIR/$NAME/8_${NAME}_edited_counts_added.bed > $DIR/$NAME/9_${NAME}_readCounts.bed
