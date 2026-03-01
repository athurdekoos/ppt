# Fix Cover Slide Decorative Dots Implementation Plan

**Status:** ✅ Completed (2026-02-28)

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Remove the translucent decorative dots from the cover slide that appear as small gray balls next to the large favicon on the gradient panel.

**Architecture:** The `render_cover` function in `slide_renderers.py` draws four small oval shapes (0.35" diameter) at 30% opacity on the right-side gradient panel. On the dark Navy→Blue gradient these appear as washed-out gray circles. We remove them entirely — the large favicon + gradient already provide enough visual interest.

**Tech Stack:** Python, python-pptx

---

### Task 1: Remove decorative dots from cover renderer

**Files:**
- Modify: `openteams-pptx/scripts/slide_renderers.py:288-296`

**Step 1: Remove the decorative dots loop**

In `render_cover()`, delete this block (lines ~288–296):

```python
    # Decorative dots
    for dx, dy, col in [
        (8.2, 1.5, sb.theme.yellow), (9.8, 2.0, sb.theme.salmon),
        (8.8, 5.0, sb.theme.day_blue), (10.5, 4.2, sb.theme.yellow),
    ]:
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(dx), Inches(dy),
                                      Inches(0.35), Inches(0.35))
        set_shape_fill(dot, col)
        set_no_border(dot)
        set_shape_alpha(dot, '30000')
```

Replace with nothing (just remove the block entirely).

**Step 2: Regenerate the IBM deck to verify the fix**

Run:
```bash
/home/mia/.venvs/pptx/bin/python /home/mia/.pi/agent/skills/openteams-pptx/scripts/generate_deck.py \
  --spec /tmp/ibm_deck_spec.json \
  --brand /home/mia/.pi/agent/skills/openteams-pptx/references/brand.json \
  --out /home/mia/dev/ppt/OpenTeams_x_IBM.pptx
```

Expected: 10 slides generated successfully. Cover slide (slide 1) should have the gradient panel and large favicon but NO small circles/dots.

**Step 3: Commit**

```bash
cd /home/mia/dev/ppt
git add openteams-pptx/scripts/slide_renderers.py OpenTeams_x_IBM.pptx
git commit -m "fix: remove decorative dots from cover slide gradient panel"
```
