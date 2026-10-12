# Attaining the Plotkin Bound for Permutation Codes in the Kendall τ-Metric

Supplementary material for the paper

> Y. M. Chee, "Attaining the Plotkin bound for permutation codes in the Kendall τ-metric."

## Contents

| Path | Description |
|---|---|
| `codes/n16_M6.txt` | Six permutations of length 16, pairwise at distance 72, every pair of symbols of split three. Used in the proof of Theorem 7.1(b). |
| `codes/n8_M8.txt` | The code in Table I (Theorem 7.1(c)). |
| `codes/n7_M7.txt` | The code in Table II (Theorem 7.1(c)). |
| `codes/n5_M5.txt` | The code in Table III (Theorem 7.1(b)). |
| `verify.py` | Verifies all codes and carries out the computation for permutation length five in the proof of Theorem 7.1(b). Python 3, standard library only. |
| `expected_output.txt` | Output of `verify.py`. |
| `search/sa.c` | Simulated annealing program used to find the codes of lengths seven and eight. |

Each file in `codes/` lists one permutation per line, as the sequence of its symbols from first to last. Lines starting with `#` are comments.

## Verification

```
python3 verify.py
```

The script checks that every row of each code is a permutation of 0, …, n−1, that all pairwise distances in the Kendall τ-metric equal the stated value, and that every pair of symbols has the stated splits. It then lists the 20 permutations of length five at distance six from 01234, builds the graph in which two of them are adjacent when they are at distance six, and reports its degrees, its numbers of edges, triangles and cliques of size four, the seven cliques of size four, and its clique number, which is four. The script exits with a nonzero status if any check fails.

## Search program

```
gcc -O2 -o sa search/sa.c -lm
./sa 8 8 1 200 1.5 0.5
```

The arguments are the length n, the size M, a random seed, the number of iterations in millions, and the initial and final temperatures. The program prints a code of size M and length n with all pairwise distances equal to ⌈M/2⌉·C(n,2)/(2⌈M/2⌉−1) and all splits as even as possible, when it finds one.

## License

MIT. See `LICENSE`.
