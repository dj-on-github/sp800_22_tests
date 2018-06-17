# gf2matrix.py
#
# Copyright (C) 2017 David Johnston
#
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

import copy

MATRIX_FORWARD_ELIMINATION = 0
MATRIX_BACKWARD_ELIMINATION = 1

def print_matrix(matrix):
    #print "PRINT MATRIX"
    #print "len matrix = ",str(len(matrix))
    #for line in matrix:
    #    print line
    for i in range(len(matrix)):
        #print "Line %d" % i
        line = matrix[i]
        #print "Line %d = %s" % (i,str(line))
        if i==0:
            astr = "["+str(line)+" : "
        else:
            astr += " "+str(line)+" : "
        for ch in line:
            astr = astr + str(ch)
        if i == (len(matrix)-1):
            astr += "]"
        else:
            astr = astr + "\n"
    print(astr)
    #print "END PRINT MATRIX"

    
def row_echelon(M,Q,matrix,blknum):
    lm = copy.deepcopy(matrix)
    
    pivotstartrow = 0
    pivotstartcol = 0
    for i in range(Q):
        # find pivotrow
        found = False
        for k in range(pivotstartrow,Q):
            if lm[k][pivotstartcol] == 1:
                found = True
                pivotrow = k
                break
        
        if found:        
            # Swap with pivot
            if pivotrow != pivotstartrow:
                lm[pivotrow],lm[pivotstartrow] = lm[pivotstartrow],lm[pivotrow]
                    
            # eliminate lower triangle column
            for j in range(pivotstartrow+1,Q):
                if lm[j][pivotstartcol]==1:
                    lm[j] = [x ^ y for x,y in zip(lm[pivotstartrow],lm[j])]  
                
            pivotstartcol += 1
            pivotstartrow += 1
        else:
            pivotstartcol += 1
        
    return lm

def rank(M,Q,matrix,blknum):
    lm = row_echelon(M,Q,matrix,blknum)
    rank = 0
    for i in range(Q):
        nonzero = False
        for bit in lm[i]:
            if bit == 1:
                nonzero = True
        if nonzero:
            rank += 1
    return rank
    
def computeRank(M, Q, matrix):
    m = min(M,Q)
    
    localmatrix = copy.deepcopy(matrix)
    # FORWARD APPLICATION OF ELEMENTARY ROW OPERATIONS  
    for i in range(m-1):
        if ( localmatrix[i][i] == 1 ): 
            localmatrix = perform_elementary_row_operations(MATRIX_FORWARD_ELIMINATION, i, M, Q, localmatrix)
        else: # localmatrix[i][i] = 0 
            row_op,localmatrix = find_unit_element_and_swap(MATRIX_FORWARD_ELIMINATION, i, M, Q, localmatrix)
            if row_op == 1: 
                localmatrix = perform_elementary_row_operations(MATRIX_FORWARD_ELIMINATION, i, M, Q, localmatrix)
        


    # BACKWARD APPLICATION OF ELEMENTARY ROW OPERATIONS  
    for i in range(m-1,0,-1):
    #for ( i=m-1; i>0; i-- ) {
        if ( localmatrix[i][i] == 1 ):
            localmatrix = perform_elementary_row_operations(MATRIX_BACKWARD_ELIMINATION, i, M, Q, localmatrix)
        else: #  matrix[i][i] = 0 
            row_op,localmatrix = find_unit_element_and_swap(MATRIX_BACKWARD_ELIMINATION, i, M, Q, localmatrix) 
            if row_op == 1:
                localmatrix = perform_elementary_row_operations(MATRIX_BACKWARD_ELIMINATION, i, M, Q, localmatrix)

    #for aline in localmatrix:
    #    print " UUU : ",aline
    #print
    
    rank = determine_rank(m, M, Q, localmatrix)

    return rank

def perform_elementary_row_operations(flag, i, M, Q, A):
    j = 0
    k = 0
    
    if ( flag == MATRIX_FORWARD_ELIMINATION ):
        for j in range(i+1,M):
        #for ( j=i+1; j<M;  j++ )
            if ( A[j][i] == 1 ):
                for k in range(i,Q):
                #for ( k=i; k<Q; k++ ) 
                    A[j][k] = (A[j][k] + A[i][k]) % 2
    else: 
        #for ( j=i-1; j>=0;  j-- )
        for j in range(i-1,-1,-1):
            if ( A[j][i] == 1 ):
                for k in range(Q):
                #for ( k=0; k<Q; k++ )
                    A[j][k] = (A[j][k] + A[i][k]) % 2

    return A

def find_unit_element_and_swap(flag, i, M, Q, A):
    index  = 0
    row_op = 0

    if ( flag == MATRIX_FORWARD_ELIMINATION ):
        index = i+1
        while ( (index < M) and (A[index][i] == 0) ):
            index += 1
            if ( index < M ):
                row_op = 1
                A = swap_rows(i, index, Q, A)
    else:
        index = i-1
        while ( (index >= 0) and (A[index][i] == 0) ): 
            index = index -1
            if ( index >= 0 ):
                row_op = 1
                A = swap_rows(i, index, Q, A)
    return row_op,A

def swap_rows(i, index, Q, A):
    A[i],A[index] = A[index],A[i]
    #for p in xrange(Q): 
    #    temp = A[i][p]
    #    A[i][p] = A[index][p]
    #    A[index][p] = temp
    return A

def determine_rank(m, M, Q, A):
    i = 0
    j = 0
    rank = 0
    allZeroes = 0
   
    # DETERMINE RANK, THAT IS, COUNT THE NUMBER OF NONZERO ROWS
    
    rank = m
    for i in range(M):
    #for ( i=0; i<M; i++ ) {
        allZeroes = 1 
        for j in range(Q):
        #for ( j=0; j<Q; j++)  {
            if ( A[i][j] == 1 ):
                allZeroes = 0
                #break
        if ( allZeroes == 1 ):
            rank -= 1
    return rank

def create_matrix(M, Q):
    matrix = list()
    for rownum in range(Q):
        row = [0 for x in range(M)]
        matrix.append(row)
        
    return matrix

def matrix_from_bits(M,Q,bits,blknum):
    m = list()
    for rownum in range(Q):
        row = bits[rownum*M:(rownum+1)*M]
        m.append(row)
    return m[:]

