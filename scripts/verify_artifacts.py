import os
import zlib
import base64
import re
from pptx import Presentation

pptx_path = r"C:\Users\Nisha\.gemini\antigravity\scratch\predictive-customer-churn-telecom\deliverables\ConnectTel_Executive_Presentation.pptx"
pdf_path = r"C:\Users\Nisha\.gemini\antigravity\scratch\predictive-customer-churn-telecom\deliverables\ConnectTel_Technical_Project_Report.pdf"

print("=" * 60)
print("DELIVERABLES VERIFICATION AUDIT")
print("=" * 60)

# 1. Check PPTX
print(f"\n1. PPTX Deliverable: {os.path.basename(pptx_path)}")
print(f"   Exists: {os.path.exists(pptx_path)}")
print(f"   Size: {os.path.getsize(pptx_path):,} bytes")
prs = Presentation(pptx_path)
print(f"   Total Slides: {len(prs.slides)}")
for idx, slide in enumerate(prs.slides):
    shapes = list(slide.shapes)
    has_img = any(s.shape_type == 13 for s in shapes)
    texts = [s.text_frame.text.strip().replace('\n', ' ') for s in shapes if s.has_text_frame and s.text_frame.text.strip()]
    title = texts[0][:50] if texts else "Untitled"
    print(f"   Slide {idx+1:02d}: {title:<50} | Shapes: {len(shapes):2d} | Image: {has_img}")

# 2. Check PDF
print(f"\n2. PDF Deliverable: {os.path.basename(pdf_path)}")
print(f"   Exists: {os.path.exists(pdf_path)}")
print(f"   Size: {os.path.getsize(pdf_path):,} bytes")

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

# Extract ASCII85 and Flate streams
stream_chunks = re.findall(rb'stream\r?\n(.*?)\~>endstream', pdf_bytes, re.DOTALL)
print(f"   ASCII85 Streams Located: {len(stream_chunks)}")

decoded_texts = []
for chunk in stream_chunks:
    try:
        cleaned = chunk.strip()
        payload = b'<~' + cleaned + b'~>'
        raw = base64.a85decode(payload, adobe=True)
        try:
            decomp = zlib.decompress(raw)
            decoded_texts.append(decomp)
        except Exception:
            decoded_texts.append(raw)
    except Exception as e:
        pass

print(f"   Successfully Decoded Streams: {len(decoded_texts)}")
all_text = b"\n".join(decoded_texts).decode("latin1", errors="ignore")
print(f"   Total Decoded Content Size: {len(all_text):,} characters")

# Find page markers (e.g. Page X of Y or page break markers)
page_markers = set(re.findall(r'Page\s+(\d+)\s+of\s+(\d+)', all_text))
print(f"   Page Markers found in running footer: {sorted(list(page_markers))}")

# 3. Check required keywords and values
required_terms = [
    "ConnectTel",
    "Persevex AI Internship",
    "320 synthetic",
    "Logistic Regression",
    "0.55",
    "0.7697",
    "0.7679",
    "0.095473",
    "0.209454",
    "Brier",
    "SHAP",
    "Electric Orange",
    "High-Risk Delinquent",
    "Loyal Subscriber",
    "A/B testing",
    "uncalibrated"
]

print("\n3. Keyword & Fact Audit in PDF:")
all_pass = True
for term in required_terms:
    found = term in all_text
    status = "PASS" if found else "FAIL"
    if not found:
        all_pass = False
    print(f"   [{status}] {term}")

print(f"\nAudit Result: {'ALL CHECKS PASSED' if all_pass else 'SOME CHECKS FAILED'}")

