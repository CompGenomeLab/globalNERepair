#   For xr-seq data
#   This script subsample the xr-seq data by considering plus and minus strands.

import os
import pandas as pd

path = "/cta/users/ardacetin/globalRepair/MelanomaPrediction/repair/XR-seqProtocolFile_4hr/"

dir_list = os.listdir(path)

for SRA in dir_list:
    os.system("grep -c '^' " + path + SRA + "/6_" + SRA + "_filtered_sorted.bed > " + path + SRA + "/6_" + SRA + "_filtered_sorted_readCount.txt")

    fl_p = open(path + SRA + "/6_" + SRA + "_filtered_sorted_readCount.txt","r")
    output_p = int(fl_p.readline())
    fl_p.close()
    os.system("rm " + path + SRA + "/6_" + SRA + "_filtered_sorted_readCount.txt")

    file_p = pd.read_csv(path + SRA + "/6_" + SRA + "_filtered_sorted.bed", sep="\t", index_col=False)
    rdm_p = file_p.sample(n=2852000, random_state=1) #10349089
    rdm_p.to_csv(path + SRA + "/SPO_" + SRA + "_3M_Melsubsampled.bed", sep="\t", index=False)
    #part_Ip = "sed 's/,/\t/g' " + path + SRA + "/SPO_" + SRA + "_18M_Melsubsampled.bed > "
    #part_IIp = path + SRA + "/SPO_" + SRA + "_18M_plus_Melsubsampled_edited.bed"
    #partp_conc = part_Ip + part_IIp
    #os.system(partp_conc)
