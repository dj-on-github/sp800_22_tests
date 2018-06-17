#!/usr/bin/env python

# sp800_22_serial_test.py
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
#from scipy.special import gamma, gammainc, gammaincc
from gamma_functions import *

def int2patt(n,m):
    pattern = list()
    for i in range(m):
        pattern.append((n >> i) & 1)
    return pattern
    
def countpattern(patt,bits,n):
    thecount = 0
    for i in range(n):
        match = True
        for j in range(len(patt)):
            if patt[j] != bits[i+j]:
                match = False
        if match:
            thecount += 1
    return thecount

def psi_sq_mv1(m, n, padded_bits):
    counts = [0 for i in range(2**m)] 
    for i in range(2**m):
        pattern = int2patt(i,m)
        count = countpattern(pattern,padded_bits,n)
        counts.append(count)
        
    psi_sq_m = 0.0
    for count in counts: 
        psi_sq_m += (count**2)
    psi_sq_m = psi_sq_m * (2**m)/n 
    psi_sq_m -= n
    return psi_sq_m            
         
def serial_test(bits,patternlen=None):
    n = len(bits)
    if patternlen != None:
        m = patternlen  
    else:  
        m = int(math.floor(math.log(n,2)))-2
    
        if m < 4:
            print("Error. Not enough data for m to be 4")
            return False,0,None
        m = 4
    
    # Step 1
    padded_bits=bits+bits[0:m-1]
    
    # Step 2
    psi_sq_m   = psi_sq_mv1(m, n, padded_bits)
    psi_sq_mm1 = psi_sq_mv1(m-1, n, padded_bits)
    psi_sq_mm2 = psi_sq_mv1(m-2, n, padded_bits)    
    
    delta1 = psi_sq_m - psi_sq_mm1
    delta2 = psi_sq_m - (2*psi_sq_mm1) + psi_sq_mm2
    
    P1 = gammaincc(2**(m-2),delta1/2.0)
    P2 = gammaincc(2**(m-3),delta2/2.0)
        
    print("  psi_sq_m   = ",psi_sq_m)
    print("  psi_sq_mm1 = ",psi_sq_mm1)
    print("  psi_sq_mm2 = ",psi_sq_mm2)
    print("  delta1     = ",delta1)
    print("  delta2     = ",delta2)  
    print("  P1         = ",P1)
    print("  P2         = ",P2)
     
    success = (P1 >= 0.01) and (P2 >= 0.01)
    return (success, None, [P1,P2])

if __name__ == "__main__":
    bits = [0,0,1,1,0,1,1,1,0,1]
    success, _, plist = serial_test(bits, patternlen=3)
    
    print("success =",success)
    print("plist = ",plist)
    
