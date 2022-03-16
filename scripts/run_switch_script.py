#coding: utf-8


import os
import gzip


ref_prefix = "path/to/switch_error/data/"
ref_sample_list = ["HGDP00776","HGDP00784","HGDP00812","HGDP00819"]

def get_per_sample_het_snp():
    fout_header_list = []
    ref_snp_cbind_list = []
    ref_snp_cbind_geno_dt = {}
    ref_sample_index_dt = {}
    ref_path = ref_prefix + "4HAN.genomewide.hc.snp.filtered.chr22.b38.phased.vcf.gz"
    with gzip.open(ref_path) as file:
        for line in file:
            val = line.strip()
            if val.count("#") == 2:
                fout_header_list.append(line)
            elif val.count("#") == 1:
                j = line.strip().split()
                for nu in range(len(j)):
                    sample = j[nu]
                    if sample in ref_sample_list:
                        ref_sample_index_dt[sample] = nu
            elif val.count("#") == 0:
                j = line.strip().split()
                chr = j[0][3:]
                pos = j[1]
                ref = j[3]
                alt = j[4]
                snp_cbind = chr + "-" + pos + "-" + ref + "-" + alt
                ref_snp_cbind_list.append(snp_cbind)
                ref_snp_cbind_geno_dt[snp_cbind] = {}
                for sample in ref_sample_list:
                    geno = j[ref_sample_index_dt[sample]]
                    j[0] = chr
                    ref_snp_cbind_geno_dt[snp_cbind][sample] = j[:9] + [geno] 

    for sample in ref_sample_list:
        fout_path = ref_prefix + sample + ".chr22.phased.vcf"
        if os.path.exists(fout_path + ".gz"):
            os.system("rm %s.gz" %(fout_path))
        fout_file = open(fout_path,"w")
        for header in fout_header_list:
            fout_file.write(header)
        result = ["#CHROM","POS","ID","REF","ALT","QUAL","FILTER","INFO","FORMAT",sample]
        fout_file.write("\t".join(result) + "\n")
        for snp_cbind in ref_snp_cbind_list:
            result = ref_snp_cbind_geno_dt[snp_cbind][sample]
            geno = result[-1]
            if (geno == "0|1") or (geno == "1|0"):
                fout_file.write("\t".join(result) + "\n")
        fout_file.close()
        os.system("bgzip %s" %(fout_path))

def generate_multihetsep():
    for sample in ref_sample_list:
        ref_path = ref_prefix + sample + ".chr22.phased.vcf.gz"
        fout_path = ref_prefix + sample + ".distance.chr22.txt"
        os.system("generate_multihetsep.py %s 1>%s 2>/dev/null" %(ref_path,fout_path))

def run_switch_2():
    for sample in ref_sample_list:
        ref_bam = ref_prefix + sample + ".dedup.chr22.sorted.bam"
        ref_path = ref_prefix + sample + ".distance.chr22.txt"
        fout_path = ref_prefix + sample + ".rs.chr22.txt"
        os.system("switch-2 %s %s 1>%s 2>/dev/null" %(ref_path,ref_bam,fout_path))

def get_switch_error():
    fout_path = ref_prefix + "4HAN.switch_error.txt"
    fout_file = open(fout_path,"w")
    result = ("sample","switch_error")
    fout_file.write("\t".join(result) + "\n")
    for sample in ref_sample_list:
        ref_path = ref_prefix + sample + ".rs.chr22.txt"
        error_count = 0
        total_count = 0
        with open(ref_path) as file:
            for line in file:
                j = line.strip().split()
                flag_1 = j[1]
                flag_2 = j[4]
                if (flag_1 == "1") and (flag_2 == "1"):
                    total_reads = int(j[6]) + int(j[7]) + int(j[8]) + int(j[9]) + int(j[10])
                    if 15 <= total_reads <= 50:
                        total_count += 1
                        if float(int(j[8]) + int(j[9]) + int(j[10]))/(int(j[6]) + int(j[7]) + int(j[8]) + int(j[9]) + int(j[10])) > 0.2:
                            error_count += 1
        switch_error = float(error_count)/total_count
        result = (sample,str(switch_error))
        fout_file.write("\t".join(result) + "\n")
    fout_file.close()

get_per_sample_het_snp()
generate_multihetsep()
run_switch_2()
get_switch_error()

