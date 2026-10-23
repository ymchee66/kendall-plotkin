"""Negative tests for verify.py.

Each test copies codes/ to a temporary directory, damages one certificate or one
expected parameter, and checks that verify.py reports a failure.  Run from the
repository root with

    python3 test_verify.py
"""

import contextlib
import io
import shutil
import tempfile
from pathlib import Path

import verify

ROOT = Path(__file__).resolve().parent


def rows(path):
    lines = path.read_text().splitlines()
    return lines, [i for i, line in enumerate(lines) if line.split("#", 1)[0].strip()]


def remove_codeword(path):
    lines, idx = rows(path)
    del lines[idx[-1]]
    path.write_text("\n".join(lines) + "\n")


def duplicate_codeword(path):
    lines, idx = rows(path)
    lines[idx[1]] = lines[idx[0]]
    path.write_text("\n".join(lines) + "\n")


def lengthen_codeword(path):
    lines, idx = rows(path)
    n = len(lines[idx[0]].split())
    lines[idx[0]] = lines[idx[0]] + f" {n}"
    path.write_text("\n".join(lines) + "\n")


def run(codes_dir, certificates=None):
    saved = dict(verify.CERTIFICATES)
    if certificates is not None:
        verify.CERTIFICATES.clear()
        verify.CERTIFICATES.update(certificates)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return verify.check_codes(codes_dir)
    finally:
        verify.CERTIFICATES.clear()
        verify.CERTIFICATES.update(saved)


def main():
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / "codes"
        shutil.copytree(ROOT / "codes", base)
        results.append(("unchanged certificates pass", run(base) is True))
        for name in verify.CERTIFICATES:
            for damage in (remove_codeword, duplicate_codeword, lengthen_codeword):
                d = Path(tmp) / f"{name}_{damage.__name__}"
                shutil.copytree(ROOT / "codes", d)
                damage(d / name)
                results.append((f"{damage.__name__} in {name} fails", run(d) is False))
            n, M, kind, dist, spl = verify.CERTIFICATES[name]
            for label, changed in (("length", (n + 1, M, kind, dist, spl)),
                                   ("size", (n, M + 1, kind, dist, spl)),
                                   ("distance", (n, M, kind, dist + 1, spl))):
                certs = dict(verify.CERTIFICATES)
                certs[name] = changed
                results.append((f"wrong expected {label} for {name} fails", run(base, certs) is False))
    bad = [label for label, good in results if not good]
    print(f"{len(results) - len(bad)} of {len(results)} negative tests behave as expected.")
    for label in bad:
        print(f"  UNEXPECTED: {label}")
    raise SystemExit(1 if bad else 0)


if __name__ == "__main__":
    main()
