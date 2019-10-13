#!/usr/bin/env python

# sp800_22_maurers_universal_test.pylon
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

def pattern2int(pattern):
    l = len(pattern)
    n = 0
    for bit in (pattern):
        n = (n << 1) + bit
    return n          
         
def maurers_universal_test(bits,patternlen=None, initblocks=None):
    n = len(bits)

    # Step 1. Choose the block size
    if patternlen != None:
        L = patternlen  
    else: 
        ns = [904960,2068480,4654080,10342400,
              22753280,49643520,107560960,
              231669760,496435200,1059061760]
        L = 6
        if n < 387840:
            print("Error. Need at least 387840 bits. Got %d." % n)
            #exit()
            return False,0.0,None
        for threshold in ns:
            if n >= threshold:
                L += 1 

    # Step 2 Split the data into Q and K blocks
    nblocks = int(math.floor(n/L))
    if initblocks != None:
        Q = initblocks
    else:
        Q = 10*(2**L)
    K = nblocks - Q
    
    # Step 3 Construct Table
    nsymbols = (2**L)
    T=[0 for x in range(nsymbols)] # zero out the table
    for i in range(Q):             # Mark final position of
        pattern = bits[i*L:(i+1)*L] # each pattern
        idx = pattern2int(pattern)
        T[idx]=i+1      # +1 to number indexes 1..(2**L)+1
                        # instead of 0..2**L
    # Step 4 Iterate
    sum = 0.0
    for i in range(Q,nblocks):
        pattern = bits[i*L:(i+1)*L]
        j = pattern2int(pattern)
        dist = i+1-T[j]
        T[j] = i+1
        sum = sum + math.log(dist,2)
    print("  sum =", sum)
    
    # Step 5 Compute the test statistic
    fn = sum/K
    print("  fn =",fn)
       
    # Step 6 Compute the P Value
    # Tables from https://static.aminer.org/pdf/PDF/000/120/333/
    # a_universal_statistical_test_for_random_bit_generators.pdf
    ev_table =  [0,0.73264948,1.5374383,2.40160681,3.31122472,
                 4.25342659,5.2177052,6.1962507,7.1836656,
                 8.1764248,9.1723243,10.170032,11.168765,
                 12.168070,13.167693,14.167488,15.167379]
    var_table = [0,0.690,1.338,1.901,2.358,2.705,2.954,3.125,
                 3.238,3.311,3.356,3.384,3.401,3.410,3.416,
                 3.419,3.421]
                 
    # sigma = math.sqrt(var_table[L])
    mag = abs((fn - ev_table[L]) / ((0.7 - 0.8 / L + (4 + 32 / L) * (pow(K, -3 / L)) / 15) * (math.sqrt(var_table[L] / K)) * math.sqrt(2)))
    P = math.erfc(mag)

    success = (P >= 0.01)
    return (success, P, None)
    

if __name__ == "__main__":
    bits = [0,1,0,1,1,0,1,0,0,1,1,1,0,1,0,1,0,1,1,1]
    success, p, _ = maurers_universal_test(bits, patternlen=2, initblocks=4)
    
    print("success =",success)
    print("p       = ",p)
    
