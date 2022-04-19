#!/usr/bin/perl
#Used to convert symbolic VCFs to explicit VCFs
#USAGE: explicitVCF.converter reference.genome.fasta symbolic.vcffile.vcf
#samtools is needed for this script

use strict;
my $refgenome="$ARGV[0]";

open(INFILE,"$ARGV[1]");
my @infile=<INFILE>;
chomp @infile;
close INFILE;

open(OUT,">>$ARGV[1]_explicit.vcf");
print OUT "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tAAGC031920D\n";
for(my $i=0;$i<@infile;$i++){
	if (@infile[$i] =~ /#/) {
		#print OUT @infile[$i]."\n";
		next;
	}

	my @single=split("\t",@infile[$i]);

	my $filter=@single[6];
	if ($filter ne "PASS") {
		next;
	}
	
	my $chrom=@single[0];
	my $pos=@single[1];
	my $id=@single[2];
	my $ref;
	my $alt;
	my $qual=@single[5];
	my $info=@single[7];
	my $format="GT";
	my $length;
	my $end=$info;
	$end=~ s/(END=)([0-9]{1,10})(;.*)/$2/;
	$info=~ s/(END=)([0-9]{1,10};)(.*)/$3/;
	my $cal=0;
	my @GTout=split(":",@single[9]);
	my $GT=@GTout[0];
	my $CN;
	$ref=`samtools faidx $refgenome $chrom:$pos-$end | sed "1d" | xargs | sed "s/ //g"`;
	chop $ref;
	$alt=substr($ref,0,1);
	print OUT $chrom."\t".$pos."\t".$id."\t".$ref."\t".$alt."\t".$qual."\t".$filter."\t".$info."\t".$format."\t".$GT."\n";
}
close (OUT);
