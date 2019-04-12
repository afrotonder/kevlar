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

You can checkout or download kevlar at our <a href='https://github.com/dib-lab/kevlar
Link to documentation: https://kevlar.readthedocs.io
'> GitHub </a>

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

    $ pip3 install pysam networkx pandas scipy intervaltree git+https://github.com/dib-lab/khmer.git

    $ pip3 install biokevlar

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

This is the most surefire way to really see what kevlar is made of. To run the Snake

To do so, you first need some genome files in fas   

<h1>Setup development environment for Kevlar</h1>



[travisbadge]: https://img.shields.io/travis/dib-lab/kevlar.svg
[pypibadge]: https://img.shields.io/pypi/v/biokevlar.svg
[codecovbadge]: https://img.shields.io/codecov/c/github/dib-lab/kevlar.svg
[rtdbadge]: https://readthedocs.org/projects/kevlar/badge/?version=latest&maxAge=900
[dockerbadge]: https://quay.io/repository/dib-lab/kevlar/status
[licensebadge]: https://img.shields.io/badge/license-MIT-blue.svg
