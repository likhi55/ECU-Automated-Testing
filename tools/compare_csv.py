#!/usr/bin/env python3
"""
Compare two CSV files (out vs golden) by column names and row order.

Usage:
  python tools/compare_csv.py --out path/to/out.csv --golden path/to/golden.csv \
      [--rtol 0.0] [--atol 0.0] [--ignore-cols col1,col2]

- rtol/atol apply to numeric columns (float/int). Strings must match exactly.
- Columns must match by name; out may contain extra columns (ignored unless not listed in ignore-cols).
- Exit code 0 if equal within tolerances; 1 otherwise. Prints a short summary.
"""
import argparse, csv, math, sys

def is_number(x):
    try:
        float(x)
        return True
    except:
        return False

def almost_equal(a, b, rtol, atol):
    try:
        af, bf = float(a), float(b)
        return math.isclose(af, bf, rel_tol=rtol, abs_tol=atol)
    except:
        return a == b

def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        headers = reader.fieldnames or []
    return headers, rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--golden", required=True)
    ap.add_argument("--rtol", type=float, default=0.0)
    ap.add_argument("--atol", type=float, default=0.0)
    ap.add_argument("--ignore-cols", default="")
    args = ap.parse_args()

    ign = set([c.strip() for c in args.ignore_cols.split(",") if c.strip()])

    h_out, rows_out = read_csv(args.out)
    h_gld, rows_gld = read_csv(args.golden)

    # Required columns = golden minus ignored
    req_cols = [c for c in h_gld if c not in ign]

    # Quick header check
    missing = [c for c in req_cols if c not in h_out]
    if missing:
        print(f"FAIL: missing columns in out: {missing}")
        sys.exit(1)

    if len(rows_out) != len(rows_gld):
        print(f"FAIL: row count mismatch: out={len(rows_out)} golden={len(rows_gld)}")
        sys.exit(1)

    errors = []
    for i, (ro, rg) in enumerate(zip(rows_out, rows_gld)):
        for col in req_cols:
            vo = ro.get(col, "")
            vg = rg.get(col, "")
            if is_number(vg) and is_number(vo):
                if not almost_equal(vo, vg, args.rtol, args.atol):
                    errors.append(f"row {i} col '{col}': out={vo} golden={vg}")
            else:
                if vo != vg:
                    errors.append(f"row {i} col '{col}': out={vo} golden={vg}")

    if errors:
        print("FAIL")
        for e in errors[:20]:
            print("  " + e)
        if len(errors) > 20:
            print(f"  ... and {len(errors)-20} more")
        sys.exit(1)
    else:
        print("PASS")
        sys.exit(0)

if __name__ == "__main__":
    main()
