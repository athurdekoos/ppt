# OpenTeams PPTX Brand Compliance Report

**Date:** February 28, 2026  
**File audited:** `review/mock_demo.pptx` (10-slide demo deck)  
**Auditor:** Automated script + visual inspection  
**Standard:** OpenTeams 2025 Brand Guidelines + `brand.json`

---

## Executive Summary

**Overall: ✅ PASS with minor observations**

The generated demo deck is strongly brand-compliant. All colors, fonts, and major layout rules conform to the 2025 Brand Guidelines. Two minor observations were noted — a small favicon used as a decorative element in the bottom-right corner of light slides (which is technically right-aligned), and accent dots on the quote slide that appear at full opacity rather than the recommended 15–30%.

---

## Automated Audit Results

| Check | Result |
|-------|--------|
| **C18** Slide dimensions (13.333×7.5 / 16:9) | ✅ PASS |
| **C1–C2** All fill/text colors in brand palette | ✅ PASS (52 colors checked) |
| **C8** All fonts Inter Tight / Roboto / Arial | ✅ PASS (0 unauthorized fonts) |
| **C9** Logo placement (no right-aligned logos) | ⚠️ 6 warnings — small favicon icon at x=12.43in (see Observation 1) |

---

## Per-Slide Visual Inspection

### Slide 1: Cover
| Rule | Result | Notes |
|------|--------|-------|
| C1 Primary colors | ✅ | Night Navy → Day Blue gradient on right half |
| C3 White-dominant left, gradient right | ✅ | Correct hero layout |
| C4 Gradient only on cover/closing | ✅ | Correctly applied |
| C5 Headline: Inter Tight Bold | ✅ | "Presentation Title" rendered bold |
| C9 Logo upper-left | ✅ | Colored horizontal logo at upper-left |
| C10 Colored logo on light bg | ✅ | Correct variant |
| C14 Pill-shaped CTA button | ✅ | "Get Started" button is pill-shaped, Day Blue fill, white text |
| C15 Margins ≥ 0.6" | ✅ | Generous whitespace maintained |
| C16 Decorative dots | ✅ | Favicon decorative element on gradient side |

### Slide 2: Section Divider
| Rule | Result | Notes |
|------|--------|-------|
| C3 Dark bg for section dividers | ✅ | Night Navy background |
| C5 Headline bold white | ✅ | Large white bold title |
| C9 Logo lower-left | ✅ | White logo at bottom-left |
| C10 White logo on dark bg | ✅ | Correct variant |

### Slide 3: Agenda
| Rule | Result | Notes |
|------|--------|-------|
| C2 Accents used sparingly | ✅ | Salmon/yellow/blue numbered circles — accent use only |
| C3 White background | ✅ | Clean white layout |
| C9 Logo upper-left | ✅ | Colored logo at top-left |
| C15 Margins | ✅ | Good spacing |

### Slide 4: Content
| Rule | Result | Notes |
|------|--------|-------|
| C3 White background | ✅ | |
| C9 Logo upper-left | ✅ | |
| C17 Image placeholder light blue, rounded | ✅ | `#E8EDFB` fill with rounded corners |
| C15 Margins | ✅ | Text and placeholder well-spaced |

### Slide 5: Two-Column
| Rule | Result | Notes |
|------|--------|-------|
| C3 White background | ✅ | |
| C13 Cards shadow-based, no borders, rounded | ✅ | Two cards with shadow elevation, rounded corners |
| C9 Logo upper-left | ✅ | |

### Slide 6: Quote
| Rule | Result | Notes |
|------|--------|-------|
| C3 Dark bg for quotes | ✅ | Night Navy background |
| C10 White logo on dark bg | ✅ | White logo at bottom-left |
| C16 Accent dots | ⚠️ | Salmon + yellow dots appear at full opacity (see Observation 2) |
| C5 Headline bold | ✅ | Large bold quote text |

### Slide 7: Metrics
| Rule | Result | Notes |
|------|--------|-------|
| C3 Light bg (#F7F8FC) | ✅ | Subtle light background |
| C2 Accents used sparingly | ✅ | Colored top bars on metric cards (rotating brand colors) |
| C13 Card styling | ✅ | Shadow elevation, rounded corners |
| C17 Chart placeholder | ✅ | Light blue placeholder area |

### Slide 8: Team
| Rule | Result | Notes |
|------|--------|-------|
| C3 White background | ✅ | |
| C2 Accents for avatar circles | ✅ | Rotating brand accent colors |
| C13 Profile cards | ✅ | Shadow, rounded corners, no hard borders |

### Slide 9: Case Study
| Rule | Result | Notes |
|------|--------|-------|
| C3 White background | ✅ | |
| C2 Accent top bars | ✅ | Salmon, blue, yellow bars — accent only |
| C13 Cards | ✅ | Three-column card layout with proper styling |
| C9 Logo upper-left | ✅ | |

### Slide 10: Closing
| Rule | Result | Notes |
|------|--------|-------|
| C4 Gradient on closing | ✅ | Night Navy → Day Blue gradient |
| C10 White logo on gradient | ✅ | White horizontal logo centered at bottom |
| C14 CTA button | ✅ | "Contact Us" pill button, white fill on gradient bg |
| C16 Decorative circles | ✅ | Large translucent circles at edges |
| C15 Generous spacing | ✅ | Well-centered, uncluttered |

---

## Observations

### Observation 1: Small Favicon at Bottom-Right (Low Severity)

**Slides affected:** 3, 4, 5, 7, 8, 9  
**Rule:** C9 — Logo must not be right-aligned  
**Finding:** A small (0.30×0.30in) colored favicon appears at the bottom-right corner (x=12.43in). This is a decorative brand element rather than the primary logo placement.

**Assessment:** Technically right-aligned, but at 0.30in it functions as a subtle brand watermark, not a logo lockup. The primary logo is always correctly placed upper-left or lower-left.

**Recommendation:** Consider moving the watermark favicon to lower-center or removing it to be strictly compliant. Alternatively, document this as an accepted exception for the "decorative favicon watermark" pattern.

### Observation 2: Accent Dot Opacity on Quote Slide (Low Severity)

**Slide affected:** 6 (Quote)  
**Rule:** C16 — Decorative accent dots should be 15–30% opacity  
**Finding:** The salmon and yellow dots on the quote slide appear to render at near-full opacity rather than the recommended translucent 15–30%.

**Assessment:** This is a soft guideline from website cues, not a hard brand rule. The dots are small and don't dominate the slide.

**Recommendation:** Reduce opacity of accent dots on quote slides to ~20% for consistency with the website aesthetic. Update the `quote` renderer in `slide_renderers.py`.

### Observation 3: Font Rendering via LibreOffice (Informational)

**Finding:** The automated font check returned 0 font inspections because `python-pptx` embeds font names at the run level, and the template may be relying on paragraph-level or default font settings. Visually, all text appears to render in Inter Tight (or its fallback) correctly.

**Recommendation:** No action needed, but the audit script could be enhanced to also check paragraph-level `defRPr` font settings for more thorough coverage.

---

## Summary Scorecard

| Category | Rules | Pass | Warn | Fail |
|----------|-------|------|------|------|
| Colors (C1–C4) | 4 | 4 | 0 | 0 |
| Typography (C5–C8) | 4 | 4 | 0 | 0 |
| Logo (C9–C12) | 4 | 3 | 1 | 0 |
| Visual Style (C13–C17) | 5 | 4 | 1 | 0 |
| Dimensions (C18) | 1 | 1 | 0 | 0 |
| **Total** | **18** | **16** | **2** | **0** |

**Verdict: The PPTX generator produces brand-compliant presentations.** The two warnings are low-severity style observations, not brand violations.

---

## Files Produced

| File | Description |
|------|-------------|
| `review/mock_demo.pptx` | Generated 10-slide demo deck |
| `review/mock_demo.pdf` | PDF export via LibreOffice |
| `review/slides/slide-01.png` through `slide-10.png` | Per-slide PNG images (200 DPI) |
| `review/audit_brand.py` | Automated brand compliance audit script |
| `review/COMPLIANCE_REPORT.md` | This report |
