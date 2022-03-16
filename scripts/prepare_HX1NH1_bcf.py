#coding: utf-8


import os 
import sys
import gzip

ref_HX1NH1_path = sys.argv[1]

def prepare_ref_list():
    fout_header_list = [] 
    fout_HX1NH1_line_list = []
    with gzip.open(ref_HX1NH1_path) as file:
        for line in file:
            val = line.strip()
            if val.count("#") != 0:
                fout_header_list.append(line)
            else:
                j = line.strip().split()
                chr = j[0]
                pos = j[1]
                ref = j[3]
                alt = j[4]
                geno = j[-1]
                snp_cbind = chr + "-" + pos + "-" + ref + "-" + alt
                if (geno.count("0|1") != 0) or (geno.count("1|0") != 0) or (geno.count("1|1") != 0):
                    if len(ref) - len(alt) == 0:
                        fout_HX1NH1_line_list.append(line)
    return(fout_header_list,fout_HX1NH1_line_list)

fout_header_list,fout_HX1NH1_line_list = prepare_ref_list()

def fout_result(fout_line_list):
    fout_line_list = []
    for line in fout_HX1NH1_line_list:
        j = line.strip().split()
        chr = j[0]
        pos = j[1]
        ref = j[3]
        alt = j[4]
        snp_cbind = chr + "-" + pos + "-" + ref + "-" + alt
        fout_line_list.append(line)

    fout_path = "HX1NH1_refb38.dip.filtered.vcf"
    fout_file = open(fout_path,"w")
    for line in fout_header_list:
        fout_file.write(line)
    for line in fout_line_list:
        fout_file.write(line)
    fout_file.close()

    fout_bcf_path = "HX1NH1_refb38.dip.filtered.bcf"
    os.system("bcftools view %s -O b -o %s" %(fout_path,fout_bcf_path))
    os.system("bcftools index %s" %(fout_bcf_path)) 


fout_line_list = fout_HX1NH1_line_list
fout_result(fout_line_list)

