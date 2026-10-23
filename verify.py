"""Verification script for "Eventual Attainment of the Plotkin Bound for Kendall
tau Permutation Codes in Every Fixed Window" by Y. M. Chee.

Uses only the Python standard library.  Run from the repository root with

    python3 verify.py

1. For each of the 17 certificates in codes/, checks the expected length n
   and size M, that every codeword is a permutation of 0, ..., n-1, that the
   codewords are distinct, and that all pairwise distances in the Kendall
   tau-metric equal (for the five equidistant codes) or are at least (for
   the other twelve codes) the value stated in the paper.  For the five
   equidistant codes, whose distance is m/(2m-1) * C(n,2), it also checks
   the splits of all pairs of symbols.  The expected parameters are listed in CERTIFICATES.  An optional
   argument names a different directory of certificates.
2. Lists the lengths n < 2T_m for which the range of distances in
   Corollary 9.3 is nonempty.
3. Carries out the computation in the proof of Theorem 9.1(b) for
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

# Every certificate used in the paper: file name -> (length n, size M, kind, distance, splits).
# kind "equal": all pairwise distances equal the given distance.
# kind "atleast": all pairwise distances are at least the given distance.
# splits: the set of values that the split of every pair of symbols must take, or None
# when no split condition is claimed.  For codes of size 2m-1 or 2m with minimum distance
# m/(2m-1) * C(n,2), Lemma 2.4 of the paper forces splits m-1 or m, or m, respectively.
CERTIFICATES = {
    "n16_M6.txt": (16, 6, "equal", 72, {3}),
    "n8_M8.txt": (8, 8, "equal", 16, {4}),
    "n7_M7.txt": (7, 7, "equal", 12, {3, 4}),
    "n5_M5.txt": (5, 5, "equal", 6, {2, 3}),
    "n9_M9.txt": (9, 9, "equal", 20, {4, 5}),
    "n14_M6.txt": (14, 6, "atleast", 54, None),
    "n17_M6.txt": (17, 6, "atleast", 78, None),
    "n18_M6.txt": (18, 6, "atleast", 90, None),
    "n19_M6.txt": (19, 6, "atleast", 102, None),
    "n13_M8.txt": (13, 8, "atleast", 44, None),
    "n14_M10.txt": (14, 10, "atleast", 50, None),
    "n23_M10.txt": (23, 10, "atleast", 140, None),
    "n26_M10.txt": (26, 10, "atleast", 180, None),
    "n30_M10.txt": (30, 10, "atleast", 240, None),
    "n33_M10.txt": (33, 10, "atleast", 290, None),
    "n34_M10.txt": (34, 10, "atleast", 310, None),
    "n35_M10.txt": (35, 10, "atleast", 330, None),
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


def check_certificate(path, n, M, kind, dist, spl):
    """Check one certificate against its expected parameters.  Returns (ok, report)."""
    problems = []
    try:
        code = read_code(path)
    except (OSError, ValueError) as exc:
        return False, f"cannot read: {exc}"
    if len(code) != M:
        problems.append(f"has {len(code)} codewords, expected {M}")
    if any(len(s) != n for s in code):
        problems.append(f"a codeword does not have length {n}")
    if not all(sorted(s) == list(range(n)) for s in code):
        problems.append(f"a codeword is not a permutation of 0..{n - 1}")
    if len(set(code)) != len(code):
        problems.append("codewords are not distinct")
    if problems:
        return False, "; ".join(problems)
    dists = {kendall(a, b) for a, b in combinations(code, 2)}
    if kind == "equal" and dists != {dist}:
        problems.append(f"pairwise distances {sorted(dists)}, expected all equal to {dist}")
    if kind == "atleast" and min(dists) < dist:
        problems.append(f"minimum distance {min(dists)}, expected at least {dist}")
    report = f"n={n}, M={M}, pairwise distances {sorted(dists)}"
    if spl is not None:
        sp = splits(code)
        report += f", splits {sorted(sp)}"
        if sp != spl:
            problems.append(f"splits {sorted(sp)}, expected {sorted(spl)}")
    return not problems, report + ("" if not problems else " -- " + "; ".join(problems))


def check_codes(codes_dir=None):
    codes_dir = Path(codes_dir) if codes_dir else CODES
    ok = True
    for name, (n, M, kind, dist, spl) in CERTIFICATES.items():
        good, report = check_certificate(codes_dir / name, n, M, kind, dist, spl)
        ok &= good
        need = f"all distances {dist}" if kind == "equal" else f"distances at least {dist}"
        print(f"{name}: {report}; required {need} -> {'OK' if good else 'FAIL'}")
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
    ok = check_codes(sys.argv[1] if len(sys.argv) > 1 else None)
    ok &= check_small_lengths()
    ok &= check_n5()
    print("\nAll checks passed." if ok else "\nSome checks FAILED.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
