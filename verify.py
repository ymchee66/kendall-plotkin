"""Verification script for "Attaining the Plotkin Bound for Permutation Codes
in the Kendall tau-Metric" by Y. M. Chee.

Uses only the Python standard library.  Run from the repository root with

    python3 verify.py

1. For each code in codes/, checks that its rows are permutations of
   0, ..., n-1, that all pairwise distances in the Kendall tau-metric equal the value stated
   in the paper, and that every pair of symbols has the stated splits.
2. Carries out the computation in the proof of Theorem 7.1(b) for
   permutation length five.  It lists the 20 permutations at distance six from
   01234, builds the graph in which two of them are adjacent when they are at
   distance six, prints its degrees and numbers of edges and triangles, lists
   its cliques of size four, and computes its clique number.  Since the clique
   number is four, no code of six permutations of length five has minimum
   distance six.

The script exits with a nonzero status if any check fails.
"""
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import sys

CODES = Path(__file__).resolve().parent / "codes"

# file name: (pairwise distance, set of splits) as stated in the paper
EXPECTED = {
    "n16_M6.txt": (72, {3}),
    "n8_M8.txt": (16, {4}),
    "n7_M7.txt": (12, {3, 4}),
    "n5_M5.txt": (6, {2, 3}),
}


def kendall(p, q):
    """Number of pairs of symbols that p and q order differently."""
    pos = {v: i for i, v in enumerate(q)}
    r = [pos[v] for v in p]
    return sum(1 for i in range(len(r)) for j in range(i + 1, len(r)) if r[i] > r[j])


def splits(code):
    """Splits of the pairs {a, b}, a < b: the number of codewords placing a before b."""
    n = len(code[0])
    return {sum(1 for s in code if s.index(a) < s.index(b)) for a, b in combinations(range(n), 2)}


def read_code(path):
    rows = []
    for line in path.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            rows.append(tuple(int(x) for x in line.split()))
    return rows


def cliques(n_vertices, adjacent):
    """All cliques of a small graph, as tuples of vertex indices."""
    out = []

    def extend(clique, candidates):
        out.append(tuple(clique))
        for i, v in enumerate(candidates):
            extend(clique + [v], [w for w in candidates[i + 1:] if adjacent(v, w)])

    extend([], list(range(n_vertices)))
    return out


def word(p):
    return "".join(str(s) for s in p)


def check_codes():
    ok = True
    for name, (dist, spl) in EXPECTED.items():
        code = read_code(CODES / name)
        n = len(code[0])
        perms = all(sorted(s) == list(range(n)) for s in code)
        dists = {kendall(a, b) for a, b in combinations(code, 2)}
        sp = splits(code)
        good = perms and dists == {dist} and sp == spl
        ok &= good
        print(f"{name}: n={n}, size {len(code)}, pairwise distances {sorted(dists)}, "
              f"splits {sorted(sp)} -> {'OK' if good else 'FAIL'}")
    return ok


def check_n5():
    identity = tuple(range(5))
    V = sorted(p for p in permutations(range(5)) if kendall(p, identity) == 6)
    adj = lambda i, j: kendall(V[i], V[j]) == 6
    print(f"\nThe {len(V)} permutations of length five at distance 6 from 01234:")
    for i, p in enumerate(V):
        print(f"  v{i:02d} = {word(p)}")
    deg = [sum(1 for j in range(len(V)) if j != i and adj(i, j)) for i in range(len(V))]
    allc = cliques(len(V), adj)
    by_size = Counter(len(c) for c in allc)
    print(f"degrees (degree: number of vertices): {dict(sorted(Counter(deg).items(), reverse=True))}")
    print(f"edges: {by_size[2]}, triangles: {by_size[3]}, "
          f"cliques of size 4: {by_size[4]}, cliques of size 5: {by_size[5]}")
    print("cliques of size 4:")
    for c in allc:
        if len(c) == 4:
            print("  {" + ", ".join(word(V[i]) for i in c) + "}")
    omega = max(by_size)
    print(f"clique number: {omega}")
    return (len(V), by_size[2], by_size[3], by_size[4], omega) == (20, 60, 36, 7, 4)


def main():
    ok = check_codes()
    ok &= check_n5()
    print("\nAll checks passed." if ok else "\nSome checks FAILED.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
