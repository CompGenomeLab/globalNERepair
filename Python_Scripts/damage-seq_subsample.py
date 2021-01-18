#   For damage-seq data
#   This script subsample the damage-seq data by considering plus and minus strands.

import os
import pandas as pd

path = "/cta/users/ardacetin/globalRepair/MelanomaPrediction/damageseq/damage-seqProtocolFile_4hr/"

dir_list = os.listdir(path)

for SRA in dir_list:
    os.system("grep -c '^' " + path + SRA + "/10_" + SRA + "_cutadapt_sorted_plus_dipyrimidines.bed > " + path + SRA + "/10_" + SRA + "_plus_readCount.txt")
    os.system("grep -c '^' " + path + SRA + "/10_" + SRA + "_cutadapt_sorted_minus_dipyrimidines.bed > " + path + SRA + "/10_" + SRA + "_minus_readCount.txt")

    fl_p = open(path + SRA + "/10_" + SRA + "_plus_readCount.txt","r")
    output_p = int(fl_p.readline())
    fl_p.close()
    os.system("rm " + path + SRA + "/10_" + SRA + "_plus_readCount.txt")

    fl_m = open(path + SRA + "/10_" + SRA + "_minus_readCount.txt","r")
    output_m = int(fl_m.readline())
    fl_m.close()
    os.system("rm " + path + SRA + "/10_" + SRA + "_minus_readCount.txt")

    file_p = pd.read_csv(path + SRA + "/10_" + SRA + "_cutadapt_sorted_plus_dipyrimidines.bed", sep="\t", index_col=False)
    rdm_p = file_p.sample(n=1427000, random_state=1) #8786500
    rdm_p.to_csv(path + SRA + "/SPO_" + SRA + "_3M_plus_Melsubsampled.bed", sep="\t", index=False)
    #part_Ip = "sed 's/\"//g' " + path + SRA + "/SPO_" + SRA + "_9M_plus_Melsubsampled.bed > "
    #part_IIp = path + SRA + "/SPO_" + SRA + "_9M_plus_Melsubsampled_edited.bed"
    #partp_conc = part_Ip + part_IIp
    #os.system(partp_conc)


    file_m = pd.read_csv(path + SRA + "/10_" + SRA + "_cutadapt_sorted_minus_dipyrimidines.bed", sep="\t", index_col=False)
    rdm_m = file_m.sample(n=1425000, random_state=1) #8786500
    rdm_m.to_csv(path + SRA + "/SPO_" + SRA + "_3M_minus_Melsubsampled.bed", sep="\t", index=False)
    #part_Im = "sed 's/\"//g' " + path + SRA + "/SPO_" + SRA + "_9M_minus_Melsubsampled.bed > "
    #part_IIm = path + SRA + "/SPO_" + SRA + "_9M_minus_Melsubsampled_edited.bed"
    #partm_conc = part_Im + part_IIm
    #os.system(partm_conc)
