#coding:utf-8


import os
import sys

ref_fasta = sys.argv[1]
ref_fasta_fai = sys.argv[2]
fout_fasta = sys.argv[3]

ref_fasta = "hx1f4.3rdfixedv2.fasta"
ref_fasta_fai = "hx1f4.3rdfixedv2.fasta.fai"
fout_fasta = "hx1f4.3rdfixedv2.filter_len.fa"

ref_chr_list = []
with open(ref_fasta_fai) as file:
    for line in file:
        j = line.strip().split()
        chr = j[0]
        len = j[1]
        if int(len) > 1000:
            ref_chr_list.append(chr)


if os.path.exists(fout_fasta):
    os.system("rm %s" %(fout_fasta))
else:
    print("start")
    os.system("samtools faidx %s %s > %s" %(ref_fasta,ref_chr_list[0],fout_fasta))
    for chr in ref_chr_list[1:]:
        os.system("samtools faidx %s %s >> %s" %(ref_fasta,chr,fout_fasta))
