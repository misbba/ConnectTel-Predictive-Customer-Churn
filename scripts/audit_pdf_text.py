import os
import re

pdf_script = r"C:\Users\Nisha\.gemini\antigravity\scratch\predictive-customer-churn-telecom\scripts\build_pdf_report.py"

with open(pdf_script, "r", encoding="utf-8") as f:
    code = f.read()

print("=" * 70)
print("AUDITING BUILD_PDF_REPORT.PY")
print("=" * 70)

# Extract sections / Story calls
# Let's inspect sections 1 to 16
sections = re.findall(r'story\.append\(Paragraph\(\"(\d+\..*?)\", style_h1\)\)', code)
print(f"Sections defined in script: {len(sections)}")
for s in sections:
    print(f"  {s}")

# Check tables defined
tables = re.findall(r'(\w+_data)\s*=\s*\[(.*?)\]\n\s*t_', code, re.DOTALL)
print(f"\nTables defined: {len(tables)}")
for tname, tcontent in tables:
    print(f"\n--- TABLE: {tname} ---")
    print(tcontent[:600])

# Search for specific strings in the script
search_terms = [
    "XGBoost", "Random Forest", "PR-AUC", "0.3800", "0.3831", "0.319", "0.341",
    "0.4497", "0.3621", "0.176", "1.56", "fiber", "Fiber", "18,480", "18480",
    "CAC", "$300", "$450", "0.55", "calibrated", "Customer #", "Customer #38",
    "Customer #C225", "Customer #C193"
]

print("\n--- SEARCH TERM HITS IN BUILD_PDF_REPORT.PY ---")
lines = code.split("\n")
for line_no, line in enumerate(lines, 1):
    for term in search_terms:
        if term in line:
            print(f"Line {line_no:4d} [{term}]: {line.strip()[:140]}")
