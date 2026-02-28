# Contributing

How to add new slide types, modify existing layouts, and maintain brand compliance.

## Adding a New Slide Type

Adding a slide type takes three steps:

### 1. Define the Renderer

Add a function to `scripts/slide_renderers.py`:

```python
def render_timeline(sb: SlideBuilder, spec: dict) -> None:
    """Timeline slide with milestone markers."""
    slide = sb.new_slide()
    add_slide_bg_color(slide, "#FFFFFF")

    sb.add_logo(slide, "colored", "upper-left", max_width_inches=1.8, max_height_inches=0.45)
    sb.add_accent_bar(slide, sb.M, Inches(1.2), Inches(0.8), Inches(0.06))

    title = spec.get("title", "Timeline")
    sb.add_title(slide, title, y=Inches(1.4), font_size=sb.theme.h2_size)

    # Your layout logic here — use sb.add_card(), sb.add_body(), etc.

    sb.add_footer(slide, show_logo=True)
```

**Every renderer must:**
- Accept `(sb: SlideBuilder, spec: dict)`
- Call `sb.new_slide()` first
- Set the background color
- Add logo and footer

### 2. Register It

Add to the `RENDERERS` dict at the bottom of `slide_renderers.py`:

```python
RENDERERS = {
    # ... existing types ...
    "timeline":     render_timeline,
}
```

### 3. Add Validation

Add required fields in `generate_deck.py`:

```python
REQUIRED_FIELDS = {
    # ... existing types ...
    "timeline":    ["title", "milestones"],
}
```

### 4. Document It

Add the slide type to `references/slide_types.md` with:
- Purpose description
- Visual description
- Field table (name, required, type, description)

### 5. Test It

Add a test case in `tests/test_core.py`:

```python
def test_timeline_slide(self):
    spec = {"slides": [{
        "type": "timeline",
        "title": "Project Timeline",
        "milestones": [{"date": "Q1", "label": "Launch"}]
    }]}
    with tempfile.NamedTemporaryFile(suffix=".pptx", delete=False) as f:
        out_path = f.name
    try:
        generate(spec, BRAND_JSON, out_path)
        assert os.path.exists(out_path)
    finally:
        os.unlink(out_path)
```

Also verify `test_all_slide_types_have_validation` still passes — it checks that every key in `RENDERERS` has a matching entry in `REQUIRED_FIELDS`.

## Modifying Existing Layouts

### Changing Positions/Sizes

Layout values are in EMUs (English Metric Units) via `Inches()` and `Pt()`:

```python
Inches(1.0)  # 1 inch = 914400 EMU
Pt(12)       # 12 points = 152400 EMU
```

Common layout constants:
- `sb.W` — slide width (13.333")
- `sb.H` — slide height (7.5")
- `sb.M` — margin (0.6")
- `sb.G` — gutter (0.35")

### Changing Colors/Fonts

**Don't hardcode them.** Use `sb.theme`:

```python
# ✅ Correct
color=sb.theme.night_navy
font_name=sb.theme.headline_font

# ❌ Wrong
color="#022791"
font_name="Inter Tight"
```

Colors and fonts come from `references/brand.json`. Change them there if the brand guidelines update.

### Accent Color Cycling

Use `sb.ACCENT_ROTATION` for consistent cycling:

```python
for i, item in enumerate(items):
    accent = sb.ACCENT_ROTATION[i % len(sb.ACCENT_ROTATION)]
```

## Brand Rules (Do Not Break)

These are enforced by the skill and must never be violated:

1. **No right-aligned logos** — upper-left, lower-left, or center only
2. **White logo on dark backgrounds** — colored logo on light backgrounds
3. **Salmon and Yellow are accents only** — never as primary/dominant fill
4. **Inter Tight for all text** — Roboto only for footers/captions
5. **No decorative dots on cover slide gradient panel**
6. **Max 6 team member cards** — layout doesn't support more

## Running Tests

```bash
# Run all tests
~/.venvs/pptx/bin/python -m pytest tests/ -v

# Run a single test
~/.venvs/pptx/bin/python -m pytest tests/test_core.py::TestGeneration::test_demo_deck_generates -v
```

Tests must pass before committing. The test suite covers:
- Color utility functions (hex parsing, luminance, contrast)
- Spec validation (required fields, unknown types, edge cases)
- Generation smoke tests (demo deck, single slides, truncation)

## Commit Messages

Use [conventional commits](https://www.conventionalcommits.org/):

```
feat: add timeline slide type
fix: correct logo positioning on quote slide
refactor: extract card rendering helper
docs: update slide_types.md with timeline spec
test: add timeline smoke test
```

Do **not** include `Co-Authored-By` lines.
