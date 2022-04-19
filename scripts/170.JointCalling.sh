#!/bin/bash

cwd='path/to/HX1/'

mkdir -p $cwd

###ref files and bins
fasta='path/to/NH1.chr22.fa'

###############################################################
proid="HX1"

mkdir -p $cwd/170.GenotypeGVCFs.joint.calling; cd $cwd/170.GenotypeGVCFs.joint.calling
ref_fai_path="/path/to/NH1.chr22.fa.fai"
ref_chr_list=`cat $ref_fai_path | awk '{print $1}'`
for chr in $ref_chr_list
do
	bash=170.$chr.sh
	echo "#$ -N genovcf.$chr" > $bash
	echo "mkdir -p tmp/${chr}" >> $bash 
	echo "time gatk --java-options \"-Xmx20g -XX:ParallelGCThreads=8 -Djava.io.tmpdir=tmp/${chr}\" GenotypeGVCFs -R $fasta \\" >> $bash
	for line in `cat $cwd/list/$chr.list`
	do
		echo "--variant $line \\" >> $bash
	done
	echo "-L $chr -O $proid.$chr.hc.vcf.gz" >> $bash
done
#combine as one file
vlist=" "
ref_fai_path="path/to/NH1.chr22.fa.fai"
ref_chr_list=`cat $ref_fai_path | awk '{print $1}'`
for chr in $ref_chr_list
do
	vlist=" $vlist -I "$proid.$chr.hc.vcf.gz
done
bash=170.combine.sh
echo "#$ -N com170" >$bash
echo "mkdir -p tmp/combine" >> $bash 
echo "time gatk --java-options \"-Xmx256g -Djava.io.tmpdir=tmp/combine\" GatherVcfs -R $fasta $vlist -O $proid.genomewide.hc.vcf.gz" >>$bash  