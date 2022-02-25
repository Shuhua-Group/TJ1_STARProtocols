#$/bin/sh

function usage {
	cat << INTRO
	[Usage]
	paftools_wgs_call.sh ref.fa query.fa
	Default settings for minimap2 alignment: 
		-cx asm5 the divergence between two assemblies is about 5%
		-t 32 number of threads
		Assuming the VCF output
	Default settings for paftools call:
		-l 10000 min alignment length to compute coverage
		-L 50000 min alignment length to call variants
		-q 5 min mapping quality
	Any changes to the default settings should edit the code!
INTRO
}

export MINIMAP2=path/to/minimap2
export K8=path/to/k8
export PAFTOOLS=path/to/minimap2/misc/paftools.js

if [ $# -lt 2 ] || [ $# -gt 2 ];then
	usage; exit 1
fi

REF=$1
QUERY=$2
NAME="${REF%'.'fa*}.${QUERY%'.'fa*}"
THREAD=32
MINCOV=10000
MINCALL=50000
MINMAQ=5

$MINIMAP2 -cx asm5 -t $THREAD --cs $REF $QUERY > ${NAME}.paf
sort -k6,6 -k8,8n ${NAME}.paf > ${NAME}.srt.paf
$K8 $PAFTOOLS call -l $MINCOV -L $MINCALL -q $MINMAQ -f $REF -s $QUERY ${NAME}.srt.paf > ${NAME}.vcf 2>${NAME}.stat
