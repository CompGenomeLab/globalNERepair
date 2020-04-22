import os

colCount_num =  6    #   The column number of column count within the BED file.

path = "C:EXP//"     #   Path to the directory which includes the count numbers in BED file 
level_1_dir_list = os.listdir(path)

for i in level_1_dir_list:
    
    filelist = os.listdir(path + "{}".format(i))
    sorted_filelist = sorted(filelist)
    
    denominator_file_name = sorted_filelist[6]        #   The location of the BED file which has row numbers after mapping within the directory.
    main_file_name = sorted_filelist[2]                #    The location of the BED file which has the count numbers within the directory.
    
    file_nth = open(path + "{}/{}".format(i, denominator_file_name))
    denominator_list = file_nth.readlines()
    denominator = int(denominator_list[0])
    file_nth_2 = open(path + "{}/{}".format(i, main_file_name))
    newlined_list_with_each_line = file_nth_2.readlines()
    list_with_each_line = []

    for g in newlined_list_with_each_line:
        list_with_each_line.append(g.replace("\n", ""))

    rpkm_list = []
    for h in list_with_each_line:
        split = h.split("\t")
        int_rpkm = ((int(split[colCount_num])) * (10**9))/(5*denominator)
        rpkm_list.append(str(int_rpkm))

    k = 0
    #   Creating BED file including RPKM column.
    with open(path + "{}/".format(i) + "99_{}_RPKM_added.bed".format(i), 'w+') as file:
        for m in range(len(list_with_each_line)):
            file.write("{}\t{}\n".format(list_with_each_line[k],rpkm_list[k]))
            k += 1
