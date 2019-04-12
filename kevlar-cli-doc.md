The kevlar command-line interface is designed around a single command kevlar. From this one command, a variety of tasks and procedures can be invoked using several subcommands.

Once kevlar is installed, available subcommands can be listed by executing kevlar -h. To see instructions for running a specific subcommand, execute kevlar <subcommand> -h (of course replacing subcommand with the actual name of the subcommand).

kevlar count

Compute k-mer abundances for the provided sample. Supports k-mer banding: see http://kevlar.readthedocs.io/en/latest/banding.html for more details.

usage: kevlar count [-h] [-k K] [-c C] [-M MEM] [--max-fpr FPR] [--mask MSK]
                    [--count-masked] [--num-bands N] [--band I] [-t T]
                    counttable seqfile [seqfile ...]

  Positional Arguments

  counttable	name of the file to which the output (a k-mer count table) will be written; the suffix “.counttable” will be applied if the provided file name does not end in “.ct” or “.counttable”
  seqfile	input files in Fastq/Fasta format

  Named Arguments

  -k, --ksize	k-mer size; default is 31

  -c, --counter-size
    
Possible choices: 1, 4, 8

number of bits to allocate for counting each k-mer; options are 1 (max count: 1), 4 (max count: 15), and 8 (max count: 255); default is 8

-M, --memory	memory to allocate for the count table

--max-fpr	terminate if the estimated false positive rate for any sample is higher than “FPR”; default is 0.2

--mask	counttable or nodetable of k-mers to ignore when counting k-mers

--count-masked	by default, when a mask is provided k-mers in the mask are ignored; this setting inverts the behavior so that only k-mers in the mask are counted

--num-bands	number of bands into which to divide the hashed k-mer space

--band	a number between 1 and N (inclusive) indicating the band to be processed

-t, --threads	number of threads to use for file processing; default is 1

Example:

kevlar count --memory 500M case1.ct case1-reads.fastq

Example:

kevlar count --ksize 25 --memory 12G --max-fpr 0.01 --threads 8 \
    proband.counttable \
    proband-R1.fq.gz proband-R2.fq.gz proband-unpaired.fq.gz

kevlar novel

Identify “interesting” (potentially novel) k-mers and output the corresponding reads. Here we define “interesting” k-mers as those which are high abundance in each case sample and effectively absent (below some specified abundance threshold) in each control sample.

usage: kevlar novel --case F [F ...] [--case-counts F [F ...]]
                    [--control F [F ...]] [--control-counts F [F ...]] [-x X]
                    [-y Y] [-M MEM] [--max-fpr FPR] [--num-bands N] [--band I]
                    [-o FILE] [--save-case-counts CT [CT ...]]
                    [--save-ctrl-counts CT [CT ...]] [-h] [-k K]
                    [--abund-screen INT] [-t T] [--skip-until ID]

Case/control config

Specify input files, as well as thresholds for selecting “interesting” k-mers. A single pass is made over input files for control samples (to compute k-mer abundances), while two passes are made over input files for case samples (to compute k-mer abundances, and then to identify “interesting” k-mers). The k-mer abundance computing steps can be skipped if pre-computed k-mer abunandances are provided using the “–case-counts” and/or “–control-counts” settings. If “–control-counts” is declared, then all “–control” flags are ignored. If “–case-counts” is declared, FASTA/FASTQ files must still be provided with “–case” for selecting “interesting” k-mers and reads.

--case	one or more FASTA/FASTQ files containing reads from a case sample; can be declared multiple times corresponding to multiple case samples, see examples below

--case-counts	counttable file(s) corresponding to each case sample; if not provided, k-mer abundances will be computed from FASTA/FASTQ input; only one counttable per sample, see examples below

--control	one or more FASTA/FASTQ files containing reads from a control sample; can be declared multiple times corresponding to multiple control samples, see examples below

--control-counts

 	counttable file(s) corresponding to each control sample; if not provided, k-mer abundances will be computed from FASTA/FASTQ input; only one counttable per sample, see examples below

-x, --ctrl-max	k-mers with abund > X in any control sample are uninteresting; default is X=1

-y, --case-min	k-mers with abund < Y in any case sample are uninteresting; default is Y=6

-M, --memory	total memory allocated to k-mer abundance for each sample; default is 1M; ignored when pre-computed k-mer abundances are supplied via counttable

--max-fpr	terminate if the expected false positive rate for any sample is higher than the specified FPR; default is 0.2

K-mer banding

If memory is a limiting factor, it is possible to get a linear decrease in memory consumption by running kevlar novel in “banded” mode. Splitting the hashed k-mer space into N bands and only considering k-mers from one band at a time reduces the memory consumption to approximately 1/N of the total memory required. This implements a scatter/gather approach in which kevlar novel is run N times, after the results are combined using kevlar filter.

--num-bands	number of bands into which to divide the hashed k-mer space

--band	a number between 1 and N (inclusive) indicating the band to be processed

Output settings

-o, --out	file to which interesting reads will be written; default is terminal (stdout)

--save-case-counts

 	save the computed k-mer counts for each case sample to the specified count table file(s)

--save-ctrl-counts

 	save the computed k-mer counts for each control sample to the specified count table file(s)

Miscellaneous settings

-k, --ksize	k-mer size; default is 31

--abund-screen	discard reads with any k-mers whose abundance is < INT

-t, --threads	number of threads to use for file processing; default is 1

--skip-until	when re-running kevlar novel, skip all reads in the case input until read with name ID is observed

Example:



kevlar novel --out novel-reads.augfastq --case proband-reads.fq.gz \

    --control father-reads-r1.fq.gz father-reads-r2.fq.gz \

    --control mother-reads.fq.gz

Example:

kevlar novel --out novel-reads.augfastq.gz \

    --control-counts father.counttable mother.counttable \

    --case-counts proband.counttable --case proband-reads.fastq \

    --ctrl-max 0 --case-min 10 --ksize 27

Example:

kevlar novel --out output.augfastq \

    --case proband1.fq --case proband2.fq \

    --control control1a.fq control1b.fq \

    --control control2a.fq control2b.fq \

    --save-case-counts p1.ct p2.ct --save-ctrl-counts c1.ct c2.ct

kevlar filter

Discard k-mers and reads that are contaminant in origin or whose abundances were inflated during the preliminary k-mer counting stage.

usage: kevlar filter [-h] [-M MEM] [--max-fpr FPR] [--mask MSK] [-x X] [-y Y]
                     [-o FILE]
                     augfastq

Positional Arguments

augfastq	putatively novel reads in augmented Fastq format

Named Arguments

-M, --memory	memory to allocate for the k-mer re-counting

--max-fpr	terminate early if the estimated false positive rate for re-computed k-mer abundances is higher than “FPR”; default is 0.01

--mask	counttable or nodetable of k-mers to ignore when re-counting k-mers

-x, --ctrl-max	k-mers with abund > X in any control sample are uninteresting; default is X=1

-y, --case-min	k-mers with abund < Y in any case sample are uninteresting; default is Y=6

-o, --out	output file; default is terminal (stdout)

kevlar partition

Construct a graph to group reads by shared interesting k-mers. Nodes in the graph represent reads, and edges between a pair of nodes indicate that the two corresponding reads have one or more interesting k-mers in common. Connected components in the undirected graph correspond to distinct variants (or variant-related breakpoints).

usage: kevlar partition [-h] [-s] [--min-abund X] [--max-abund Y] [--no-dedup]
                        [--gml FILE] [--split OUTPREFIX] [-o FILE]
                        infile

Positional Arguments

infile	input reads in augmented Fast[q|a] format

Named Arguments

-s, --strict	require perfect identity between overlapping reads for inclusion in the same partition; by default, only a shared interesting k-mer is required

--min-abund	ignore k-mers with abundance lower than X; default is 2

--max-abund	ignore k-mers with abundance higher than Y; default is 200

--no-dedup	skip step to remove duplicates

--gml	write read graph to .gml file

--split	write each partition to a separate output file, each with a filename like “OUTPREFIX.cc#.augfastq.gz”

-o, --out	output file; default is terminal (stdout)

kevlar assemble

Assemble reads into contigs representing putative variants

usage: kevlar assemble [-h] [-p ID] [--max-reads N] [-o FILE] augfastq

Positional Arguments

augfastq	annotated reads in augmented Fastq/Fasta format

Named Arguments

-p, --part-id	only assemble partition “ID” in the input

--max-reads	do not attempt to assemble any partitions with more than N reads (default: 10000)

-o, --out	output file; default is terminal (stdout)

kevlar localize

For each partition, compute the reference target sequence to use for variant calling. NOTE: this command relies on the bwa program being in the PATH environmental variable.

usage: kevlar localize [-h] [-d Δ] [-p ID] [-o FILE] [-z Z] [-x X]
                       [--include REGEX] [--exclude REGEX]
                       refr contigs [contigs ...]

Positional Arguments

refr	BWA indexed reference genome

contigs	assembled reads in augmented Fasta format

Named Arguments

-d, --delta	retrieve the genomic interval from the reference by extending beyond the span of all k-mer starting positions by Δ bp

-p, --part-id	only localize partition “ID” in the input

-o, --out	output file; default is terminal (stdout)

-z, --seed-size

 	seed size; default is 51

-x, --max-diff	split and report multiple reference targets if the distance between two seed matches is > X; by default, X is set dynamically for each partition and is equal to 3 times the length of the longest contig in the partition; each resulting bin specifies a reference target sequence to which assembled contigs will subsequently be aligned

--include	discard alignments to any chromosomes whose sequence IDs do not match the given pattern

--exclude	discard alignments to any chromosomes whose sequence IDs match the given pattern

kevlar call
Align variant-related reads to the reference genome and call the variant from the alignment.
usage: kevlar call [-A A] [-B B] [-O O] [-E E] [--gen-mask FILE]
                   [--mask-mem MEM] [--mask-max-fpr FPR] [-h] [-d]
                   [--no-homopoly-filter] [--max-target-length L]
                   [--refr FILE] [-o FILE] [-k K]
                   queryseq targetseq
Required inputs
queryseq	contigs assembled by “kevlar assemble”
targetseq	region of reference genome identified by “kevlar localize”
Alignment scoring
-A, --match	match score; default is 1
-B, --mismatch	mismatch penalty; default is 2
-O, --open	gap open penalty; default is 5
-E, --extend	gap extension penalty; default is 0
Mask generation settings
--gen-mask	generate a nodetable containing all k-mers that span any variant call
--mask-mem	memory to allocate for the node table
--mask-max-fpr	terminate if the estimated false positive rate is higher than “FPR”; default is 0.01
Miscellaneous settings
-d, --debug	show debugging output
--no-homopoly-filter
 	by default, short indels adjacent to homopolymers are filtered out; use this flag to disable that filter
--max-target-length
 	do not attempt to call variants if the target genomic sequence is > L bp; by default, L=10000
--refr	reference genome indexed for BWA search; if provided, mates of interesting reads will be used to diambiguate multi-mapping contigs
-o, --out	output file; default is terminal (stdout)
-k, --ksize	k-mer size; default is 31
kevlar simlike
Sort variants by likelihood score

usage: kevlar simlike --case CT --controls CT [CT ...] --refr REFR
                      [--ctrl-max X] [--case-min Y] [--mu μ] [--sigma σ]
                      [--epsilon ε] [--ctrl-abund-high H] [--case-abund-low L]
                      [--min-like-score S] [--drop-outliers]
                      [--ambig-thresh A] [-h] [--sample-labels LBL [LBL ...]]
                      [-f] [-o OUT]
                      vcf [vcf ...]
Positional Arguments
vcf	
K-mer count files
Likelihood scores are based on the abundance of alternate allele k-mers in each sample and on the abundance of reference allele k-mers in the reference genome.

--case	k-mer counttable for case/proband
--controls	k-mer counttables for controls/parents/siblings, 1 counttable per sample
--refr	k-mer smallcounttable for reference genome
K-mer count thresholds
The thresholds originally used to detect novel k-mers are used at this stage to distinguish true variants from spurious predictions.

--ctrl-max	maximum abundance threshold for controls; default is 1
--case-min	minimum abundance threshold for proband; default is 6
K-mer coverage
Likelihood scores also depend on the estimated or observed distribution of k-mer abundances in each sample.

--mu	mean k-mer abundance; default is 30.0
--sigma	standard deviation of k-mer abundance; default is 8.0
--epsilon	error rate; default is 0.001
Heuristic filters
The following heuristic filters can improve accuracy when calling de novo variants but may require tuning for your particular data set.

--ctrl-abund-high
 	a variant call will be filtered out if either of the control samples has >H high abundance k-mers spanning the variant (where high abundance means > –ctrl-max); by default, H=4; set H<=0 to disable the filter
--case-abund-low
 	a variant call will be filtered out if the case sample has L or more consecutive low abundance k-mers spanning the variant (where low abundance means < –case-min); by default, L=5; set L<=0 to disable the filter
--min-like-score
 	filter out variant predictions with likelihood scores < S; by default, S = 0.0, but it’s often possible to improve specificity without sacrificing sensitivity by raising S to, for example, 50.0
--drop-outliers
 	discard terminal variant-spanning k-mers with abunance much higher than average (representing k-mers that should be in the reference genome but are not); this will increase sensitivity, but will potentially introduce many false calls as well
--ambig-thresh	discard contigs that result in > A distinct, equally optimal variant calls; by default, A = 10; set A=0 to disable this filter
Miscellaneous settings
--sample-labels
 	list of sample labels (with case/proband first)
-f, --fast-mode
 	whenever possible, stop computations prematurely for any putative variants that have already been filtered out
-o, --out	output file; default is terminal (standard output)
kevlar alac
Assemble partitioned reads, localize to the reference genome, align the assembled contig to the reference, and call variants.
usage: kevlar alac [-p ID] [--max-reads N] [-z Z] [-d D] [-x X]
                   [--include REGEX] [--exclude REGEX] [--max-target-length L]
                   [-A A] [-B B] [-O O] [-E E] [--gen-mask FILE]
                   [--mask-mem MEM] [--mask-max-fpr FPR] [-h] [-o FILE] [-i I]
                   [-k K] [-t T]
                   infile refr
Required inputs
infile	partitioned reads in augmented Fastq format
refr	reference genome in Fasta format (indexed for bwa search)
Read assembly
-p, --part-id	only process partition “ID” in the input
--max-reads	do not attempt to assemble any partitions with more than N reads (default: 10000)
Target extraction
-z, --seed-size
 	seed size; default is 51
-d, --delta	retrieve the genomic interval from the reference by extending beyond the span of all k-mer starting positions by D bp
-x, --max-diff	split and report multiple reference targets if the distance between two seed matches is > X; by default, X is set dynamically for each partition and is equal to 3 times the length of the longest contig in the partition; each resulting bin specifies a reference target sequence to which assembled contigs will subsequently be aligned
--include	discard alignments to any chromosomes whose sequence IDs do not match the given pattern
--exclude	discard alignments to any chromosomes whose sequence IDs match the given pattern
--max-target-length
 	do not attempt to call variants if the target genomic sequence is > L bp; by default, L=10000
Alignment scoring
-A, --match	match score; default is 1
-B, --mismatch	mismatch penalty; default is 2
-O, --open	gap open penalty; default is 5
-E, --extend	gap extension penalty; default is 0
Mask generation settings
--gen-mask	generate a nodetable containing all k-mers that span any variant call
--mask-mem	memory to allocate for the node table
--mask-max-fpr	terminate if the estimated false positive rate is higher than “FPR”; default is 0.01
Miscellaneous settings
-o, --out	output file; default is terminal (stdout)
-i, --min-ikmers
 	do not report calls that a supported by fewer than I interesting k-mers
-k, --ksize	k-mer size; default is 31
-t, --threads	process T partitions at a time using T threads
kevlar unband
When kevlar is run in k-mer banding mode, the same read will typically appear in multiple output files, annotated with a different set of potentially novel k-mers in each case. This command will consolidate these duplicated records across files into a single non-redundant set of reads with the complete set of novel k-mer annotations.

usage: kevlar unband [-h] [-n N] [-o FILE] infile [infile ...]
Positional Arguments
infile	input files in augmented Fasta/Fastq format
Named Arguments
-n, --n-batches
 	number of batches into which records will be split; default is 16; N temporary files are created and each record from the input is written to a temporary file based on its read name; then each batch is loaded into memory and duplicate records are resolved
-o, --out	output file; default is terminal (stdout)
kevlar augment
Internally, kevlar annotates sequences with “interesting k-mers” and uses “augmented” Fastq and Fasta formats. Processing sequences with third-part tools usually requires discarding these annotations. This command is used to augment/reaugment a set of sequences using annotations from an already augmented sequence file.
usage: kevlar augment [-h] [-o FILE] augseqs seqs
Positional Arguments
augseqs	augmented sequence file
seqs	sequences to annotate
Named Arguments
-o, --out	output file; default is terminal (stdout)
kevlar mutate
Apply the specified mutations to the genome provided.

usage: kevlar mutate [-h] [-o FILE] mutations genome
Positional Arguments
mutations	mutations file
genome	genome to mutate
Named Arguments
-o, --out	output file; default is terminal (stdout)
