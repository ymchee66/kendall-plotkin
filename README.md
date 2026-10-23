# Eventual Attainment of the Plotkin Bound for Kendall Permutation Codes in Every Fixed Window

Supplementary material for the paper

> Y. M. Chee, "Eventual attainment of the Plotkin bound for Kendall permutation codes in every fixed window."

## Contents

| Path | Description |
|---|---|
| `codes/n16_M6.txt` | Six permutations of length 16, pairwise at distance 72, every pair of symbols of split three. Used in the proofs of Theorem 9.1(b) and Corollary 9.3. |
| `codes/n8_M8.txt` | The code in Table I (Theorem 9.1(c)). |
| `codes/n7_M7.txt` | The code in Table II (Theorem 9.1(c)). |
| `codes/n5_M5.txt` | The code in Table III (Theorem 9.1(b)). |
| `codes/n14_M6.txt` | Six permutations of length 14, pairwise at distance at least 54. Used in the proofs of Theorem 9.2 and Corollary 9.3. |
| `codes/n17_M6.txt` | Six permutations of length 17, pairwise at distance at least 78. Used in the proof of Corollary 9.3. |
| `codes/n18_M6.txt` | Six permutations of length 18, pairwise at distance at least 90. Used in the proof of Corollary 9.3. |
| `codes/n19_M6.txt` | Six permutations of length 19, pairwise at distance at least 102. Used in the proofs of Theorem 9.2 and Corollary 9.3. |
| `codes/n13_M8.txt` | Eight permutations of length 13, pairwise at distance at least 44. Used in the proofs of Theorem 9.2 and Corollary 9.3. |
| `codes/n14_M10.txt` | Ten permutations of length 14, pairwise at distance at least 50 = 10⌊C(14,2)/18⌋. Used in the proof of Corollary 9.3(d). |
| `codes/n23_M10.txt` | Ten permutations of length 23, pairwise at distance at least 140 = 10⌊C(23,2)/18⌋. Used in the proof of Corollary 9.3(d). |
| `codes/n26_M10.txt` | Ten permutations of length 26, pairwise at distance at least 180 = 10⌊C(26,2)/18⌋. Used in the proof of Corollary 9.3(d). |
| `codes/n30_M10.txt` | Ten permutations of length 30, pairwise at distance at least 240 = 10⌊C(30,2)/18⌋. Used in the proof of Corollary 9.3(d). |
| `codes/n33_M10.txt` | Ten permutations of length 33, pairwise at distance at least 290 = 10⌊C(33,2)/18⌋. Used in the proof of Corollary 9.3(d). |
| `codes/n34_M10.txt` | Ten permutations of length 34, pairwise at distance at least 310 = 10⌊C(34,2)/18⌋. Used in the proof of Corollary 9.3(d). |
| `codes/n35_M10.txt` | Ten permutations of length 35, pairwise at distance at least 330 = 10⌊C(35,2)/18⌋. Used in the proof of Corollary 9.3(d). |
| `codes/n9_M9.txt` | Nine permutations of length nine, pairwise at distance 20 (concluding remarks). |
| `verify.py` | Verifies all codes, lists the small lengths treated in the proof of Corollary 9.3, and carries out the computation for permutation length five in the proof of Theorem 9.1(b). Python 3, standard library only. |
| `expected_output.txt` | Output of `verify.py`. |
| `test_verify.py` | Negative tests: damages copies of the certificates (removing a codeword, duplicating a codeword, lengthening a codeword) or the expected parameters (length, size, distance), and checks that `verify.py` reports a failure in every case. |
| `search/sa.c` | Heuristic simulated annealing program (not needed for verification) used to find the codes of lengths 7 and 8, which attain the Plotkin bound with equal pairwise distances. |
| `search/sa_atleast.c` | Heuristic simulated annealing program (not needed for verification) used to find the codes whose pairwise distances are at least a given value. |

Each file in `codes/` lists one permutation per line, as the sequence of its symbols from first to last. Lines starting with `#` are comments.

## Verification

```
python3 verify.py
python3 test_verify.py
```

For each certificate, the script checks the expected length n and size M, that every row is a permutation of 0, …, n−1, that the rows are distinct, and that all pairwise distances in the Kendall τ-metric equal the stated value (for the five equidistant codes, whose distance is m/(2m−1)·C(n,2) and whose splits are also checked) or are at least the stated value (for the other twelve codes). The expected parameters are listed in `CERTIFICATES` in `verify.py`. It then lists, for m = 2, 3, 4, 5, the lengths 3 ≤ n < 2Tₘ for which the range of distances in Corollary 9.3 contains an integer. It then lists the 20 permutations of length five at distance six from 01234, builds the graph in which two of them are adjacent when they are at distance six, and reports its degrees, its numbers of edges, triangles and cliques of size four, the seven cliques of size four, and its clique number, which is four. The script exits with a nonzero status if any check fails.

## Search programs

The search programs are heuristic. They are included to record how the codes were found and are not needed to check them: `verify.py` checks every code directly.

```
gcc -O2 -o sa search/sa.c -lm
./sa 8 8 1 200 1.5 0.5

gcc -O2 -o sa_atleast search/sa_atleast.c -lm
./sa_atleast 14 6 54 1 50 1.5 0.3
```

For `sa`, the arguments are the length n, the size M, a random seed, the number of iterations in millions, and the initial and final temperatures. It prints a code of size M and length n with all pairwise distances equal to ⌈M/2⌉·C(n,2)/(2⌈M/2⌉−1) and all splits as even as possible, when it finds one. For `sa_atleast`, the third argument is the required minimum distance D, and the program prints a code of size M and length n with all pairwise distances at least D, when it finds one.

## License

MIT. See `LICENSE`.
