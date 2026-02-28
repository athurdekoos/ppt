# OpenTeams PPTX Generator Skill

A pi agent skill that generates modern, on-brand OpenTeams PowerPoint presentations from natural-language prompts.

## What It Does

- Generates `.pptx` files following the **OpenTeams 2025 Brand Guidelines**
- Supports 11 slide types: cover, section divider, agenda, content, two-column, quote, metrics, team, case study, closing, and blank
- Uses Night Navy / Day Blue color palette, Inter Tight typography, and proper logo placement
- Produces widescreen (16:9) presentations with professional layouts

## Prerequisites

- **Python 3.11+**
- Virtual environment at `/home/mia/.venvs/pptx/`
- Install dependencies:
  ```bash
  /home/mia/.venvs/pptx/bin/pip install -r ../requirements.txt
  ```

## Quick Start

**As a pi agent skill:** Just ask the agent to create a presentation:
> "Create a 5-slide presentation about OpenTeams' Nebari platform"

The agent will gather content, build a slide spec, and generate the `.pptx` file.

**Manual CLI usage:**

```bash
# Generate from a slide spec JSON
/home/mia/.venvs/pptx/bin/python scripts/generate_deck.py \
  --spec slides.json \
  --brand references/brand.json \
  --out output.pptx

# Generate demo deck (all slide types with placeholder content)
/home/mia/.venvs/pptx/bin/python scripts/generate_deck.py \
  --demo \
  --brand references/brand.json \
  --out demo.pptx
```

## Brand Guidelines Summary

| Element | Rule |
|---------|------|
| **Primary colors** | Night Navy `#022791`, Day Blue `#4D75FE` |
| **Accent colors** | Salmon `#FF8A69`, Yellow `#FAA944` (accents only) |
| **Headlines** | Inter Tight Bold |
| **Body text** | Inter Tight Regular |
| **Logo placement** | Upper-left or lower-left/center only — never right-aligned |
| **Backgrounds** | White-dominant; dark only for dividers, quotes, closing |

## Directory Structure

```
openteams-pptx/
├── SKILL.md                      # Agent skill definition
├── README.md                     # This file
├── .gitignore
├── assets/
│   └── logos -> ../../Assets              # Symlink to logo files
├── references/
│   ├── brand.json                # Brand tokens (colors, fonts, spacing, logos)
│   └── slide_types.md            # Slide type catalog and JSON schema
├── scripts/
│   ├── generate_deck.py          # CLI entry point
│   ├── brand_engine.py           # Brand config loader + theme builder
│   ├── slide_renderers.py        # SlideBuilder class + per-type renderers
│   ├── pptx_helpers.py           # Low-level shape/gradient/shadow helpers
│   └── refresh_site_style.py     # Website crawl to refresh visual cues
└── tests/
    └── test_ai_readiness.json    # Sample 8-slide e2e test spec
```

## Refreshing Website Styles

If the OpenTeams website has been updated, refresh the visual cues in `brand.json`:

```bash
/home/mia/.venvs/pptx/bin/python scripts/refresh_site_style.py \
  --url https://openteams.com/ \
  --brand-json references/brand.json
```
