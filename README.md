# sp800_22_tests
A python implementation of the SP800-22 Rev 1a PRNG test suite.

The NIST STS-2.1.2 implementation of the SP800-22 Rev1a tests has some problems. It tends to crash a lot and give the wrong result.

This implementation provides a separate python file, one for each test and a program to read a binary data file and send it to each of the tests. The summary results are output at the end.

In the example below a 1 Mibibit uniform random binary file is generated with djenrandom and run through the test.

$ djenrandom -b -k 128 > megabitrand.bin
$ ./sp800_22_tests.py megabitrand.bin
Tests of Distinguishability from Random
TEST: monobit_test
  Ones count   = 523619
  Zeroes count = 524957
  PASS
  P=0.191334792562

[ Lots of per test output ]

SUMMARY
-------
monobit_test                             0.191334792562   PASS
frequency_within_block_test              0.866040491238   PASS
runs_test                                0.45073315513    PASS
longest_run_ones_in_a_block_test         0.464001170438   PASS
binary_matrix_rank_test                  0.405449005115   PASS
dft_test                                 0.852965102607   PASS
non_overlapping_template_matching_test   1.0              PASS
overlapping_template_matching_test       0.91976483935    PASS
maurers_universal_test                   0.998884573989   PASS
linear_complexity_test                   0.0406698787073  PASS
serial_test                              0.895646559993   PASS
approximate_entropy_test                 0.895690030562   PASS
cumulative_sums_test                     0.18603533058    PASS
random_excursion_test                    0.151908516968   PASS
random_excursion_variant_test            0.019160041631   PASS
