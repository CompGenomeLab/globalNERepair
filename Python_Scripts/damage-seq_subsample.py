import pandas as pd
import os


###############################################
path = "/cta/users/ardacetin/globalRepair/MelanomaPrediction/damageseq/damage-seqProtocolFile_4hr/"     # Path where the created files will be.
Min_read_number = 17572461    # The minimum tolerated read number for a file for not involving in downsampling process.
dir_list = os.listdir(path)   # All ChIP-seq files should be at the same directory.
###############################################


for SRA in dir_list:
    os.system("grep -c '^' " + path + SRA + "/10_" + SRA + "_cutadapt_sorted_plus_dipyrimidines.bed > " + path + SRA + "/10_" + SRA + "_plus_readCount.txt")
    os.system("grep -c '^' " + path + SRA + "/10_" + SRA + "_cutadapt_sorted_minus_dipyrimidines.bed > " + path + SRA + "/10_" + SRA + "_minus_readCount.txt")
    
    # For the equal selection of reads at plus and minus strands, the number of random sampling value should be written manually.
    # The number of sampling value may not be even always so it is sensible to type the value by hand.
    
    #   Reading read numbers for plus strand
    fl_p = open(path + SRA + "/10_" + SRA + "_plus_readCount.txt","r")
    output_p = int(fl_p.readline())
    fl_p.close()
    os.system("rm " + path + SRA + "/10_" + SRA + "_plus_readCount.txt")
    if int(output_p) > Min_read_number:     # Check whether read number is higher than the given value. If so, downsample the corresponding file otherwise, skip it.
        
            # Sampling reads randomply for plus strand 
            file_p = pd.read_csv(path + SRA + "/10_" + SRA + "_cutadapt_sorted_plus_dipyrimidines.bed", sep="\t", index_col=False)
            rdm_p = file_p.sample(n=1427000, random_state=1)
            rdm_p.to_csv(path + SRA + "/SPO_" + SRA + "_3M_plus_Melsubsampled.bed", sep="\t", index=False)

    #   Reading read numbers for minus strand
    fl_m = open(path + SRA + "/10_" + SRA + "_minus_readCount.txt","r")
    output_m = int(fl_m.readline())
    fl_m.close()
    os.system("rm " + path + SRA + "/10_" + SRA + "_minus_readCount.txt")
    if int(output_m) > Min_read_number:      # Check whether read number is higher than the given value. If so, downsample the corresponding file otherwise, skip it.
        
            # Sampling reads randomply for minus strand 
            file_m = pd.read_csv(path + SRA + "/10_" + SRA + "_cutadapt_sorted_minus_dipyrimidines.bed", sep="\t", index_col=False)
            rdm_m = file_m.sample(n=1425000, random_state=1)
            rdm_m.to_csv(path + SRA + "/SPO_" + SRA + "_3M_minus_Melsubsampled.bed", sep="\t", index=False)
            
    
            ### If application of below codes necessary, do not forget to it for both file outputs(plus and minus):
        
            # The created files may have undesired characters and spacing. The below line of code is advised to be run individually.
            # os.system("sed 's/\"//g' " + path + histone + "/SPO_" + histone + "_3M_Melsubsampled.bed > " + path + histone + "/SPO_" + histone + "_3M_subsampled.bed")
            # or before "rdm.to_csv" step, apply "rdm.str.replace('"', '')" to discard the undesired or problemetic characters.

