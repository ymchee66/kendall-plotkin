"""Verification script for "Optimal Permutation Codes Throughout the Plotkin
Regime of the Kendall tau-Metric" by Y. M. Chee.

Uses only the Python standard library.  Run from the repository root with

    python3 verify.py

1. For each code in codes/, checks that its rows are permutations of
   0, ..., n-1.  For the codes attaining the Plotkin bound, it checks that
   all pairwise distances in the Kendall tau-metric equal the value stated in
   the paper and that every pair of symbols has the stated splits.  For the
   codes used in Theorem 9.2 and Corollary 9.3, it checks that all pairwise
   distances are at least the stated value.  It also checks that the nine
   permutations of length nine in the concluding remarks are pairwise at
   distance 20.
2. Checks that no relabelling of the symbols turns the code of length 16 into
   a code of insertion permutations, and, as a test of this check, that the
   code in Example 4.7 is a code of insertion permutations.
3. Lists the lengths n < 2T_m for which the range of distances in
   Corollary 9.3 is nonempty.
4. Carries out the computation in the proof of Theorem 9.1(b) for
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

# Codes attaining the Plotkin bound: file name -> (pairwise distance, set of splits).
EXPECTED = {
    "n16_M6.txt": (72, {3}),
    "n8_M8.txt": (16, {4}),
    "n7_M7.txt": (12, {3, 4}),
    "n5_M5.txt": (6, {2, 3}),
}

# Nine permutations of length nine, pairwise at distance 20 (concluding remarks).
NINE = ("n9_M9.txt", 20)

# Codes for Theorem 9.2 and Corollary 9.3: file name -> lower bound on the pairwise distances.
AT_LEAST = {
    "n14_M6.txt": 54,
    "n17_M6.txt": 78,
    "n18_M6.txt": 90,
    "n19_M6.txt": 102,
    "n13_M8.txt": 44,
    "n14_M10.txt": 50,
    "n23_M10.txt": 140,
    "n26_M10.txt": 180,
    "n30_M10.txt": 240,
    "n33_M10.txt": 290,
    "n34_M10.txt": 310,
    "n35_M10.txt": 330,
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
    for name, low in AT_LEAST.items():
        code = read_code(CODES / name)
        n = len(code[0])
        perms = all(sorted(s) == list(range(n)) for s in code) and len(set(code)) == len(code)
        dists = {kendall(a, b) for a, b in combinations(code, 2)}
        good = perms and min(dists) >= low
        ok &= good
        print(f"{name}: n={n}, size {len(code)}, pairwise distances {sorted(dists)}, "
              f"required at least {low} -> {'OK' if good else 'FAIL'}")
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


def check_nine():
    name, dist = NINE
    code = read_code(CODES / name)
    perms = all(sorted(s) == list(range(9)) for s in code) and len(set(code)) == 9
    dists = {kendall(a, b) for a, b in combinations(code, 2)}
    good = perms and dists == {dist}
    print(f"{name}: n=9, size {len(code)}, pairwise distances {sorted(dists)} -> {'OK' if good else 'FAIL'}")
    return good


def insertion_relabelling_exists(code):
    """Whether some relabelling of the symbols turns every codeword into an
    insertion permutation.  The symbol relabelled 0 must be first or last in
    every codeword, and, after deleting it, the same holds recursively."""
    n = len(code[0])
    seen = {}

    def rec(rem):
        if len(rem) <= 1:
            return True
        if rem not in seen:
            cands = []
            for a in rem:
                ok = True
                for s in code:
                    t = [x for x in s if x in rem]
                    if a != t[0] and a != t[-1]:
                        ok = False
                        break
                if ok:
                    cands.append(a)
            seen[rem] = any(rec(rem - {a}) for a in cands)
        return seen[rem]

    return rec(frozenset(range(n)))


def check_not_insertion():
    example = [tuple(int(c) for c in w) for w in ("012345", "054321", "145320", "235410")]
    code = read_code(CODES / "n16_M6.txt")
    a = insertion_relabelling_exists(example)
    b = insertion_relabelling_exists(code)
    print(f"\nExample 4.7 code is a code of insertion permutations: {a}")
    print(f"n16_M6.txt can be relabelled into a code of insertion permutations: {b}")
    return a and not b


def check_small_lengths():
    """Lengths 3 <= n < 2*T_m for which the m-th window contains an integer d
    with d <= m/(2m-1) * T_m * floor(N/T_m), as in the proof of Corollary 9.3."""
    from fractions import Fraction
    expected = {2: [3, 4], 3: [5, 14, 16, 17, 18, 19], 4: [7, 8, 13],
                5: [9, 14, 23, 26, 28, 30, 33, 34, 35]}
    ok = True
    print("\nLengths n < 2T_m in the proof of Corollary 9.3:")
    for m, T in ((2, 3), (3, 10), (4, 7), (5, 18)):
        found = []
        for n in range(3, 2 * T):
            N = n * (n - 1) // 2
            L = Fraction(m, 2 * m - 1) * T * (N // T)
            lower = Fraction(m + 1, 2 * m + 1) * N
            if any(lower < d <= L for d in range(N + 1)):
                found.append(n)
        good = found == expected[m]
        ok &= good
        print(f"  m={m}: {found} -> {'OK' if good else 'FAIL'}")
    return ok


def main():
    ok = check_codes()
    ok &= check_nine()
    ok &= check_not_insertion()
    ok &= check_small_lengths()
    ok &= check_n5()
    print("\nAll checks passed." if ok else "\nSome checks FAILED.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
