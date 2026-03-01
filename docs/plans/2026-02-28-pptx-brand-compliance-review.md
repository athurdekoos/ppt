# PPTX Brand Compliance Review Plan

**Status:** ✅ Completed (2026-02-28)

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Generate a mock OpenTeams presentation, export each slide as an image, and audit every slide against the OpenTeams 2025 Brand Guidelines — documenting pass/fail for colors, typography, logo placement, spacing, and visual cues.

**Architecture:** Use the `openteams-pptx` skill to generate a demo deck covering all 10 slide types. Convert each slide to an image using `libreoffice`. Then systematically inspect each image and the underlying PPTX XML against the brand standard, producing a compliance report.

**Tech Stack:** Python 3, python-pptx, LibreOffice (headless PDF/PNG export), OpenTeams brand.json

---

## Checklist: Brand Compliance Criteria

These are the non-negotiable rules from the 2025 Brand Guidelines and `brand.json`:

| ID | Rule | Source |
|----|------|--------|
| C1 | Primary colors are Night Navy `#022791` and Day Blue `#4D75FE` only | Brand Guidelines |
| C2 | Salmon `#FF8A69` and Yellow `#FAA944` used as accents only, never dominant | Brand Guidelines |
| C3 | White-dominant backgrounds for most slides; dark (Night Navy) only for section dividers, quotes, closing | Brand Guidelines |
| C4 | Gradients: Night Navy → Day Blue, used on cover and closing only | Brand Guidelines |
| C5 | Headlines use Inter Tight Bold | Brand Guidelines |
| C6 | Body text uses Inter Tight Regular | Brand Guidelines |
| C7 | Utility text (footers, captions) uses Roboto | Brand Guidelines |
| C8 | No unauthorized fonts | Brand Guidelines |
| C9 | Logo placed upper-left or lower-left/center only — never right-aligned | Brand Guidelines |
| C10 | Colored logo on light backgrounds, white logo on dark backgrounds | Brand Guidelines |
| C11 | Logo not altered, distorted, or given effects | Brand Guidelines |
| C12 | Minimum clearspace respected (width of "O") | Brand Guidelines |
| C13 | Cards: shadow-based elevation, no visible borders, 12pt corner radius | Website Cues |
| C14 | Buttons: pill-shaped, Day Blue fill, white text | Website Cues |
| C15 | Generous whitespace: 0.6" margins, 0.35" gutters | brand.json |
| C16 | Decorative accent dots at 15–30% opacity (where used) | Website Cues |
| C17 | Image placeholders: rounded corners, light blue `#E8EDFB` fill | Website Cues |
| C18 | Slide dimensions: 13.333" × 7.5" (16:9) | brand.json |

---

### Task 1: Generate the Demo Deck

**Files:**
- Create: `/home/mia/dev/ppt/review/mock_demo.pptx`

**Step 1: Create output directory**

```bash
mkdir -p /home/mia/dev/ppt/review
```

**Step 2: Generate the demo deck using the openteams-pptx skill script**

Run:
```bash
/home/mia/.venvs/pptx/bin/python /home/mia/.pi/agent/skills/openteams-pptx/scripts/generate_deck.py \
  --demo \
  --brand /home/mia/.pi/agent/skills/openteams-pptx/references/brand.json \
  --out /home/mia/dev/ppt/review/mock_demo.pptx
```

Expected: `Generated 10 slides → /home/mia/dev/ppt/review/mock_demo.pptx`

---

### Task 2: Export Slides as Images

**Files:**
- Create: `/home/mia/dev/ppt/review/slides/` (directory of PNG images)

**Step 1: Convert PPTX to PDF via LibreOffice**

Run:
```bash
libreoffice --headless --convert-to pdf --outdir /home/mia/dev/ppt/review /home/mia/dev/ppt/review/mock_demo.pptx
```

**Step 2: Convert PDF pages to individual PNGs**

Run:
```bash
mkdir -p /home/mia/dev/ppt/review/slides
# Use pdftoppm (poppler-utils) or ImageMagick convert
pdftoppm -png -r 200 /home/mia/dev/ppt/review/mock_demo.pdf /home/mia/dev/ppt/review/slides/slide
```

Expected: 10 PNG files in `/home/mia/dev/ppt/review/slides/`

---

### Task 3: Inspect PPTX Internals for Color Compliance (C1–C4)

**Step 1: Write a Python audit script**

Create `/home/mia/dev/ppt/review/audit_brand.py` — this script opens the .pptx and inspects every shape's fill/font colors, checking them against the allowed palette.

```python
#!/usr/bin/env python3
"""Audit a .pptx file against OpenTeams brand color rules."""
import sys
from pptx import Presentation
from pptx.util import Pt, Inches, Emu
from pptx.dml.color import RGBColor

ALLOWED_COLORS = {
    "022791", "4D75FE", "FF8A69", "FAA944",
    "0C0C0C", "262626", "3F3F3F", "FFFFFF",
    "F7F8FC", "E8EDFB", "3AD58E",
    "000000",  # python-pptx default black
}

ACCENT_ONLY = {"FF8A69", "FAA944"}

DARK_BG_TYPES = {"section_divider", "quote", "closing"}

def hex_of(rgb):
    if rgb is None:
        return None
    return f"{rgb.red:02X}{rgb.green:02X}{rgb.blue:02X}" if hasattr(rgb, 'red') else str(rgb)

def audit(path):
    prs = Presentation(path)
    issues = []

    # C18: Slide dimensions
    w = prs.slide_width / 914400  # EMU to inches
    h = prs.slide_height / 914400
    if abs(w - 13.333) > 0.01 or abs(h - 7.5) > 0.01:
        issues.append(f"C18 FAIL: Slide size {w:.3f}x{h:.3f} != 13.333x7.5")
    else:
        issues.append(f"C18 PASS: Slide size {w:.3f}x{h:.3f}")

    for i, slide in enumerate(prs.slides, 1):
        for shape in slide.shapes:
            # Check fill colors
            if shape.shape_type is not None and hasattr(shape, 'fill'):
                try:
                    fill = shape.fill
                    if fill.type is not None and hasattr(fill, 'fore_color'):
                        c = hex_of(fill.fore_color.rgb)
                        if c and c.upper() not in ALLOWED_COLORS:
                            issues.append(f"Slide {i}, shape '{shape.name}': fill color #{c} NOT in brand palette")
                except:
                    pass

            # Check text colors and fonts
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        # Font color
                        if run.font.color and run.font.color.rgb:
                            c = hex_of(run.font.color.rgb)
                            if c and c.upper() not in ALLOWED_COLORS:
                                issues.append(f"Slide {i}, text '{run.text[:30]}': color #{c} NOT in brand palette")
                        # Font name (C5-C8)
                        fname = run.font.name
                        if fname and fname not in ("Inter Tight", "Roboto", "Arial"):
                            issues.append(f"C8 FAIL Slide {i}: font '{fname}' not allowed")

    return issues

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "/home/mia/dev/ppt/review/mock_demo.pptx"
    results = audit(path)
    for r in results:
        print(r)
    fails = [r for r in results if "FAIL" in r or "NOT in" in r]
    print(f"\n{'='*50}")
    print(f"Total checks: {len(results)} | Issues: {len(fails)}")
    if not fails:
        print("✅ All automated checks passed!")
    else:
        print("❌ Issues found — review above.")
```

**Step 2: Run the audit**

Run:
```bash
/home/mia/.venvs/pptx/bin/python /home/mia/dev/ppt/review/audit_brand.py /home/mia/dev/ppt/review/mock_demo.pptx
```

Expected: List of pass/fail results for colors, fonts, and dimensions.

---

### Task 4: Visual Inspection of Exported Slide Images

**Step 1: View each slide image and compare against brand rules**

For each slide PNG in `/home/mia/dev/ppt/review/slides/`, use the `read` tool to view the image and manually check:

| Slide | Type | Check C9 (logo position) | Check C10 (logo variant) | Check C3 (bg color) | Check C15 (margins) | Check C13 (cards) | Check C14 (buttons) |
|-------|------|--------------------------|--------------------------|---------------------|---------------------|-------------------|---------------------|
| 1     | cover | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2     | section_divider | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3     | agenda | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4     | content | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5     | two_column | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6     | quote | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7     | metrics | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8     | team | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9     | case_study | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10    | closing | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

**Step 2: Record findings in compliance report**

---

### Task 5: Write the Compliance Report

**Files:**
- Create: `/home/mia/dev/ppt/review/COMPLIANCE_REPORT.md`

Compile all automated audit results + visual inspection into a single report with:

1. **Executive Summary** — overall pass/fail
2. **Per-Slide Breakdown** — slide type, thumbnail, checklist results
3. **Issues Found** — specific deviations with rule IDs
4. **Recommendations** — fixes needed in slide renderers or brand.json

---

### Task 6: Commit

```bash
cd /home/mia/dev/ppt
git add review/
git commit -m "docs: add PPTX brand compliance review and mock deck audit"
```
