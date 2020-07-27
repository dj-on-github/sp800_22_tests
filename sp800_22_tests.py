#!/usr/bin/env python

# sp800_22_tests.py
# 
# Copyright (C) 2017 David Johnston
# This program is distributed under the terms of the GNU General Public License.
# 
# This file is part of sp800_22_tests.
# 
# sp800_22_tests is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# sp800_22_tests is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with sp800_22_tests.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

import argparse
import sys
import numpy


def read_bits_from_file(filename,bigendian):
    bitlist = list()
    if filename == None:
        f = sys.stdin
    else:
        f = open(filename, "rb")
    while True:
        bytes = f.read(16384)
        if bytes:
            for bytech in bytes:
                if sys.version_info > (3,0):
                    byte = bytech
                else:
                    byte = ord(bytech) 
                for i in range(8):
                    if bigendian:
                        bit = (byte & 0x80) >> 7
                        byte = byte << 1
                    else:
                        bit = (byte >> i) & 1
                    bitlist.append(bit)    
        else:
            break
    f.close()
    return bitlist

import argparse
import sys
import matplotlib.pyplot
import scipy.stats
parser = argparse.ArgumentParser(description='Test data for distinguishability form random, using NIST SP800-22Rev1a algorithms.')
parser.add_argument('alphabet_size', type=int, help='Size of alphabet to consider')
parser.add_argument('filename', type=str, nargs='?', help='Filename of binary file to test')
parser.add_argument('--be', action='store_false',help='Treat data as big endian bits within bytes. Defaults to little endian')
parser.add_argument('-t', '--testname', default=None,help='Select the test to run. Defaults to running all tests. Use --list_tests to see the list')
parser.add_argument('--list_tests', action='store_true',help='Display the list of tests')
parser.add_argument('--mode', default="default", type=str)

args = parser.parse_args()

bigendian = args.be
filename = args.filename
sigma = args.alphabet_size

# X 3.1  Frequency (Monobits) Test
# X 3.2  Frequency Test within a Block
# X 3.3  Runs Test
# X 3.4  Test for the Longest Run of Ones in a Block
# X 3.5  Binary Matrix Rank Test
# X 3.6  Discrete Fourier Transform (Specral) Test
# X 3.7  Non-Overlapping Template Matching Test
# X 3.8  Overlapping Template Matching Test
# X 3.9  Maurers Universal Statistical Test
# X 3.10 Linear Complexity Test
# X 3.11 Serial Test
# X 3.12 Approximate Entropy Test
# X 3.13 Cumulative Sums Test
# X 3.14 Random Excursions Test
# X 3.15 Random Excursions Variant Test 


testlist = ['frequency_within_block_test']

if args.mode == "histogram":
    p_values = []
    for i in range(0, 10000):
        arr = numpy.random.randint(0, sigma, 100000)
        m = __import__("sp800_22_frequency_within_block_test")
        func = getattr(m, "frequency_within_block_test")
        (success,p,plist) = func(arr, sigma)
        p_values.append(p)

    matplotlib.pyplot.hist(p_values, 10)
    matplotlib.pyplot.show()
    statistic, kspvalue = scipy.stats.kstest(p_values, 'uniform')
    print(kspvalue)

else:
    arr = numpy.random.randint(0, sigma, 100000)
    results = list()
    
    for testname in testlist:
        print("TEST: %s" % testname)
        m = __import__ ("sp800_22_"+testname)
        func = getattr(m,testname)
        
        (success,p,plist) = func(arr, sigma)

        summary_name = testname
        if success:
            print("  PASS")
            summary_result = "PASS"
        else:
            print("  FAIL")
            summary_result = "FAIL"
        
        if p != None:
            print("  P="+str(p))
            summary_p = str(p)
            
        if plist != None:
            for pval in plist:
                print("P="+str(pval))
            summary_p = str(min(plist))
        
        results.append((summary_name,summary_p, summary_result))
        
    print()
    print("SUMMARY")
    print("-------")
    
    for result in results:
        (summary_name,summary_p, summary_result) = result
        print(summary_name.ljust(40),summary_p.ljust(18),summary_result)
    
