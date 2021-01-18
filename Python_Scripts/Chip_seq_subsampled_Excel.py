import pandas as pd
import os

# This python code extract data from excel file.
# The only difference between this ".py" and "Chip-seq_subsample_dir.py" is the type of file source.
##############################################
num_rows = 17573000		# The number of row wanted to be downsampling randomly.
Min_read_number = 17572461	# The threshold value for deciding whether the BED file needs a random downsampling
path = '/cta/users/ardacetin/globalRepair/MelanomaPrediction/chipseq/ChIP-seqProtocolFile/'	  # Path to the directory of BED file
path_excel = "C://Users//Arda//Documents//TEZ//ENCODE_ChIP-seq_Table-NHDF_skinfibroblast.xlsx"    # Path to the excel file which includes histone marker name and thier corresponding SRA_IDs.
##############################################



histone_file = pd.read_excel(path_excel)
SRAid_column = histone_file['SRA_id'].tolist()

for histone in SRAid_column:
	os.system("grep -c '^' " + path + histone + "/4_" + histone + "_edited_sorted.bed > " + path + histone + "/5_" + histone + "_counts.txt")
	
	fl = open(path + histone + "/5_" + histone + "_counts.txt","r")
	output = int(fl.readline())
	fl.close()
	os.system("rm " + path + histone + "/5_" + histone + "_counts.txt")
	if int(output) > Min_read_number:      # Check whether read number is higher than the given value. If so, downsample the corresponding file otherwise, skip it.
		
		data = pd.read_csv(path + histone + "/4_" + histone + "_edited_sorted.bed", sep="\t", index_col=False)
		rdm = data.sample(n=num_rows, random_state=1)
		rdm.to_csv(path + histone + '/SPO_' + histone +'_3M_Melsubsampled.bed', sep="\t", index=False)
		
		# The created file may have undesired characters and spacing. The below line of code is advised to be run individually.
		# os.system("sed 's/\"//g' " + path + histone + "/SPO_" + histone + "_3M_Melsubsampled.bed > " + path + histone + "/SPO_" + histone + "_3M_subsampled.bed")
		# or before "rdm.to_csv" step, apply "rdm.str.replace('"', '')" to discard the undesired or problemetic characters.
