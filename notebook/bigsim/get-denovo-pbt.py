#!/usr/bin/env python
#
# -----------------------------------------------------------------------------
# Copyright (c) 2018 The Regents of the University of California
#
# This file is part of kevlar (http://github.com/dib-lab/kevlar) and is
# licensed under the MIT license: see LICENSE.
# -----------------------------------------------------------------------------

import kevlar
import sys

reader = kevlar.vcf.VCFReader(sys.stdin)
writer = kevlar.vcf.VCFWriter(sys.stdout)
for varcall in reader:
    momgt = varcall.format('Mom_30x', 'GT')
    dadgt = varcall.format('Dad_30x', 'GT')
    kidgt = varcall.format('Kid_30x', 'GT')
    if momgt in ('0|0', '0/0') and dadgt in ('0|0', '0/0') and kidgt in ('0|1', '1|0', '0/1', '1/0'):
        writer.write(varcall)
