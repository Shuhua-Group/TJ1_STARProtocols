#coding:utf-8
#2021-9-1

import os 
import sys

chrom = sys.argv[1]
ref_mrg_path = sys.argv[2]
ref_gff_path = sys.argv[3]

os.system("mkdir -p ./snpeff_test/")

fout_bed_path = "./NH1.medically_gene.bed"
fout_gff_path = "./snpeff_test/genes.gff"

ref_medically_gene_dt = {}
line_nu = 0
with open(ref_mrg_path) as file:
    for line in file:
        line_nu += 1
        if line_nu == 1:
            pass
        else:
            j = line.strip().split("\t")
            chr = j[0]
            gene = j[-1]
            if chr == chrom:
                ref_medically_gene_dt[gene] = []

def fout_bed(ref_path,fout_path):
    ref_gene_dt = {}
    ref_gene_list = []
    with open(ref_path) as file:
        for line in file:
            val = line.strip()
            if val.count("#") != 0:
                pass
            else:
                j = val.split("\t")
                chr = j[0]
                start = j[3]
                end = j[4]
                gene_cbind = chr + "--" + start + "--" + end
                info_list = j[8].split(";")
                if (j[2].count("gene") != 0) and (chr == "GWHAAAS00000500"):
                    for info in info_list:
                        if info.split("=")[0] == "gene_name":
                            gene_name = info.split("=")[1]
                            if gene_name in ref_medically_gene_dt:
                                ref_gene_list.append(gene_name)
                                ref_gene_dt[gene_name] = gene_cbind

    fout_file = open(fout_path,"w")
    for gene in ref_gene_list:
        gene_cbind = ref_gene_dt[gene]
        chr = gene_cbind.split("--")[0]
        start = gene_cbind.split("--")[1]
        end = gene_cbind.split("--")[2]
        result = (chr,start,end)
        fout_file.write("\t".join(result) + "\n")
    fout_file.close()

def fout_gff(ref_path,fout_path):
    fout_line_list = []
    with open(ref_path) as file:
        for line in file:
            val = line.strip()
            if val.count("#") != 0:
                pass
            else:
                j = val.split("\t")
                chr = j[0]
                start = j[3]
                end = j[4]
                gene_cbind = chr + "--" + start + "--" + end
                info_list = j[8].split(";")
                if chr == "GWHAAAS00000500":
                    if (j[2].count("gene") != 0):
                        for info in info_list:
                            if info.split("=")[0] == "gene_name":
                                gene_name = info.split("=")[1]
                                if gene_name in ref_medically_gene_dt:
                                    fout_line_list.append(line)
                                break
                    else:
                        if gene_name in ref_medically_gene_dt:
                            fout_line_list.append(line)

    fout_file = open(fout_path,"w")
    for line in fout_line_list:
        fout_file.write(line)
    fout_file.close()

fout_bed(ref_gff_path,fout_bed_path)
fout_gff(ref_gff_path,fout_gff_path)

