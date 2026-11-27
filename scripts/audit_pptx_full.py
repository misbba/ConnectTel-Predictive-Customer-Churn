from pptx import Presentation
import os

prs = Presentation(r"C:\Users\Nisha\.gemini\antigravity\scratch\predictive-customer-churn-telecom\deliverables\ConnectTel_Executive_Presentation.pptx")

print("=" * 70)
print("LINE-BY-LINE AUDIT OF PPTX SLIDES")
print("=" * 70)

for idx, slide in enumerate(prs.slides):
    slide_num = idx + 1
    texts = []
    for shape in slide.shapes:
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                t = p.text.strip()
                if t:
                    texts.append(t)
    slide_text = " \n ".join(texts)
    print(f"\n--- SLIDE {slide_num:02d} ---")
    for t in texts:
        print(f"  * {t[:120]}")
