#!/usr/bin/env python2.7

import doctest
doctest.testfile("xor.txt",
    optionflags=doctest.REPORT_ONLY_FIRST_FAILURE|doctest.ELLIPSIS)
doctest.testfile("multipleoutput.txt",
    optionflags=doctest.REPORT_ONLY_FIRST_FAILURE|doctest.ELLIPSIS)
doctest.testfile("trainer.txt",
    optionflags=doctest.REPORT_ONLY_FIRST_FAILURE|doctest.ELLIPSIS)
