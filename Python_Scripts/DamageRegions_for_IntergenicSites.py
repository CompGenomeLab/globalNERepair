#################################################################################################################
#   Using damage-seq reads, which were mapped to hg19 genome, the mappable chromosome positions are acquired    #
#   for selecting intergenic regions accordingly.                                                               #
#   All damage-seq data should grouped in a single file.                                                        # 
#################################################################################################################
from itertools import islice

path_files = "C://demo_path_to_damage-seq_files//"
count_threshold = 164.955800093

List_64PPADMG, List_64PPBDMG, List_CPDADMG, List_CPDBDMG, Unwanted_List, Common_rows_List = [],[],[],[],[],[]

with open(path_files + 'Combined_damage-seq_files.csv','r') as allDMG:
    for dmg_lane in allDMG:
        column = dmg_lane.split('\t')
        Chr_name = column[0]
        Start = column[1]
        End = column[2]
        Count = column[9].rstrip()
        Label = column[8]
        
        #   Filter and check count numbers (RPKM) of [6-4]PP replicate A
        if (column[8] == '"HDA64A1_ATCACG"') and (float(Count) > count_threshold):
            List_64PPADMG.append([Chr_name, "\t", Start, "\t", End, "\t", Count, "\t", Label])
            
        #   Filter and check count numbers (RPKM) of [6-4]PP replicate B
        elif (column[8] == '"HDA64B19_GTGAAA"') and (float(Count) > count_threshold):
            List_64PPBDMG.append([Chr_name, "\t", Start, "\t", End, "\t", Count, "\t", Label])
            
        #   Filter and check count numbers (RPKM) of CPD replicate A
        elif (column[8] == '"HDACA6_GCCAAT"') and (float(Count) > count_threshold):
            List_CPDADMG.append([Chr_name, "\t", Start, "\t", End, "\t", Count, "\t", Label])
            
        #   Filter and check count numbers (RPKM) of CPD replicate B
        elif (column[8] == '"HDACB23_GAGTGG"') and (float(Count) > count_threshold):
            List_CPDBDMG.append([Chr_name, "\t", Start, "\t", End, "\t", Count, "\t", Label])
            
        #   All the reads having less than given count_threshold
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
sum_list = len(List_64PPADMG) + len(List_64PPBDMG) + len(List_CPDADMG) + len(List_CPDBDMG)
print(sum_list)

#   Concatanate lists into one big list:
Big_list = List_64PPADMG + List_64PPBDMG + List_CPDADMG + List_CPDBDMG

#   Check the values below the threshold:
for k in islice(Unwanted_List,10,):
    print(k)

#   Write down the rows into a new file:
path_file_write = "D://new_path//"

t = 0
with open(path_file_write + "Damage_regions_Hg19Genome.bed",'w') as nfl:
    for w in Big_list:
        nfl.write('{}\n'.format(w))
        t = t + 1
print("The number of lanes found within newly created file: " , t , " == ", sum_list)

nfl.close()
