import pandas as pd
import os
import subprocess

#	The below num_rows, path and path_excel should be changed according to user preference before using the script.
num_rows = 17573000			#	The number of row wanted to be downsampling randomly.
threshold_val = 17572461	#	The threshold value for deciding whether the BED file needs a random downsampling
path = '/cta/users/ardacetin/globalRepair/MelanomaPrediction/chipseq/ChIP-seqProtocolFile/'		#	Path to the directory of BED file
path_excel = "C://Users//Arda//Documents//TEZ//ENCODE_ChIP-seq_Table-NHDF_skinfibroblast.xlsx"    #   Path to the excel file which includes histone marker name and thier corresponding SRA_IDs.
#######################################################

histone_file = pd.read_excel(path_excel)
SRAid_column = histone_file['SRA_id'].tolist()

for histone in SRAid_column:
	#	Creates file including row number information using BED file CHR information alone.
	os.system("grep -c '^' " + path + histone + "/4_" + histone + "_edited_sorted.bed > " + path + histone + "/5_" + histone + "_counts.txt")
	
	#	Opens newly created file having row number.
	fl = open(path + histone + "/5_" + histone + "_counts.txt","r")
	output = int(fl.readline())
	fl.close()
	os.system("rm " + path + histone + "/5_" + histone + "_counts.txt")
	#	Checks whether the row number in a BED file is above a threshold value.
	if int(output) > threshold_val:					#	Threshold value for checking number of row. 
		
		data = pd.read_csv(path + histone + "/4_" + histone + "_edited_sorted.bed", sep="\t", index_col=False)
		rdm = data.sample(n= num_rows, random_state=1)
		rdm.to_csv(path + histone + '/SPO_' + histone +'_18M_Melsubsampled.bed', sep="\t", index=False)