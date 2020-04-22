##  Script eleminates rows that are having zero RPKM value then, divides replicate A of each damage type to corresponding XR-seq damage repair.
#   If DMG_PPD_column and DMG_CPD_column column number changed to the replicate B of (6-4)PP and CPD damage, the Replicate B normalization could be performed.

### REMOVE ROWS WITH RESPECT TO DAMAGE-seq REPLICATE A  ###
stock_file_path = 'D://allseq-Data//MelanomaPrediction//Stock_Only_RPKM//Subsampled//Intergenes//'
stock_file = open(stock_file_path + 'STOCK_allseq_subsampled_Intergene_RPKM_woHeader.bed','r')

##  Row removal and Normalization for 6-4PP Damage ##
without_zero_rows_list = []
for indiv_lines in stock_file:
    splitted_lines = indiv_lines.split('\t')
    DMG_PPD_column = float(splitted_lines[7])       #   The Damage-seq column of Replicate A of whatever Damage type it is. In this case it is 6-4PP RepA.
    PPD_three_columns = splitted_lines[0:3]         #   CHR name, start and end coordinates
    PPD_histone_markers = splitted_lines[11:20]     #   The RPKM values column of ChIP-seq histone markers.
    XR_seq_PPD_RepA = float(splitted_lines[3])      #   The RPKM values column of XR-seq Replicate A
    XR_seq_PPD_RepB = float(splitted_lines[4])      #   The RPKM values column of XR-seq Replicate B
    PPD_DNAseI_column = float(splitted_lines[20])   #   The RPKM values column of XR-seq Replicate B
    if DMG_PPD_column != 0:
        #without_zero_rows_list.append(str(CPDA_three_columns).replace("'",""))
        R1_one = float(XR_seq_PPD_RepA / DMG_PPD_column)
        #without_zero_rows_list.append(R_one)
        R1_two = float(XR_seq_PPD_RepB / DMG_PPD_column)
        #without_zero_rows_list.append(R_two)
        #without_zero_rows_list.append(str(CPDA_histone_markers).replace("'",""))
        without_zero_rows_list.append([str(PPD_three_columns),str(R1_one),str(R1_two),str(PPD_histone_markers),str(PPD_DNAseI_column)])
    else:
        continue

c = 0
for Numelmnts in without_zero_rows_list:
    #print(Numelmnts)
    c += 1
print(c)
stock_file.close()
"""
##############################################################################################################################################
##############################################################################################################################################
#   This part is exactly similar with above part except the column numbers due to the difference in damage type.
stock_file_path2 = 'D://allseq-Data//MelanomaPrediction//Stock_Only_RPKM//Subsampled//Intergenes//'
stock_file2 = open(stock_file_path2 + 'STOCK_allseq_subsampled_Intergene_RPKM_woHeader.bed','r')

##  Row removal and Normalization for CPD Damage ##
without_zero_rows_list2 = []
for indiv_lines2 in stock_file2:
    splitted_lines2 = indiv_lines2.split('\t')
    DMG_CPD_column = float(splitted_lines2[9])      #   Replicate A of CPD damage
    CPD_three_columns = splitted_lines2[0:3]        #   CHR name, start and end coordinates
    CPD_histone_markers = splitted_lines2[11:20]    #   The RPKM values column of ChIP-seq histone markers.
    XR_seq_CPD_RepA = float(splitted_lines2[5])     #   The RPKM values column of XR-seq Replicate A
    XR_seq_CPD_RepB = float(splitted_lines2[6])     #   
    CPD_DNaseI_column = float(splitted_lines2[20])
    if DMG_CPD_column != 0:
        #without_zero_rows_list.append(str(CPDA_three_columns).replace("'",""))
        R2_one = float(XR_seq_CPD_RepA / DMG_CPD_column)
        #without_zero_rows_list.append(R_one)
        R2_two = float(XR_seq_CPD_RepB / DMG_CPD_column)
        #without_zero_rows_list.append(R_two)
        #without_zero_rows_list.append(str(CPDA_histone_markers).replace("'",""))
        without_zero_rows_list2.append([str(CPD_three_columns),str(R2_one),str(R2_two),str(CPD_histone_markers),str(CPD_DNaseI_column)])
    else:
        continue

k = 0
for Numelmnts2 in without_zero_rows_list2:
    #print(Numelmnts2)
    k += 1
print(k)
stock_file2.close()
"""
### CREATE FILE ###

######  Write down the remaining of zero removed rows into a file.  #####
#   Change the list (without_zero_rows_list or without_zero_rows_list2) accoding to which damage type is normalized.
#   HDA64A1_ATCACG      HDA64B19_GTGAAA         HDACA6_GCCAAT        HDACB23_GAGTGG
#              without_zero_rows_list                   without_zero_rows_list2
total = 0
directory = 'D://allseq-Data//MelanomaPrediction//RepA_Filtered_Normalized_allseq_Data//Subsampled//Intergenes//'
with open(directory + 'Zero_removed_divided_Intergene_HDA64A1_ATCACG_normalized_allseqs_w_ChrStartEnd.csv','w') as df:
    for wr in without_zero_rows_list:
        df.write('{}\n'.format(wr))       #       Do not put \n front of '{}'.
        total += 1
print("The newly generated file is having " , total , ' number of rows!')

#   The newly created Datium Structure is   #
#   Chr names   Chr Start   Chr END     6-4PP(XR-seq RepA / DMG RepA)   6-4PP(XR-seq RepB /  DMG RepA)   ChIP-seq (15 columns)
#                                                        OR
#   Chr names   Chr Start   Chr END     CPD(XR-seq RepA / DMG RepA)   CPD(XR-seq RepB /  DMG RepA)   ChIP-seq (15 columns)