# tools/parse_test_summary.py
import sys, re, os, json

PATH = sys.argv[1] if len(sys.argv) > 1 else "testcases_run_summary.md"
failed = 0
passed = 0

if not os.path.exists(PATH):
    print("FAIL:summary_missing")
    sys.exit(0)

with open(PATH, "r", encoding="utf-8") as f:
    txt = f.read()

m_fail = re.search(r"failed\s*[:=]\s*(\d+)", txt, re.I)
m_pass = re.search(r"passed\s*[:=]\s*(\d+)", txt, re.I)
failed = int(m_fail.group(1)) if m_fail else 0
passed = int(m_pass.group(1)) if m_pass else 0

print("PASS" if failed == 0 else f"FAIL:{failed}")
