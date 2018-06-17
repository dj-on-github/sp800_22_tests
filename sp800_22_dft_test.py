
# sp800_22_dft_test.py
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
import numpy
import sys

def dft_test(bits):
    n = len(bits)
    if (n % 2) == 1:        # Make it an even number
        bits = bits[:-1]

    ts = list()             # Convert to +1,-1
    for bit in bits:
        ts.append((bit*2)-1)

    ts_np = numpy.array(ts)
    fs = numpy.fft.fft(ts_np)  # Compute DFT
   
    if sys.version_info > (3,0):
        mags = abs(fs)[:n//2] # Compute magnitudes of first half of sequence
    else:
        mags = abs(fs)[:n/2] # Compute magnitudes of first half of sequence
    
    T = math.sqrt(math.log(1.0/0.05)*n) # Compute upper threshold
    N0 = 0.95*n/2.0
    print("  N0 = %f" % N0)

    N1 = 0.0   # Count the peaks above the upper theshold
    for mag in mags:
        if mag < T:
            N1 += 1.0
    print("  N1 = %f" % N1)
    d = (N1 - N0)/math.sqrt((n*0.95*0.05)/4) # Compute the P value
    p = math.erfc(abs(d)/math.sqrt(2))

    success = (p >= 0.01)
    return (success,p,None)

