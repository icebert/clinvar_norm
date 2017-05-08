#!/bin/env python

import sys
import hgvs.parser

hp  = hgvs.parser.Parser()

for var in sys.stdin:
    var = var.rstrip('\n')
    var_i = hp.parse_hgvs_variant(var)
    print(str(var_i))



