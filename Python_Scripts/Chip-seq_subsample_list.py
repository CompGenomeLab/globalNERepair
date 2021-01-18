import pandas as pd
import os

#################################################
# All ChIP-seq files should be at the same directory.
path = '/cta/users/ardacetin/globalRepair/MelanomaPrediction/chipseq/ChIP-seqProtocolFile_4hr/'    # Path where the created files will be.
histones = ["SRR227397_SRR227398.fastq","SRR227579_SRR227580.fastq","SRR568344_SRR568345.fastq"]   # ChIP-seq file name labels, in this case they are SRR IDs.
subsample_n = 17573000        # The number of reads which will be randomly picked.
Min_read_number = 17572461    # The minimum tolerated read number for a file for not involving in downsampling process.
##################################################


for histone in histones:
	os.system("grep -c '^' " + path + histone + "/4_" + histone + "_edited_sorted.bed > " + path + histone + "/5_" + histone + "_counts.txt") # Find read numbers.
	
	fl = open(path + histone + "/5_" + histone + "_counts.txt","r")
	output = int(fl.readline())
	fl.close()
	os.system("rm " + path + histone + "/5_" + histone + "_counts.txt")
	if int(output) > Min_read_number:	# Check whether read number is higher than the given value. If so, downsample the corresponding file otherwise, skip it.
		
		data = pd.read_csv(path + histone + "/4_" + histone + "_edited_sorted.bed", sep="\t", index_col=False)
		rdm = data.sample(n=subsample_n, random_state=1)
		rdm.to_csv(path + histone + '/SPO_' + histone +'_3M_Melsubsampled.bed', sep="\t", index=False)
		
		# The created file may have undesired characters and spacing. The below line of code is advised to be run individually.
		# os.system("sed 's/\"//g' " + path + histone + "/SPO_" + histone + "_3M_Melsubsampled.bed > " + path + histone + "/SPO_" + histone + "_3M_subsampled.bed")
		# or before "rdm.to_csv" step, apply "rdm.str.replace('"', '')" to discard the undesired or problemetic characters.
