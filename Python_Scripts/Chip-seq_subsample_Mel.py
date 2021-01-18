import pandas as pd
import os
import subprocess

path = '/cta/users/ardacetin/globalRepair/MelanomaPrediction/chipseq/ChIP-seqProtocolFile_4hr/'

histones = ["SRR227397_SRR227398.fastq","SRR227579_SRR227580.fastq","SRR568344_SRR568345.fastq","SRR227501_SRR227502.fastq","SRR227596_SRR227597.fastq","SRR568397_SRR568398.fastq","SRR227554_SRR227555.fastq","SRR568266_SRR568267_SRR568268.fastq","SRR568399_SRR568400.fastq","SRR577321_SRR577322.fastq"]

for histone in histones:
	os.system("grep -c '^' " + path + histone + "/4_" + histone + "_edited_sorted.bed > " + path + histone + "/5_" + histone + "_counts.txt")
	
	fl = open(path + histone + "/5_" + histone + "_counts.txt","r")
	output = int(fl.readline())
	fl.close()
	os.system("rm " + path + histone + "/5_" + histone + "_counts.txt")
	if int(output) > 10349091:
		
		data = pd.read_csv(path + histone + "/4_" + histone + "_edited_sorted.bed", sep="\t", index_col=False)
		rdm = data.sample(n=2852000, random_state=1) #17573000
		rdm.to_csv(path + histone + '/SPO_' + histone +'_3M_Melsubsampled.bed', sep="\t", index=False)
		
		#os.system("sed 's/\"//g' " + path + histone + "/SPO_" + histone + "_12andhalfM_subsampled.bed > " + path + histone + "/SPO_" + histone + "_12andHalfM_subsampled.bed")
