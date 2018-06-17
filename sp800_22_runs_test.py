#!/usr/bin/env python

# sp800_22_runs_test.py
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

import math
from fractions import Fraction
#from scipy.special import gamma, gammainc, gammaincc
from gamma_functions import *
import numpy
import cmath
import random

#ones_table = [bin(i)[2:].count('1') for i in range(256)]
def count_ones_zeroes(bits):
    ones = 0
    zeroes = 0
    for bit in bits:
        if (bit == 1):
            ones += 1
        else:
            zeroes += 1
    return (zeroes,ones)

def runs_test(bits):
    n = len(bits)
    zeroes,ones = count_ones_zeroes(bits)

    prop = float(ones)/float(n)
    print("  prop ",prop)

    tau = 2.0/math.sqrt(n)
    print("  tau ",tau)

    if abs(prop-0.5) > tau:
        return (False,0.0,None)

    vobs = 1.0
    for i in range(n-1):
        if bits[i] != bits[i+1]:
            vobs += 1.0

    print("  vobs ",vobs)
      
    p = math.erfc(abs(vobs - (2.0*n*prop*(1.0-prop)))/(2.0*math.sqrt(2.0*n)*prop*(1-prop) ))
    success = (p >= 0.01)
    return (success,p,None)


