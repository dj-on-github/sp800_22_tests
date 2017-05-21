# sp800_22_tests
A python implementation of the SP800-22 Rev 1a PRNG test suite.

The NIST STS-2.1.2 implementation of the SP800-22 Rev1a tests has some problems. It tends to crash a lot and give the wrong result.

This implementation provides a separate python file, one for each test and a program to read a binary data file and send it to each of the tests. The summary results are output at the end.

In the example below a 1 Mibibit uniform random binary file is generated with djenrandom (https://github.com/dj-on-github/djenrandom) and run through the test.

```
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
```

Next we create a biased data file, where the probability of a 1 is 40% and a 0 is 60% and run it through the test.

```
$ djenrandom -b -k 128 -m biased --bias=0.4 > biased_megabitrand.bin
$ ./sp800_22_tests.py biased_megabitrand.bin
Tests of Distinguishability from Random
TEST: monobit_test
  Ones count   = 420122
  Zeroes count = 628454
  FAIL

[ Lots of per test output ]

SUMMARY
-------
monobit_test                             0.0                FAIL
frequency_within_block_test              0.0                FAIL
runs_test                                0.0                FAIL
longest_run_ones_in_a_block_test         1.81518103863e-81  FAIL
binary_matrix_rank_test                  0.22156738316      PASS
dft_test                                 3.56787241447e-17  FAIL
non_overlapping_template_matching_test   0.759928185368     PASS
overlapping_template_matching_test       5.31335556946e-91  FAIL
maurers_universal_test                   0.910613044038     PASS
linear_complexity_test                   0.317575269575     PASS
serial_test                              0.0                FAIL
approximate_entropy_test                 0.0                FAIL
cumulative_sums_test                     0.0                FAIL
random_excursion_test                    9.15178471457e-06  FAIL
random_excursion_variant_test            0.121267812518     PASS
```

Next we create some serially correlated data and run it through the tests.

```
$ djenrandom -b -k 128 -m correlated --correlation=-0.2 > correlated_megrandom.bin
$ ./sp800_22_tests.py correlated_megabitrand.bin
Tests of Distinguishability from Random
TEST: monobit_test
  Ones count   = 524242
  Zeroes count = 524334
  PASS
  P=0.928411381275

[ Lots of per test output ]

SUMMARY
-------
monobit_test                             0.928411381275     PASS
frequency_within_block_test              0.99598493834      PASS
runs_test                                0.0                FAIL
longest_run_ones_in_a_block_test         3.45886379519e-81  FAIL
binary_matrix_rank_test                  0.379259346315     PASS
dft_test                                 8.67506291511e-16  FAIL
non_overlapping_template_matching_test   0.999999863695     PASS
overlapping_template_matching_test       1.1953875512e-90   FAIL
maurers_universal_test                   0.923207164612     PASS
linear_complexity_test                   0.47696777353      PASS
serial_test                              0.0                FAIL
approximate_entropy_test                 0.0                FAIL
cumulative_sums_test                     0.853890590584     PASS
random_excursion_test                    7.63411305092e-09  FAIL
random_excursion_variant_test            0.0662033926665    PASS
```

Next we create some data with both bias and serial correlation from an Ornstein–Uhlenbeck process and run it through the tool

```
$ djenrandom -b -k 128 -m sums -l 0.2 -r 0.3 > sums_megrandom.bin
$ ./sp800_22_tests.py sums_megrandom.bin
Tests of Distinguishability from Random
TEST: monobit_test
  Ones count   = 419429
  Zeroes count = 629147
  FAIL
  P=0.0

[ Lots of per test output ]

SUMMARY
-------
monobit_test                             0.0                FAIL
frequency_within_block_test              0.0                FAIL
runs_test                                0.0                FAIL
longest_run_ones_in_a_block_test         2.32811341972e-159 FAIL
binary_matrix_rank_test                  0.702984863193     PASS
dft_test                                 7.91957168353e-06  FAIL
non_overlapping_template_matching_test   0.949847572332     PASS
overlapping_template_matching_test       1.16046343793e-137 FAIL
maurers_universal_test                   0.90191137295      PASS
linear_complexity_test                   0.16038668337      PASS
serial_test                              0.0                FAIL
approximate_entropy_test                 0.0                FAIL
cumulative_sums_test                     0.0                FAIL
random_excursion_test                    2.20517667303e-09  FAIL
random_excursion_variant_test            0.0                FAIL
```

