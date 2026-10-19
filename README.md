# Optimal Permutation Codes Throughout the Plotkin Regime of the Kendall τ-Metric

Supplementary material for the paper

> Y. M. Chee, "Optimal permutation codes in the Plotkin regime of the Kendall τ-metric."

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
| `codes/n*_M10.txt` | Ten permutations of length n ∈ {14, 23, 26, 30, 33, 34, 35}, pairwise at distance at least 10⌊C(n,2)/18⌋. Used in the proof of Corollary 9.3(d). |
| `codes/n9_M9.txt` | Nine permutations of length nine, pairwise at distance 20 (concluding remarks). |
| `verify.py` | Verifies all codes, lists the small lengths treated in the proof of Corollary 9.3, and carries out the computation for permutation length five in the proof of Theorem 9.1(b). Python 3, standard library only. |
| `expected_output.txt` | Output of `verify.py`. |
| `search/sa.c` | Heuristic simulated annealing program (not needed for verification) used to find the codes of lengths 7 and 8, which attain the Plotkin bound with equal pairwise distances. |
| `search/sa_atleast.c` | Heuristic simulated annealing program (not needed for verification) used to find the codes whose pairwise distances are at least a given value. |

Each file in `codes/` lists one permutation per line, as the sequence of its symbols from first to last. Lines starting with `#` are comments.

## Verification

```
python3 verify.py
```

The script checks that every row of each code is a permutation of 0, …, n−1. For the codes that attain the Plotkin bound, it checks that all pairwise distances in the Kendall τ-metric equal the stated value and that every pair of symbols has the stated splits. For the codes used in Theorem 9.2 and Corollary 9.3, it checks that all pairwise distances are at least the stated value, and it checks that the nine permutations of length nine are pairwise at distance 20. It then checks that no relabelling of the symbols turns the code of length 16 into a code of insertion permutations, testing this check on the code in Example 4.7. It then lists, for m = 2, 3, 4, 5, the lengths 3 ≤ n < 2Tₘ for which the range of distances in Corollary 9.3 contains an integer. It then lists the 20 permutations of length five at distance six from 01234, builds the graph in which two of them are adjacent when they are at distance six, and reports its degrees, its numbers of edges, triangles and cliques of size four, the seven cliques of size four, and its clique number, which is four. The script exits with a nonzero status if any check fails.

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
