#############################################################################################################################################
#   This script enable me to reach regions on the Hg19 genome where there is damage. The damage indicates these regions of genome is mappable.
#############################################################################################################################################
from itertools import islice

path_files = "C://Users//Arda//Documents//TEZ//TEZ-Data//HeLa-Cells//Damage-seq_Data//No_ControlandSignDiversity_Data//"

List_64PPADMG, List_64PPBDMG, List_CPDADMG, List_CPDBDMG, Unwanted_List, Common_rows_List = [],[],[],[],[],[]

with open(path_files + 'dmg_seqs_no_signs.csv','r') as allDMG:
    for dmg_lane in allDMG:
        column = dmg_lane.split('\t')
        #print(column[8])
        Chr_name = column[0]
        Start = column[1]
        End = column[2]
        Count = column[9].rstrip()
        Label = column[8]
        if column[8] == '"HDA64A1_ATCACG"' and float(Count) > 164.955800093:
            List_64PPADMG.append([Chr_name, "\t", Start, "\t", End, "\t", Count, "\t", Label])
        elif column[8] == '"HDA64B19_GTGAAA"' and float(Count) > 164.955800093:
            List_64PPBDMG.append([Chr_name, "\t", Start, "\t", End, "\t", Count, "\t", Label])
        elif column[8] == '"HDACA6_GCCAAT"' and float(Count) > 164.955800093:
            List_CPDADMG.append([Chr_name, "\t", Start, "\t", End, "\t", Count, "\t", Label])
        elif column[8] == '"HDACB23_GAGTGG"' and float(Count) > 164.955800093:
            List_CPDBDMG.append([Chr_name, "\t", Start, "\t", End, "\t", Count, "\t", Label])
        else:
            Unwanted_List.append(dmg_lane)
            continue
allDMG.close()
print(len(List_64PPADMG))
print(len(List_64PPBDMG))
print(len(List_CPDADMG))
print(len(List_CPDBDMG))
print(len(Unwanted_List))

#   Sum of Damage rows excluding values lower than threshold:
print(len(List_64PPADMG) + len(List_64PPBDMG) + len(List_CPDADMG) + len(List_CPDBDMG))

#   Concatanate lists into one big list:
Big_list = List_64PPADMG + List_64PPBDMG + List_CPDADMG + List_CPDBDMG

#   Check the values below the threshold:
for k in islice(Unwanted_List,10,):
    print(k)

#   Write down the rows into a new file:
path_file_write = "D://Human_Gene_Annotations//Damage_Coordinates_for_IntergenicSite_Selection//"
t = 0
with open(path_file_write + "Damage_regions_Hg19Genome.bed",'w') as nfl:
    for w in Big_list:
        nfl.write('{}\n'.format(w))
        t = t + 1
print("The number of lanes found within newly created file: " , t , " == 2161680")