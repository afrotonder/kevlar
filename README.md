[![kevlar build status][travisbadge]](https://travis-ci.org/dib-lab/kevlar)
[![PyPI version][pypibadge]](https://pypi.python.org/pypi/biokevlar)
[![Test coverage][codecovbadge]](https://codecov.io/github/dib-lab/kevlar)
[![kevlar documentation][rtdbadge]](http://kevlar.readthedocs.io/en/latest/?badge=latest)
[![Docker build status][dockerbadge]](https://quay.io/repository/dib-lab/kevlar)
[![MIT licensed][licensebadge]](https://github.com/dib-lab/kevlar/blob/master/LICENSE)

<!-- <img src="docs/_static/morpheus-kevlar.jpg" alt=" What if I told you we don't need alignments to find variants?" width="400px" /> -->

# kevlar

Daniel Standage, 2016-2019  
https://kevlar.readthedocs.io

Welcome to **kevlar**, software for predicting *de novo* genetic variants without mapping reads to a reference genome!
kevlar's *k*-mer abundance based method calls single nucleotide variants (SNVs), multinucleotide variants (MNVs), insertion/deletion variants (indels), and structural variants (SVs) simultaneously with a single simple model.
This software is free for use under the MIT license.

You can checkout or download kevlar at our <a href='https://github.com/dib-lab/kevlar'>GitHub </a> or learn how to install below.

Here's a link to the kevlar documentation: https://kevlar.readthedocs.io
 

<h1>Setup Virtual Environment for Kevlar</h1>

We recommend installing kevlar and its dependencies in a dedicated virtual environment 
using [venv](https://docs.python.org/3/library/venv.html) or [conda](https://conda.io/en/latest/).

The following commands create a virtual environment for venv and conda respectively. These only
need to be executed once. 

<h3>venv</h3>

    $ python3 -m venv kevlar-env 

<h3>conda</h3>

    $ conda create --name kevlar-env python=3.6 

The following commands activate your virtual environment for venv and conda respectively. 
These need to be will need to be re-executed any time you open a new session in your terminal.

<h3>venv</h3>

    $ source kevlar-env/bin/activate
    
<h3>conda</h3>

    $ source activate kevlar-env 


<h1>Download Kevlar</h1>

The following commands install kevlar and all of its dependencies. 


<h3>Unix like OS:</h3>

    $ pip3 install snakemake pysam networkx pandas scipy intervaltree git+https://github.com/dib-lab/khmer.git

    $ pip3 install biokevlar

*If you choose not to setup a virtual environment, the snakemake dependency will require you
you to **sudo** install.

<h3>Windows OS:</h3>
  
     ¯\_(ツ)_/¯


<h1>Genome Files</h1>

To use kevlar you need some genome files in FASTA(.fa) and/or FASTQ(.fq) format. If you have your own, go on
ahead to the How To Run Kevlar section below. 

If you need some genomic data, this simulated 25 Mb genome and can be downloaded anonymously from the (Open Science Framework)[https://osf.io/anr56/]
or if youd rather not leave the terminal/editor, curl is another option. 

    curl -L https://s3-us-west-1.amazonaws.com/noble-trios/neon-mother-reads.fq.gz -o mother.fq.gz
    curl -L https://s3-us-west-1.amazonaws.com/noble-trios/neon-father-reads.fq.gz -o father.fq.gz
    curl -L https://s3-us-west-1.amazonaws.com/noble-trios/neon-proband-reads.fq.gz -o proband.fq.gz
    curl -L https://s3-us-west-1.amazonaws.com/noble-trios/neon-refr.fa.gz -o refr.fa.gz

<h1>How to run Kevlar</h1>

<h2>Reference genome Indexing with BWA</h2>

Before running kevlar, you need to index the reference genome using the BWA package installed above.

BWA is a software package for mapping DNA sequences against a large reference genome, such as the human genome.
It consists of three algorithms: BWA-backtrack, BWA-SW and BWA-MEM. The first algorithm is designed for Illumina 
sequence reads up to 100bp, while the rest two for longer sequences ranged from 70bp to a few megabases. 
BWA-MEM and BWA-SW share similar features such as the support of long reads and chimeric alignment, but BWA-MEM,
which is the latest, is generally recommended as it is faster and more accurate. BWA-MEM also has better
performance than BWA-backtrack for 70-100bp Illumina reads.

For all the algorithms, BWA first needs to construct the FM-index for the reference genome (the index command).
Alignment algorithms are invoked with different sub-commands: aln/samse/sampe for BWA-backtrack,
bwasw for BWA-SW and mem for the BWA-MEM algorithm.

<h3> How to index: </h3>

    $ git clone https://github.com/lh3/bwa.git
    $ cd bwa
    $ make
    $ bwa index ref.fa


<h2>kevlar CLI</h2>

Running kevlar is a no brainer with its integrated CLI! This lets you run kevlar commands like count, novel, partition, etc.
individually to the file.

Enter [the official kevlar  documentation](https://kevlar.readthedocs.io/en/latest/cli.html#kevlar-count-api) for instructions on how to run each command with examples. 
Alternatively, there is a [Markdown file](kevlar-cli-doc.md) containing the whole cli documentation bundled with the project.


<h2>kevlar Snakemake Workflow</h2>

[Snakemake](https://snakemake.readthedocs.io/en/stable/) is a workflow manager for Python data projects.
It helps automate processes like sequencing, filtering, and counting kmers. 

This is the most surefire way to really see what kevlar is made of. Before running the snakemake workflow,
a few things need to be setup. 

First, assuming you have your genomic files already downloaded, a config.json file
will need to be setup for snakemake. From your kevlar root folder, navigate to this path:

    $ cd kevlar/workflows/mark-I/

Here you will see three files: config.json, <span>README.md</span>, and Snakefile. The file we want to edit is config.json.

Setting up the config.json file is simple. Open it in your favorite editor and replace 
the existing filenames with the full paths of your input files. This is explained below.

<h3>config.json Setup</h3>

This json file will hold all the data that will be fed to the Snakemake workflow.
Files fed can be zipped or unzipped, and _fastx_ means fasta or fastq files are welcome.
Otherwise, the property will specify if the file should be either.

Line 5 defines the _samples_ property, which nests the _case_ and _controls_ properties to be edited. 

 1. _case_ has its own property _fastx_ which holds the path to the proband file.

 2.  _controls_ has two _fastx_ properties which will hold the paths to the 'mother' and 'father' genomes, respectively.
    The terms mother and father follow the default test case kevlar has uppon installing, 
    but feel free to rename them to your use.

Line 39 defines the _mask_ property, which nests the _fastx_ property to be edited.

 1. _fastx_ property holds the path to the reference genome file (i.e [human genome](https://osf.io/anr56/)).
 
Line 46 defines the _reference_ property, which nests the *fasta* property to be edited.
Note: *this file must be in fasta format, not fastq.* 

 1. _fasta_ property holds the path to the *fasta* format reference genome file (i.e [human genome](https://osf.io/anr56/))

Once you have those file paths setup, youre ready to run snakemake.

<h3>Running Kevlar Snakemake Workflow Mark I</h3>

To check if the snakemake worflow is setup correctly, start by running the following dry run:

    $ snakemake --configfile path/to/config.json --snakefile kevlar/workflows/mark-I/Snakefile --cores 64 --directory /path/to/desired/work/dir/ --printshellcmds --dryrun calls

If no warnings are output, youre good to go! To run the kevlar snakemake workflow, run the same command
but exclude the _--dryrun_ flag like so:

    $ snakemake --configfile path/to/config.json --snakefile kevlar/workflows/mark-I/Snakefile --cores 64 --directory /path/to/desired/work/dir/ --printshellcmds calls

Thats it for the snakemake workflow! Congrats if you hade it here smoothly!
If youre here and are recieving errors, its probably permissions or a missing dependency.
Read that output carefully and youll probably get it fixed in a jiffy. This is a pretty straighforward
process and the common errors are the ones mentioned. We hope kevlar helps you progress!


<h1>Setup development environment for Kevlar</h1>

If you’d like to contribute to kevlar’s development or simply poke around, the source code can be 
cloned from the [official kevlar github](https://github.com/dib-lab/kevlar.git) or by following the 
steps provided below. Also, in addition to the dependencies listed above, a few additional dependencies are 
required for a complete development environment. These can be installed with make for your convenience.

    $ git clone https://github.com/dib-lab/kevlar.git
    $ cd kevlar
    $ make devenv
    $ pip3 install -e

Hack away! Feel free to ask questions or submit bug reports to the kevlar issue tracker.


<h1>Miscellaneous Information</h1>

<h2>kevlar Snakemake Workflow in detail</h2>

Here's a simple step by step rundown of what the snakemake workflow does:

<h3>Step 0: count k-mers </h3>

The kevlar count command is used to count k-mers for each sample, as well as for the reference genome and the mask.
 
<h3>Step 1: find interesting k-mers</h3>

The kevlar novel command uses pre-computed k-mer counts to find reads containing novel k-mers using the specified thresholds.

<h3>Step 2: filter k-mers and reads</h3>

The kevlar filter command recomputes k-mer counts and filters out k-mers with insufficient abundance or k-mers from contaminant sources. Any reads that no longer have any interesting k-mers after filtering are discarded.
 
<h3>Step 3: partition reads</h3>

Reads spanning the same variant will typically share numerous interesting k-mers. The kevlar partition command groups reads based on shared novel k-mers.
 
<h3>Step 4: contig assembly</h3>

The kevlar assemble command assembles each partition of reads into contigs for variant annotation.
 
<h3>Step 5: localize reference targets</h3>

The kevlar localize command identifies the appropriate target (or set of targets) in the reference genome for aligning each variant-spanning contig for variant annotation.
 
<h3>Step 6: call variants</h3>

The kevlar call command computes a full dynamic programming alignment of each reference-spanning contig to its corresponding reference target(s) and calls variants based on the alignment path.
 
<h3>Step 7: score and rank variant calls</h3>

The kevlar simlike command computes a likelihood score for each variant prediction and ranks variant calls based on this score.



<h2>Some notes on workflow configuration</h2>

1. An arbitrary number of Fasta/Fastq files is supported for each sample.

2. Paired-end reads are not required, and any pairing information will be ignored.

3. Parameters are tuned for error-corrected whole genome shotgun sequencing of human samples at ≈30x coverage. Without error correction much more memory will be required, or an alternative workflow will be required.

4. kevlar will be accurate even when the k-mer counting false-positive rate (FPR) is fairly high in the case sample, as this is corrected in subsequent steps. Sensitivity will be lost if the k-mer counting FPR is too high in the control samples, however.

5. The mask should include your reference genome and any potential sources of contamination. For example, UniVec includes many sources of technical contamination (such as adapters) that often cause problems.

6. Accuracy can often be improved by filtering preliminary calls. Use the varfilter setting to provide a BED file of intervals from which to filter out variant predictions (by default, varfilter: null will disable this step). It's common to filter out variant calls in segmental duplications or SSRs, for example, as these are usually problematic. Also, filtering out common variants (using dbSNP, for example) will successfully remove inherited variants that are erroneously classified as de novo due to low coverage in the donor parent.


[travisbadge]: https://img.shields.io/travis/dib-lab/kevlar.svg
[pypibadge]: https://img.shields.io/pypi/v/biokevlar.svg
[codecovbadge]: https://img.shields.io/codecov/c/github/dib-lab/kevlar.svg
[rtdbadge]: https://readthedocs.org/projects/kevlar/badge/?version=latest&maxAge=900
[dockerbadge]: https://quay.io/repository/dib-lab/kevlar/status
[licensebadge]: https://img.shields.io/badge/license-MIT-blue.svg
