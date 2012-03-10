#!/usr/bin/env python2.7

import doctest


files = ("trainer.txt", "xor.txt", "multipleoutput.txt")
opts = doctest.REPORT_ONLY_FIRST_FAILURE|doctest.ELLIPSIS

for f in files:
    doctest.testfile(f, optionflags=opts)
