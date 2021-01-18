import pandas as pd
import os
import subprocess

path = '/cta/users/ardacetin/globalRepair/MelanomaPrediction/DNAseI/DNAse-seqProtocolFiles_4hr/'

histones = ["SRR231190.fastq"]

for histone in histones:
	os.system("grep -c '^' " + path + histone + "/4_" + histone + "_edited_sorted.bed > " + path + histone + "/5_" + histone + "_counts.txt")
	
	fl = open(path + histone + "/5_" + histone + "_counts.txt","r")
	output = int(fl.readline())
	fl.close()
	os.system("rm " + path + histone + "/5_" + histone + "_counts.txt")
	if int(output) > 2852010:
		
		data = pd.read_csv(path + histone + "/4_" + histone + "_edited_sorted.bed", sep="\t", index_col=False)
		rdm = data.sample(n=2852000, random_state=1)
		rdm.to_csv(path + histone + '/SPO_' + histone +'_3M_Melsubsampled.bed', sep="\t", index=False)
		
		#os.system("sed 's/\"//g' " + path + histone + "/SPO_" + histone + "_12andhalfM_subsampled.bed > " + path + histone + "/SPO_" + histone + "_12andHalfM_subsampled.bed")
