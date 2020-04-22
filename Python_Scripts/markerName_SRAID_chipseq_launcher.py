#   The script enable user to initiate ChIP-seq pipeline (not only chip-seq but it could be used for any other purposes as well) with two inputs.
import os
import pandas as pd
import itertools

#   User should adjust these three parameters before using the script:
name_fl = "partial_chip_Mel.sh"   # The name of the ChIP-seq pipeline
path_fl = "/cta/users/ardacetin/globalRepair/MelanomaPrediction/chipseq/"   #   The path of the ChIP-seq pipeline

path_excel = "C://Users//Arda//Documents//TEZ//ENCODE_ChIP-seq_Table-NHDF_skinfibroblast.xlsx"    #   Path to the excel file which includes histone marker name and thier corresponding SRA_IDs.
#########################################################################

histone_file = pd.read_excel(path_excel)

SRAid_column = histone_file['SRA_id'].tolist()
HistoneName_column = histone_file['marker'].tolist()

for Nam, SRA in zip(HistoneName_column, SRAid_column):
    partI = "sbatch " + path_fl + name_fl + " "
    partII = SRA + " " + Nam
    concatanate_parts = partI + partII
    os.system(concatanate_parts)