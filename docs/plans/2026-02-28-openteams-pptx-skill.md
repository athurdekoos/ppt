# OpenTeams PPTX Generator Skill — Implementation Plan

**Status:** ✅ Completed (2026-02-28)

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a pi agent skill (`openteams-pptx`) that generates modern, on-brand PowerPoint presentations from natural-language prompts, using the OpenTeams 2025 Brand Guidelines, local logo assets, and website-derived visual cues.

**Architecture:** The skill is a SKILL.md that instructs the agent how to use a bundled Python library (`scripts/generate_deck.py`) to produce `.pptx` files. The Python library encapsulates brand tokens, a slide-type registry, and a `python-pptx`-based renderer. The agent gathers slide content from the user, writes a JSON slide spec, then invokes the script. The brand reference data (colors, fonts, logo paths, site style tokens) lives in `references/brand.json` so it's loadable without re-crawling.

**Tech Stack:** Python 3.11+, python-pptx, Pillow, lxml, requests+beautifulsoup4 (optional, for site crawl refresh)

---

## Part A — Brand Reference Layer

### Task 1: Create the skill directory structure

**Files:**
- Create: `openteams-pptx/SKILL.md` (stub)
- Create: `openteams-pptx/scripts/` (directory)
- Create: `openteams-pptx/references/` (directory)
- Create: `openteams-pptx/assets/` (symlink or copy of logos)

**Step 1: Create directories**
```bash
mkdir -p /home/mia/dev/ppt/openteams-pptx/{scripts,references,assets}
```

**Step 2: Symlink logo assets**

> **Note:** The actual directory on disk is `Assets` (capital A, correctly spelled).
> The legacy `assets_index.json` contains a typo (`Assests/`) — do NOT follow that spelling.
> All paths in `brand.json` use the symlink `assets/logos/` which points to the real `Assets/` directory.

```bash
ln -s /home/mia/dev/ppt/Assets /home/mia/dev/ppt/openteams-pptx/assets/logos
```

**Step 3: Create stub SKILL.md**
Create `/home/mia/dev/ppt/openteams-pptx/SKILL.md` with frontmatter only (name + description placeholder).

**Step 4: Commit**
```bash
git add openteams-pptx/
git commit -m "chore: scaffold openteams-pptx skill directory"
```

---

### Task 2: Create `references/brand.json` — the single source of truth

This file encodes every brand token extracted from the Brand Guidelines PDF, the `site_style.json`, and `assets_index.json` into one merged, self-contained JSON. The generation script reads only this file at runtime.

**Files:**
- Create: `openteams-pptx/references/brand.json`

**Step 1: Write brand.json**

The file must contain these sections:

```json
{
  "colors": {
    "night_navy":  "#022791",
    "day_blue":    "#4D75FE",
    "salmon":      "#FF8A69",
    "yellow":      "#FAA944",
    "black":       "#0C0C0C",
    "gray":        "#262626",
    "text":        "#3F3F3F",
    "white":       "#FFFFFF",
    "light_bg":    "#F7F8FC",
    "light_blue":  "#E8EDFB",
    "accent_green":"#3AD58E"
  },
  "color_roles": {
    "primary":          "night_navy",
    "primary_bright":   "day_blue",
    "accent_warm_1":    "salmon",
    "accent_warm_2":    "yellow",
    "bg_default":       "white",
    "bg_subtle":        "light_bg",
    "text_heading":     "gray",
    "text_body":        "text",
    "footer_text":      "text"
  },
  "gradient": {
    "hero": {"from": "night_navy", "to": "day_blue", "angle": 135},
    "cta_button": {"from": "salmon", "to": "day_blue", "angle": 90}
  },
  "typography": {
    "headline_font":    "Inter Tight",
    "headline_weight":  "Bold",
    "body_font":        "Inter Tight",
    "body_weight":      "Regular",
    "utility_font":     "Roboto",
    "fallback":         "Arial"
  },
  "type_scale_pt": {
    "hero":     90,
    "h1":       44,
    "h2":       32,
    "h3":       24,
    "h4":       18,
    "body":     14,
    "body_lg":  18,
    "small":    11,
    "caption":  10
  },
  "spacing_inches": {
    "margin":      0.6,
    "gutter":      0.35,
    "section_pad": 0.5
  },
  "card_style": {
    "radius_pt":       12,
    "shadow_blur_emu":  152400,
    "shadow_dist_emu":  38100,
    "shadow_alpha_pct": 15
  },
  "button_style": {
    "shape":       "pill",
    "radius_pt":   20,
    "fill_color":  "day_blue",
    "text_color":  "white",
    "font_size_pt": 13
  },
  "logo_rules": {
    "min_size_px":          100,
    "clearspace_unit":      "O_width",
    "allowed_placements":   ["upper-left", "lower-left", "upper-center", "lower-center"],
    "forbidden_placements": ["right-aligned"],
    "dont_alter_colors":    true,
    "dont_add_tagline":     true,
    "dont_distort":         true
  },
  "logo_assets": {
    "colored_horizontal_png": "assets/logos/OT_Colored_Logos/Colored-Horizontal-transparent-logo/OT-new-logo-final.png",
    "colored_vertical_png":   "assets/logos/OT_Colored_Logos/Colored-vertical-transparent-logo/OT-new-logo-vertical-lockup.png",
    "white_horizontal_png":   "assets/logos/OT_White_Logos/White-Horizontal-transparent-logo/OT-new-logo-final-white-horizontal-lockup.png",
    "black_horizontal_png":   "assets/logos/OT_Black_Logos/Black-Horizontal-tansparent/OpennTeams_logo_horizontal_lockup_black.png",
    "favicon_colored_png":    "assets/logos/OT_Colored_Logos/Favicon-transparent-background/OpenTeams-favicon-01.png",
    "favicon_white_png":      "assets/logos/OT_White_Logos/White-Horizontal-transparent-logo/OT-new-logo-final-white-favicon.png"
  },
  "website_cues": {
    "hero_style":       "large headline left-aligned, illustration/image right, white or light gradient bg",
    "card_elevation":   "shadow-based, no visible border",
    "button_style":     "pill/fully-rounded, gradient or solid Day Blue, white text",
    "icon_style":       "line icons, medium stroke, brand-colored",
    "image_treatment":  "rounded corners ~16px, occasional blue tint overlays",
    "section_padding":  "generous (96px web → 0.5in slides)",
    "white_dominant":   true,
    "accent_dots":      "decorative transparent circles in yellow/salmon/blue"
  },
  "slide_dimensions": {
    "width_inches":  13.333,
    "height_inches": 7.5,
    "aspect":        "16:9"
  }
}
```

**Step 2: Verify JSON is valid**
```bash
python3 -c "import json; json.load(open('openteams-pptx/references/brand.json'))"
```
Expected: no error.

**Step 3: Commit**
```bash
git add openteams-pptx/references/brand.json
git commit -m "feat: add brand.json reference with all brand tokens"
```

---

### Task 3: Create `references/slide_types.md` — slide type catalog

This is a reference doc the agent reads to understand what slide types are available and what content each requires. The agent uses this to translate user requests into structured JSON.

**Files:**
- Create: `openteams-pptx/references/slide_types.md`

**Step 1: Write the slide type catalog**

Document each slide type with:
- Name and ID (e.g., `cover`, `section_divider`, `agenda`, `content`, `two_column`, `quote`, `metrics`, `team`, `case_study`, `closing`, `blank`)
- Required fields (title, subtitle, items, etc.)
- Optional fields
- Visual description (so the agent can match user intent to slide type)

Include a JSON schema example for the full deck spec:

```json
{
  "title": "Deck title for filename",
  "slides": [
    {
      "type": "cover",
      "title": "...",
      "subtitle": "...",
      "date": "February 2026"
    },
    {
      "type": "agenda",
      "items": ["Topic 1", "Topic 2", "Topic 3"]
    },
    {
      "type": "content",
      "title": "...",
      "body": "...",
      "image_placeholder": "Description of visual"
    }
  ]
}
```

**Step 2: Commit**
```bash
git add openteams-pptx/references/slide_types.md
git commit -m "feat: add slide type catalog reference"
```

---

## Part B — Python Generation Script

### Task 4: Extract and refactor `build_template.py` into `scripts/generate_deck.py`

The existing `build_template.py` (1547 lines) already has all the PowerPoint-building logic. We'll refactor it into a reusable script that:
1. Reads `brand.json` instead of hard-coding tokens
2. Reads a **slide spec JSON** (from stdin or file) instead of generating fixed demo content
3. Renders each slide per the spec using the existing `SlideBuilder` class

**Files:**
- Create: `openteams-pptx/scripts/generate_deck.py`
- Create: `openteams-pptx/scripts/brand_engine.py` (brand token loader + theme builder)
- Create: `openteams-pptx/scripts/slide_renderers.py` (one function per slide type)
- Create: `openteams-pptx/scripts/pptx_helpers.py` (low-level shape/gradient/shadow helpers)
- ~~`openteams-pptx/scripts/__init__.py`~~ — **Not needed.** Scripts are standalone, not a package (see Step 4).

**Step 1: Create `pptx_helpers.py`**

Extract from `build_template.py` sections 5 (PowerPoint helpers):
- `hex_to_rgbcolor`, `luminance`, `contrast_ratio`, `auto_text_color`
- `set_shape_fill`, `set_shape_rounded_rect_radius`, `set_no_border`
- `add_slide_bg_color`, `make_gradient_rect`, `set_shape_alpha`
- `_get_spPr`

No changes to logic — just move to separate module.

**Step 2: Create `brand_engine.py`**

- `load_brand(brand_json_path) -> BrandConfig` dataclass
- `BrandConfig` holds colors dict, typography dict, logo paths (resolved to absolute), spacing, card/button styles
- `build_theme(brand: BrandConfig) -> ThemeConfig` (same as existing)
- Resolve logo paths relative to the skill directory

**Step 3: Create `slide_renderers.py`**

Extract the `SlideBuilder` class and all `build_slide_*` functions. Modify them to:
- Accept content from a dict (the slide spec) instead of hard-coded strings
- Fall back to placeholder text if a field is missing (keeps template-preview mode working)

Registry pattern:
```python
RENDERERS = {
    "cover":            render_cover,
    "section_divider":  render_section_divider,
    "agenda":           render_agenda,
    "content":          render_content,
    "two_column":       render_two_column,
    "quote":            render_quote,
    "metrics":          render_metrics,
    "team":             render_team,
    "case_study":       render_case_study,
    "closing":          render_closing,
    "blank":            render_blank,
}
```

Each renderer signature: `render_*(sb: SlideBuilder, spec: dict) -> None`

**Step 4: Create `generate_deck.py` (CLI entry point)**

This is a **standalone script** (not a package import). It uses only same-directory relative imports
so it can be invoked directly:

```
Usage:
  python generate_deck.py --spec slides.json --brand ../references/brand.json --out output.pptx
  # OR
  echo '{"slides":[...]}' | python generate_deck.py --brand ../references/brand.json --out output.pptx
```

All cross-module imports within `scripts/` must use explicit `sys.path` manipulation or be
co-located flat imports (e.g., `from brand_engine import ...`), NOT relative package imports.
This avoids the `python scripts/generate_deck.py` vs `python -m scripts.generate_deck` ambiguity.
Remove `__init__.py` — these are standalone scripts in a shared directory, not a package.

Logic:
1. Load brand config
2. Build theme
3. **Validate the slide spec** (see Step 4a below)
4. Create Presentation with correct dimensions
5. For each slide in spec, look up renderer, call it
6. Save .pptx

**Step 4a: Add `validate_spec()` to `generate_deck.py`**

Before rendering, validate the incoming JSON spec to catch agent errors early with clear messages:

```python
REQUIRED_FIELDS = {
    "cover":           ["title"],
    "section_divider": ["title"],
    "agenda":          ["items"],
    "content":         ["title"],
    "two_column":      ["title", "left_title", "right_title"],
    "quote":           ["text"],
    "metrics":         ["title", "metrics"],
    "team":            ["title", "members"],
    "case_study":      ["title", "challenge", "solution", "results"],
    "closing":         ["title"],
    "blank":           [],
}

def validate_spec(spec: dict) -> list[str]:
    """Return a list of human-readable error strings. Empty list = valid."""
    errors = []
    if "slides" not in spec or not isinstance(spec["slides"], list):
        return ["Spec must contain a 'slides' array."]
    for i, slide in enumerate(spec["slides"], 1):
        stype = slide.get("type")
        if not stype:
            errors.append(f"Slide {i}: missing 'type' field.")
            continue
        if stype not in REQUIRED_FIELDS:
            errors.append(f"Slide {i}: unknown type '{stype}'. "
                          f"Valid types: {', '.join(REQUIRED_FIELDS)}")
            continue
        for field in REQUIRED_FIELDS[stype]:
            if field not in slide:
                errors.append(f"Slide {i} ({stype}): missing required field '{field}'.")
    return errors
```

On validation failure, print all errors to stderr and exit with code 1.
On success, proceed to rendering.

**Step 5: Test with the existing template content as a spec**

Write a quick `test_spec.json` that reproduces the 10 demo slides from `build_template.py`. Run:
```bash
cd /home/mia/dev/ppt/openteams-pptx
/home/mia/.venvs/pptx/bin/python scripts/generate_deck.py \
  --spec test_spec.json \
  --brand references/brand.json \
  --out /tmp/test_output.pptx
```
Expected: 10-slide .pptx file, visually matching the original template.

**Step 6: Commit**
```bash
git add openteams-pptx/scripts/
git commit -m "feat: add generate_deck.py with modular slide renderers"
```

---

### Task 5: Add website crawl refresh capability (optional)

**Files:**
- Create: `openteams-pptx/scripts/refresh_site_style.py`

This is a standalone script the agent can run to re-crawl `openteams.com` and update `brand.json`'s `website_cues` section. It extracts:
- CSS custom properties (colors, fonts, spacing)
- Card border-radius values
- Box-shadow patterns
- Background color distribution
- Button styles

Based on the existing `crawl_website()` function in `build_template.py`.

**Step 1: Write the script**

```bash
python refresh_site_style.py --url https://openteams.com/ --brand-json ../references/brand.json
```

It should:
1. Crawl homepage + up to 3 subpages
2. Extract CSS tokens
3. Merge into `brand.json` under `website_cues` (without touching `colors`, `typography`, or `logo_rules`)
4. Print a diff summary

**Step 2: Test**
```bash
/home/mia/.venvs/pptx/bin/python scripts/refresh_site_style.py \
  --url https://openteams.com/ \
  --brand-json references/brand.json
```

**Step 3: Commit**
```bash
git add openteams-pptx/scripts/refresh_site_style.py
git commit -m "feat: add website style refresh script"
```

---

## Part C — The Skill (SKILL.md)

### Task 6: Write the complete SKILL.md

**Files:**
- Modify: `openteams-pptx/SKILL.md`

This is the core of the skill — what the agent reads when triggered. It must cover:

**Frontmatter:**
```yaml
---
name: openteams-pptx
description: >
  Generate modern, on-brand OpenTeams PowerPoint presentations from natural language.
  Use this skill whenever the user asks to create a presentation, slide deck, pitch deck,
  or .pptx file for OpenTeams. Also trigger when the user mentions "slides", "powerpoint",
  "deck", "presentation template", or wants to present OpenTeams content to clients,
  partners, or internal stakeholders. Covers cover slides, agendas, content layouts,
  metrics dashboards, team pages, case studies, quotes, and closing slides.
---
```

**Body sections:**

1. **Overview** — What this skill does (generates .pptx files using OpenTeams brand)

2. **How It Works** — Three-phase workflow:
   - **Phase 1: Gather content** — Ask the user what the presentation is about. Determine slide count, types, and content. Reference `references/slide_types.md` for available types.
   - **Phase 2: Build slide spec** — Write a JSON file following the schema in `slide_types.md`. Save to a temp file.
   - **Phase 3: Generate** — Run `scripts/generate_deck.py` with the spec. The script uses `references/brand.json` for all brand tokens. Present the output file path to the user.

3. **Brand Rules (Non-Negotiable)** — Key constraints the agent must never violate:
   - Colors: Night Navy `#022791` and Day Blue `#4D75FE` are primary. Salmon and Yellow are accents only.
   - Typography: Inter Tight Bold for headlines, Inter Tight Regular for body. Never use other fonts.
   - Logo: Always upper-left or lower-left/center. Never right-aligned. Never add tagline. Never alter colors.
   - White-dominant backgrounds for most slides. Dark backgrounds (Night Navy) only for section dividers, quotes, and closing.
   - Gradient usage: Night Navy → Day Blue for hero sections and closing slides only.

4. **Website Visual Cues (Style Preference)** — Softer guidelines derived from openteams.com:
   - Pill-shaped buttons with Day Blue fill
   - Card-based layouts with subtle shadow elevation, no visible borders
   - Generous whitespace (0.6" margins, 0.35" gutters)
   - Decorative accent dots (translucent circles in brand accent colors)
   - Rounded corners on image placeholders (~12pt radius)
   - Clean, minimal aesthetic — avoid clutter

5. **Slide Types Reference** — Point to `references/slide_types.md` for the full catalog

6. **Script Usage** — Exact command to generate.

   The agent resolves `<skill-dir>` as the **parent directory of this SKILL.md file**.
   Per pi skill conventions, when SKILL.md references a relative path, the agent resolves it
   against the skill directory (the dirname of SKILL.md). The SKILL.md must state this explicitly:

   > All paths below are relative to this skill's directory (the folder containing this SKILL.md).

   Exact command:
   ```bash
   /home/mia/.venvs/pptx/bin/python <skill-dir>/scripts/generate_deck.py \
     --spec <spec-file>.json \
     --brand <skill-dir>/references/brand.json \
     --out <output-path>.pptx
   ```
   Where `<skill-dir>` = the directory containing this SKILL.md (e.g., `/home/mia/dev/ppt/openteams-pptx`).

7. **Refreshing Website Styles** — When to run the refresh script (e.g., if user says site was recently updated)

8. **Tips for Great Decks:**
   - Keep slide count to 8-15 for most presentations
   - One key message per slide
   - Use metrics slides for quantitative claims
   - Use quote slides to break up dense sections
   - Always start with cover, end with closing
   - Agenda slide for 5+ content slides

**Step 1: Write the full SKILL.md**

**Step 2: Validate it's under 500 lines**

**Step 3: Commit**
```bash
git add openteams-pptx/SKILL.md
git commit -m "feat: write complete SKILL.md for openteams-pptx"
```

---

## Part D — Testing & Validation

### Task 7: End-to-end test with a real prompt

**Step 1: Create a test spec by hand**

Write `openteams-pptx/tests/test_ai_readiness.json` — a realistic 8-slide deck:
```json
{
  "title": "AI Readiness Assessment",
  "slides": [
    {"type": "cover", "title": "AI Readiness Assessment", "subtitle": "Helping enterprises prepare for AI adoption", "date": "February 2026"},
    {"type": "agenda", "items": ["Current State Analysis", "AI Maturity Model", "Gap Assessment", "Recommended Roadmap", "Investment Overview"]},
    {"type": "content", "title": "Why AI Readiness Matters", "body": "Organizations that invest in AI readiness see 3x faster time-to-value.\n\nWithout proper preparation, 85% of AI initiatives fail to reach production.", "image_placeholder": "AI adoption curve chart"},
    {"type": "two_column", "title": "Assessment Framework", "left_title": "Technical Readiness", "left_body": "Data infrastructure\nML pipeline maturity\nCompute & tooling\nSecurity posture", "right_title": "Organizational Readiness", "right_body": "Talent & skills gap\nChange management\nGovernance framework\nBudget alignment"},
    {"type": "metrics", "title": "Your Readiness Scores", "metrics": [{"value": "72%", "label": "Data Readiness"}, {"value": "45%", "label": "Infra Maturity"}, {"value": "88%", "label": "Team Alignment"}, {"value": "60%", "label": "Governance"}]},
    {"type": "quote", "text": "The best time to prepare for AI was yesterday.\nThe second best time is now.", "attribution": "OpenTeams Advisory"},
    {"type": "case_study", "title": "Case Study: Fortune 500 Biotech", "challenge": "Scattered ML workflows across 12 teams with no shared infrastructure.", "solution": "OpenTeams deployed Nebari as a unified ML platform with SSO and RBAC.", "results": "70% reduction in experiment-to-production time. $2.4M annual savings."},
    {"type": "closing", "title": "Let's Build Your AI Future", "subtitle": "Ready to get started?", "contact": "ai@openteams.com  |  openteams.com/ai-readiness-assessment"}
  ]
}
```

**Step 2: Generate the deck**
```bash
/home/mia/.venvs/pptx/bin/python openteams-pptx/scripts/generate_deck.py \
  --spec openteams-pptx/tests/test_ai_readiness.json \
  --brand openteams-pptx/references/brand.json \
  --out /tmp/ai_readiness_test.pptx
```
Expected: Clean exit, file created.

**Step 3: Validate programmatically**
```python
from pptx import Presentation
prs = Presentation('/tmp/ai_readiness_test.pptx')
assert len(prs.slides) == 8
assert prs.slide_width.inches > 13  # widescreen
```

**Step 4: Commit tests**
```bash
git add openteams-pptx/tests/
git commit -m "test: add AI readiness e2e test spec"
```

---

### Task 8: Template-preview mode (generate demo deck with placeholder content)

**Step 1: Add `--demo` flag to `generate_deck.py`**

When invoked with `--demo`, generate the same 10-slide deck as the original `build_template.py` with all placeholder text. This serves as a showcase of all slide types.

**Step 2: Test**
```bash
/home/mia/.venvs/pptx/bin/python openteams-pptx/scripts/generate_deck.py \
  --demo \
  --brand openteams-pptx/references/brand.json \
  --out /tmp/demo_template.pptx
```

**Step 3: Commit**
```bash
git commit -m "feat: add --demo mode for template preview generation"
```

---

## Part E — Installation & Docs

### Task 9: Create requirements.txt and README

**Files:**
- Create: `openteams-pptx/requirements.txt`
- Create: `openteams-pptx/README.md`

**Step 1: Write requirements.txt**
```
python-pptx>=1.0.0
Pillow>=9.0.0
lxml>=4.0.0
requests>=2.28.0
beautifulsoup4>=4.11.0
```

**Step 2: Write README.md**
- What it does
- Prerequisites (Python 3.11+, venv at `/home/mia/.venvs/pptx/`)
- Quick start: "Ask the agent to create a presentation"
- Manual usage: CLI commands
- Brand guidelines summary
- Directory structure

**Step 3: Commit**
```bash
git add openteams-pptx/requirements.txt openteams-pptx/README.md
git commit -m "docs: add README and requirements for openteams-pptx skill"
```

---

### Task 10: Install the skill

**Step 1: Symlink to pi skills directory**
```bash
ln -s /home/mia/dev/ppt/openteams-pptx /home/mia/.pi/agent/skills/openteams-pptx
```

**Step 2: Verify skill is discoverable**

Start a new pi session and check that the skill appears in the available skills list. Test with a prompt like:
> "Create a 5-slide presentation about OpenTeams' Nebari platform"

**Step 3: Final commit**
```bash
git add -A
git commit -m "feat: complete openteams-pptx skill — ready for use"
```

---

## Summary

| Task | Deliverable | Depends On |
|------|-------------|------------|
| 1 | Directory scaffold | — |
| 2 | `references/brand.json` | 1 |
| 3 | `references/slide_types.md` | 1 |
| 4 | `scripts/generate_deck.py` + modules | 2, 3 |
| 5 | `scripts/refresh_site_style.py` | 2, 4 |
| 6 | `SKILL.md` (complete) | 3, 4 |
| 7 | E2E test with real spec | 4, 6 |
| 8 | `--demo` template mode | 4 |
| 9 | README + requirements | 4, 6 |
| 10 | Install & verify | all |

**Estimated effort:** Tasks 1-3 are fast (scaffolding + data). Task 4 is the bulk — refactoring 1500 lines into modular scripts. Tasks 5-10 are incremental.
