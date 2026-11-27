import re

with open(r"C:\Users\Nisha\.gemini\antigravity\scratch\predictive-customer-churn-telecom\scripts\build_pdf_report.py", "r", encoding="utf-8") as f:
    text = f.read()

# Let's see all sections and paragraphs in build_pdf_report.py
sections = re.split(r'story\.append\(Paragraph\(\"(\d+\..*?)\", style_h1\)\)', text)

print("=" * 70)
print("AUDITING BUILD_PDF_REPORT.PY SECTIONS")
print("=" * 70)

# Section 0 is preamble/cover
print("--- PREAMBLE & COVER ---")
print(sections[0][:800])

for i in range(1, len(sections), 2):
    sec_title = sections[i]
    sec_body = sections[i+1]
    print(f"\n--- SECTION {sec_title} ---")
    # Extract plain text from paragraphs in sec_body
    paras = re.findall(r'Paragraph\(\s*\"(.*?)\"', sec_body, re.DOTALL)
    for p in paras[:8]: # print first 8 paragraphs
        clean_p = p.replace('\n', ' ').strip()
        print(f"  * {clean_p[:120]}")
    # Also look for tables in sec_body
    t_matches = re.findall(r'(\w+_data)\s*=\s*\[(.*?)\]\n\s*t_', sec_body, re.DOTALL)
    for tname, tcontent in t_matches:
        print(f"  [TABLE {tname}]:")
        for row in re.findall(r'\[(.*?)\]', tcontent):
            row_items = re.findall(r'Paragraph\(\"([^\"]+)\"', row)
            if row_items:
                print(f"    - {' | '.join(row_items)}")
