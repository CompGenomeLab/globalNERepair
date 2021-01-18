import pandas as pd
import os

############################################
path = "/cta/users/ardacetin/globalRepair/MelanomaPrediction/repair/XR-seqProtocolFile_4hr/"       # Path where the created files will be.
subsample_n = 17573000        # The number of reads which will be randomly picked.
Min_read_number = 17572461    # The minimum tolerated read number for a file for not involving in downsampling process.
############################################

dir_list = os.listdir(path)

for SRA in dir_list:
    os.system("grep -c '^' " + path + SRA + "/6_" + SRA + "_filtered_sorted.bed > " + path + SRA + "/6_" + SRA + "_filtered_sorted_readCount.txt")

    fl = open(path + SRA + "/6_" + SRA + "_filtered_sorted_readCount.txt","r")
    output = int(fl.readline())
    fl.close()
    os.system("rm " + path + SRA + "/6_" + SRA + "_filtered_sorted_readCount.txt")
    if int(output) > Min_read_number:	# Check whether read number is higher than the given value. If so, downsample the corresponding file otherwise, skip it.

            data = pd.read_csv(path + SRA + "/6_" + SRA + "_filtered_sorted.bed", sep="\t", index_col=False)
            rdm = data.sample(n=subsample_n, random_state=1)
            rdm.to_csv(path + SRA + "/SPO_" + SRA + "_3M_Melsubsampled.bed", sep="\t", index=False)
    
            # The created file may have undesired characters and spacing. The below line of code is advised to be run individually.
            #os.system("sed 's/\"//g' " + path + histone + "/SPO_" + histone + "_3M_Melsubsampled.bed > " + path + histone + "/SPO_" + histone + "_3M_subsampled.bed")
            # or before "rdm.to_csv" step, apply "rdm.str.replace('"', '')" to discard the undesired or problemetic characters.
