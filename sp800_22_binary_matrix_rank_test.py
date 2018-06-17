#!/usr/bin/env python

# sp800_22_binary_matrix_rank_test.pylon
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
import copy
import gf2matrix

def binary_matrix_rank_test(bits,M=32,Q=32):
    n = len(bits)
    N = int(math.floor(n/(M*Q))) #Number of blocks
    print("  Number of blocks %d" % N)
    print("  Data bits used: %d" % (N*M*Q))
    print("  Data bits discarded: %d" % (n-(N*M*Q))) 
    
    if N < 38:
        print("  Number of blocks must be greater than 37")
        p = 0.0
        return False,p,None
        
    # Compute the reference probabilities for FM, FMM and remainder 
    r = M
    product = 1.0
    for i in range(r):
        upper1 = (1.0 - (2.0**(i-Q)))
        upper2 = (1.0 - (2.0**(i-M)))
        lower = 1-(2.0**(i-r))
        product = product * ((upper1*upper2)/lower)
    FR_prob = product * (2.0**((r*(Q+M-r)) - (M*Q)))
    
    r = M-1
    product = 1.0
    for i in range(r):
        upper1 = (1.0 - (2.0**(i-Q)))
        upper2 = (1.0 - (2.0**(i-M)))
        lower = 1-(2.0**(i-r))
        product = product * ((upper1*upper2)/lower)
    FRM1_prob = product * (2.0**((r*(Q+M-r)) - (M*Q)))
    
    LR_prob = 1.0 - (FR_prob + FRM1_prob)
    
    FM = 0      # Number of full rank matrices
    FMM = 0     # Number of rank -1 matrices
    remainder = 0
    for blknum in range(N):
        block = bits[blknum*(M*Q):(blknum+1)*(M*Q)]
        # Put in a matrix
        matrix = gf2matrix.matrix_from_bits(M,Q,block,blknum) 
        # Compute rank
        rank = gf2matrix.rank(M,Q,matrix,blknum)

        if rank == M: # count the result
            FM += 1
        elif rank == M-1:
            FMM += 1  
        else:
            remainder += 1

    chisq =  (((FM-(FR_prob*N))**2)/(FR_prob*N))
    chisq += (((FMM-(FRM1_prob*N))**2)/(FRM1_prob*N))
    chisq += (((remainder-(LR_prob*N))**2)/(LR_prob*N))
    p = math.e **(-chisq/2.0)
    success = (p >= 0.01)
    
    print("  Full Rank Count  = ",FM)
    print("  Full Rank -1 Count = ",FMM)
    print("  Remainder Count = ",remainder) 
    print("  Chi-Square = ",chisq)

    return (success, p, None)
