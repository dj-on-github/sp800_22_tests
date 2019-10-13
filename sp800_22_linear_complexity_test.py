#!/usr/bin/env python

# sp800_22_lirear_complexity_test.py
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

def berelekamp_massey(bits):
    n = len(bits)
    b = [0 for x in bits]  #initialize b and c arrays
    c = [0 for x in bits]
    b[0] = 1
    c[0] = 1
    
    L = 0
    m = -1
    N = 0
    while (N < n):
        #compute discrepancy
        d = bits[N]
        for i in range(1,L+1):
            d = d ^ (c[i] & bits[N-i])
        if (d != 0):  # If d is not zero, adjust poly
            t = c[:]
            for i in range(0,n-N+m):
                c[N-m+i] = c[N-m+i] ^ b[i] 
            if (L <= (N/2)):
                L = N + 1 - L
                m = N
                b = t 
        N = N +1
    # Return length of generator and the polynomial
    return L , c[0:L]
    
def linear_complexity_test(bits,patternlen=None):
    n = len(bits)
    # Step 1. Choose the block size
    if patternlen != None:
        M = patternlen  
    else: 
        if n < 1000000:
            print("Error. Need at least 10^6 bits")
            #exit()
            return False,0.0,None
        M = 512
    K = 6 
    N = int(math.floor(n/M))
    print("  M = ", M)
    print("  N = ", N)
    print("  K = ", K)    
    
    # Step 2 Compute the linear complexity of the blocks
    LC = list()
    for i in range(N):
        x = bits[(i*M):((i+1)*M)]
        LC.append(berelekamp_massey(x)[0])
    
    # Step 3 Compute mean
    a = float(M)/2.0
    b = ((((-1)**(M+1))+9.0))/36.0
    c = ((M/3.0) + (2.0/9.0))/(2**M)
    mu =  a+b-c
    
    T = list()
    for i in range(N):
        x = ((-1.0)**M) * (LC[i] - mu) + (2.0/9.0)
        T.append(x)
        
    # Step 4 Count the distribution over Ticket
    v = [0,0,0,0,0,0,0]
    for t in T:
        if t <= -2.5:
            v[0] += 1
        elif t <= -1.5:
            v[1] += 1
        elif t <= -0.5:
            v[2] += 1
        elif t <= 0.5:
            v[3] += 1
        elif t <= 1.5:
            v[4] += 1
        elif t <= 2.5:
            v[5] += 1            
        else:
            v[6] += 1

    # Step 5 Compute Chi Square Statistic
    pi = [0.010417,0.03125,0.125,0.5,0.25,0.0625,0.020833]
    chisq = 0.0
    for i in range(K+1):
        chisq += ((v[i] - (N*pi[i]))**2.0)/(N*pi[i])
    print("  chisq = ",chisq)
    # Step 6 Compute P Value
    P = gammaincc((K/2.0),(chisq/2.0))
    print("  P = ",P)
    success = (P >= 0.01)
    return (success, P, None)
    
if __name__ == "__main__":
    bits = [1,1,0,1,0,1,1,1,1,0,0,0,1]
    L,poly = berelekamp_massey(bits)

    bits = [1,1,0,1,0,1,1,1,1,0,0,0,1,1,1,0,1,0,1,1,1,1,0,0,
            0,1,1,1,0,1,0,1,1,1,1,0,0,0,1,1,1,0,1,0,1,1,1,1,
            0,0,0,1,1,1,0,1,0,1,1,1,1,0,0,0,1]
    success,p,_ = linear_complexity_test(bits,patternlen=7)
    
    print("L =",L)
    print("p = ",p)
       
