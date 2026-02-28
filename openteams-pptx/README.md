# OpenTeams PPTX Generator

A [pi](https://github.com/mariozechner/pi-coding-agent) agent skill that generates professional, brand-compliant OpenTeams PowerPoint presentations from natural language.

## What It Does

Ask Claude to make a presentation and it handles everything — content structure, slide layout, brand compliance, and `.pptx` generation. You get a polished deck in seconds.

**Supports 11 slide types:** cover, section divider, agenda, content, two-column, quote, metrics, team, case study, closing, and blank.

## Using the Skill with Claude

### How It Works

When you ask Claude to create a presentation, the skill activates automatically. Here's the typical flow:

**1. You describe what you need:**
> "Create a 10-slide pitch deck for IBM about our open source platform"

**2. Claude asks clarifying questions** (if needed):
- Purpose — pitch deck, internal update, client proposal?
- Audience — clients, partners, investors?
- Slide count — typically 8–15
- Key messages — what should each slide communicate

**3. Claude builds the deck:**
- Selects appropriate slide types for your content
- Writes a JSON slide spec
- Runs the generator
- Presents the output file path

**4. You review and iterate:**
> "Make the metrics slide show 4 KPIs instead of 3"
> "Change the closing slide CTA to 'Schedule a Demo'"

Claude regenerates and you get an updated file.

### Example Prompts

| Prompt | What You Get |
|--------|-------------|
| "Create a pitch deck for Acme Corp" | 10-slide client proposal with cover, agenda, content slides, metrics, and closing |
| "Make me an internal update with 5 slides" | Compact deck with cover, content slides, and closing |
| "Build a case study presentation for the Global Bank project" | Deck featuring challenge → solution → results layout |
| "Generate a demo deck showing all slide types" | All 11 slide types with placeholder content |

### Expected Output

The skill generates a `.pptx` file in the current working directory. Each deck includes:

- **Widescreen (16:9)** format at 13.333" × 7.5"
- **OpenTeams branding** — Night Navy/Day Blue palette, Inter Tight font, proper logo placement
- **Professional layouts** — cards with shadows, accent bars, gradient backgrounds, pill buttons
- **Footer on every slide** — copyright text and favicon

The file opens in PowerPoint, Google Slides, LibreOffice Impress, or Keynote.

### Trigger Phrases

The skill activates when you mention:
- "presentation", "slide deck", "pitch deck", "powerpoint", "pptx"
- "slides", "deck", "presentation template"
- Creating content for clients, partners, or stakeholders

## Quick Start (Manual CLI)

### Prerequisites

- Python 3.11+
- Virtual environment with dependencies:

```bash
python -m venv ~/.venvs/pptx
~/.venvs/pptx/bin/pip install -r requirements.txt
```

### Generate a Deck

**From a slide spec JSON:**
```bash
~/.venvs/pptx/bin/python scripts/generate_deck.py \
  --spec slides.json \
  --brand references/brand.json \
  --out output.pptx
```

**Demo deck (all slide types with placeholder content):**
```bash
~/.venvs/pptx/bin/python scripts/generate_deck.py \
  --demo \
  --brand references/brand.json \
  --out demo.pptx
```

**Pipe JSON from stdin:**
```bash
echo '{"slides":[{"type":"cover","title":"Hello"}]}' | \
  ~/.venvs/pptx/bin/python scripts/generate_deck.py \
  --brand references/brand.json \
  --out quick.pptx
```

### Slide Spec Format

```json
{
  "title": "Deck Title",
  "slides": [
    {"type": "cover", "title": "Main Title", "subtitle": "Tagline", "date": "February 2026"},
    {"type": "agenda", "items": ["Topic 1", "Topic 2", "Topic 3"]},
    {"type": "content", "title": "Key Point", "body": "Details here."},
    {"type": "closing", "title": "Thank You", "contact": "hello@openteams.com"}
  ]
}
```

See [`references/slide_types.md`](references/slide_types.md) for the full schema of all 11 slide types and their required/optional fields.

## Slide Types

| Type | Purpose | Key Fields |
|------|---------|------------|
| `cover` | Opening hero slide | `title`, `subtitle?`, `date?` |
| `section_divider` | Dark section separator | `title`, `subtitle?` |
| `agenda` | Numbered topic list | `items[]` |
| `content` | Title + body + image area | `title`, `body?`, `bullet_items?`, `image_placeholder?` |
| `two_column` | Side-by-side comparison | `title`, `left_title`, `left_body?`, `right_title`, `right_body?` |
| `quote` | Big statement, dark background | `text`, `attribution?` |
| `metrics` | KPI cards + chart area | `title`, `metrics[{value, label}]` |
| `team` | Profile cards (max 6) | `title`, `members[{name, role, bio?}]` |
| `case_study` | Challenge → Solution → Results | `title`, `challenge`, `solution`, `results` |
| `closing` | CTA with contact info | `title`, `subtitle?`, `contact?`, `cta_text?` |
| `blank` | Empty slide with logo | _(none)_ |

## Brand Compliance

These rules are enforced automatically and come from the [OpenTeams 2025 Brand Guidelines](../OpenTeams_Brand_Guidelines_2025.pdf):

| Element | Rule |
|---------|------|
| **Primary colors** | Night Navy `#022791`, Day Blue `#4D75FE` |
| **Accent colors** | Salmon `#FF8A69`, Yellow `#FAA944` — accents only, never dominant |
| **Headlines** | Inter Tight Bold |
| **Body text** | Inter Tight Regular |
| **Utility text** | Roboto (footers, captions) |
| **Logo placement** | Upper-left or lower-left/center — **never right-aligned** |
| **Logo on dark backgrounds** | White variant only |
| **Backgrounds** | White-dominant; dark (Night Navy) for dividers, quotes, closing only |
| **Gradients** | Night Navy → Day Blue for cover and closing slides only |
| **Cover slide** | No decorative dots on the gradient panel |

## Running Tests

```bash
~/.venvs/pptx/bin/pip install pytest
~/.venvs/pptx/bin/python -m pytest tests/ -v
```

Tests cover color utilities, spec validation, and smoke-test generation for all slide types.

## Directory Structure

```
openteams-pptx/
├── SKILL.md                       # Pi agent skill definition
├── README.md                      # This file
├── assets/
│   └── logos -> ../../Assets      # Symlink to logo files
├── references/
│   ├── brand.json                 # Brand tokens (colors, fonts, spacing, logos)
│   └── slide_types.md             # Slide type catalog and JSON schema
├── scripts/
│   ├── generate_deck.py           # CLI entry point + spec validation
│   ├── brand_engine.py            # Brand config loader + ThemeConfig builder
│   ├── slide_builder.py           # SlideBuilder class (high-level shape helpers)
│   ├── slide_renderers.py         # Per-slide-type render functions
│   ├── pptx_helpers.py            # Low-level shape/gradient/shadow helpers
│   └── refresh_site_style.py      # Website crawler to refresh visual cues
└── tests/
    ├── test_core.py               # Unit + integration tests
    └── test_ai_readiness.json     # Sample 8-slide e2e test spec
```

## Refreshing Website Styles

If the OpenTeams website has been updated, refresh the visual cues in `brand.json`:

```bash
~/.venvs/pptx/bin/python scripts/refresh_site_style.py \
  --url https://openteams.com/ \
  --brand-json references/brand.json
```

This re-crawls the site and updates `website_cues` in `brand.json` without touching immutable brand tokens (colors, typography, logo rules).
