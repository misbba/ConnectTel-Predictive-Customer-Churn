"""
Build Executive PowerPoint Presentation for ConnectTel Customer Churn Model.
ConnectTel / Persevex AI Internship Project - Phase 7.3.3 Visual Redesign.

Official Design System:
- Theme: Midnight Black × Electric Orange
- Palette:
  * Canvas Background: #0e0e11 (Midnight Black)
  * Primary Accent: #ff7a00 (Electric Orange)
  * Secondary Accent: #f26419 (Deep Orange)
  * Primary Card Fill: #18120f (Dark Chocolate)
  * Secondary Card Fill: #221813 (Deep Brown)
  * Highlight Card Fill: #2a1b14 (Radiant Warm Chocolate)
  * Text Primary: #e5e5e8 (Soft White)
  * Text Secondary: #a7a7b0 (Cool Grey)
  * Text Muted: #6c6c78 (Subtle Metadata)
  * Border Subtle: #38261c (Subtle Dark Brown)
  * Border Accent / Glow: #ff7a00 (Electric Orange)
  * Border Green: #2ed573 (Retained Status)
"""

import sys
import os
from pathlib import Path
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES_DIR = ROOT / "deliverables"
FIGURES_DIR = ROOT / "outputs" / "figures"
EDA_DIR = ROOT / "outputs" / "eda_figures"
EVAL_DIR = ROOT / "outputs" / "model_eval_figures"
SHAP_DIR = ROOT / "outputs" / "shap"
SCREENSHOTS_DIR = ROOT / "outputs" / "app_screenshots"

# Ensure directories exist
DELIVERABLES_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Design Colors
C_BG = RGBColor(14, 14, 17)            # #0e0e11
C_ORANGE = RGBColor(255, 122, 0)        # #ff7a00
C_DEEP_ORANGE = RGBColor(242, 100, 25)  # #f26419
C_CARD = RGBColor(24, 18, 15)           # #18120f
C_CARD_DEEP = RGBColor(34, 24, 19)      # #221813
C_CARD_GLOW = RGBColor(42, 27, 20)      # #2a1b14
C_WHITE = RGBColor(229, 229, 232)       # #e5e5e8
C_GREY = RGBColor(167, 167, 176)        # #a7a7b0
C_MUTED = RGBColor(108, 108, 120)       # #6c6c78
C_BORDER = RGBColor(56, 38, 28)         # #38261c
C_BORDER_GLOW = RGBColor(255, 122, 0)   # #ff7a00
C_GREEN = RGBColor(46, 213, 115)        # #2ed573

FONT_TITLE = "Georgia"
FONT_SANS = "Segoe UI"
FONT_BODY = "Segoe UI"


def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def set_solid_background(slide, color=C_BG):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_header(slide, title_text, category_tag="CONNECTTEL TELECOM RETENTION ML", tracker_tag=None):
    """
    Standardized, elegant editorial header bar for content slides.
    """
    # Top metadata line: Category Tag (left) and Tracker Tag (right)
    top_meta = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.733), Inches(0.35))
    tf_meta = top_meta.text_frame
    tf_meta.word_wrap = True
    tf_meta.margin_left = tf_meta.margin_right = tf_meta.margin_top = tf_meta.margin_bottom = 0

    p_meta = tf_meta.paragraphs[0]
    p_meta.text = category_tag.upper()
    p_meta.font.name = FONT_SANS
    p_meta.font.size = Pt(8.5)
    p_meta.font.bold = True
    p_meta.font.color.rgb = C_ORANGE

    if tracker_tag:
        r_pipe = p_meta.add_run()
        r_pipe.text = "   |   "
        r_pipe.font.color.rgb = C_BORDER
        r_tr = p_meta.add_run()
        r_tr.text = tracker_tag.upper()
        r_tr.font.bold = True
        r_tr.font.color.rgb = C_GREY

    # Title Box
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.733), Inches(0.65))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0

    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = FONT_TITLE
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = C_WHITE

    # Subtle divider rule across slide
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.42), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = C_CARD_DEEP
    line.line.color.rgb = C_CARD_DEEP


def add_rounded_card(slide, left, top, width, height, fill_color=C_CARD, border_color=C_BORDER, corner_radius=0.06, line_width=1.0):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = fill_color
    card.line.color.rgb = border_color
    card.line.width = Pt(line_width)
    try:
        card.adjustments[0] = corner_radius
    except Exception:
        pass
    return card


def add_hero_metric_card(slide, left, top, width, height, stat_value, stat_label, stat_desc=None, highlight=False):
    """
    Creates a hero metric card inspired by Reference Slide 2 and Slide 7.
    """
    fill_col = C_CARD_GLOW if highlight else C_CARD
    border_col = C_BORDER_GLOW if highlight else C_BORDER
    line_w = 1.5 if highlight else 1.0

    card = add_rounded_card(slide, left, top, width, height, fill_color=fill_col, border_color=border_col, corner_radius=0.08, line_width=line_w)

    tb = slide.shapes.add_textbox(left + Inches(0.22), top + Inches(0.18), width - Inches(0.44), height - Inches(0.36))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    # Big Number
    p_num = tf.paragraphs[0]
    p_num.text = str(stat_value)
    p_num.font.name = FONT_SANS
    p_num.font.size = Pt(32)
    p_num.font.bold = True
    p_num.font.color.rgb = C_ORANGE if highlight else C_WHITE

    # Label / Title
    p_lbl = tf.add_paragraph()
    p_lbl.text = stat_label
    p_lbl.font.name = FONT_SANS
    p_lbl.font.size = Pt(10)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = C_WHITE if highlight else C_GREY
    p_lbl.space_before = Pt(4)

    # Optional detailed description
    if stat_desc:
        p_desc = tf.add_paragraph()
        p_desc.text = stat_desc
        p_desc.font.name = FONT_BODY
        p_desc.font.size = Pt(8.5)
        p_desc.font.color.rgb = C_GREY if highlight else C_MUTED
        p_desc.space_before = Pt(4)

    return card


def add_framed_image(slide, left, top, width, height, img_path, title=None, badge=None, highlight=False):
    """
    Renders an image inside an elegant dark frame with subtle border and optional title pill.
    """
    border_col = C_BORDER_GLOW if highlight else C_BORDER
    line_w = 1.5 if highlight else 1.0
    bg_card = add_rounded_card(slide, left, top, width, height, fill_color=C_CARD, border_color=border_col, corner_radius=0.04, line_width=line_w)

    pad_x = Inches(0.15)
    pad_top = Inches(0.45) if (title or badge) else Inches(0.15)
    pad_bot = Inches(0.15)

    if title or badge:
        tb = slide.shapes.add_textbox(left + pad_x, top + Inches(0.12), width - pad_x * 2, Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        if badge:
            r_b = p.add_run()
            r_b.text = f"[{badge}] "
            r_b.font.name = FONT_SANS
            r_b.font.size = Pt(8.5)
            r_b.font.bold = True
            r_b.font.color.rgb = C_ORANGE
        if title:
            r_t = p.add_run()
            r_t.text = title
            r_t.font.name = FONT_SANS
            r_t.font.size = Pt(9.5)
            r_t.font.bold = True
            r_t.font.color.rgb = C_WHITE

    # Add the image
    img_left = left + pad_x
    img_top = top + pad_top
    img_w = width - pad_x * 2
    img_h = height - pad_top - pad_bot

    if Path(img_path).exists():
        slide.shapes.add_picture(str(img_path), img_left, img_top, width=img_w, height=img_h)

    return bg_card


print("Loaded presentation design core framework successfully.")
