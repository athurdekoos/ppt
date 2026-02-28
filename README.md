# OpenTeams Brand Assets & Presentation Toolkit

Brand assets, logo files, and an automated PowerPoint generator for OpenTeams.

## What's Here

### 📊 PPTX Generator (`openteams-pptx/`)

A pi agent skill that generates on-brand PowerPoint presentations from natural language. Ask Claude to create a deck and it handles content structure, slide layout, brand compliance, and `.pptx` output.

**Quick example:**
> "Create a 10-slide pitch deck for IBM about our open source platform"

→ Produces a branded `.pptx` with cover, agenda, content slides, metrics, case study, and closing.

See [`openteams-pptx/README.md`](openteams-pptx/README.md) for full usage, slide types, and CLI docs.

### 🎨 Brand Assets (`Assets/`)

Official OpenTeams logo files in multiple formats and variants:

| Directory | Contents |
|-----------|----------|
| `OT_Colored_Logos/` | Full-color logos (horizontal, vertical, favicon) — PNG, JPG, SVG |
| `OT_White_Logos/` | White logos for dark backgrounds — AI, SVG, PNG |
| `OT_Black_Logos/` | Black logos for light backgrounds — AI, SVG, PNG |
| `OT_ai_Logos/` | Adobe Illustrator source files |
| `Email signature OT logo/` | Sized for email signatures (with/without tagline) |
| `Horizontal-PDF-logo/` | PDF format horizontal logo |

Each variant is available in horizontal and vertical lockups, plus favicon.

### 📋 Brand Guidelines

- [`OpenTeams_Brand_Guidelines_2025.pdf`](OpenTeams_Brand_Guidelines_2025.pdf) — Official 36-page brand guidelines document

### 📝 Brand Compliance Review (`review/`)

- Mock deck and compliance audit report from brand review process

## Key Config Files

| File | Purpose |
|------|---------|
| [`assets_index.json`](assets_index.json) | Machine-readable index of all logo asset paths |
| [`site_style.json`](site_style.json) | Website style tokens scraped from openteams.com |
| [`openteams-pptx/references/brand.json`](openteams-pptx/references/brand.json) | Brand tokens for slide generation (colors, fonts, spacing, logos) |

## Repository Structure

```
ppt/
├── README.md                              # This file
├── CLAUDE.md                              # AI assistant guidance
├── OpenTeams_Brand_Guidelines_2025.pdf    # Official brand guidelines
├── assets_index.json                      # Logo asset index
├── site_style.json                        # Website style tokens
├── requirements.txt                       # Python dependencies
│
├── Assets/                                # Logo files (all formats/variants)
│   ├── OT_Colored_Logos/
│   ├── OT_White_Logos/
│   ├── OT_Black_Logos/
│   ├── OT_ai_Logos/
│   ├── Email signature OT logo/
│   └── Horizontal-PDF-logo/
│
├── openteams-pptx/                        # PPTX generator skill
│   ├── README.md                          # Skill documentation
│   ├── SKILL.md                           # Pi agent skill definition
│   ├── docs/
│   │   ├── ARCHITECTURE.md                # System design & data flow
│   │   └── CONTRIBUTING.md                # How to add slide types
│   ├── references/
│   │   ├── brand.json                     # Brand tokens
│   │   └── slide_types.md                 # Slide type catalog & schema
│   ├── scripts/                           # Python source (6 modules, ~1700 LOC)
│   └── tests/                             # Unit + integration tests
│
├── review/                                # Brand compliance audit
│   └── COMPLIANCE_REPORT.md
│
└── docs/plans/                            # Implementation plans
```

## Getting Started

### For Presentations (via Claude)

Just ask Claude to make a presentation. The skill triggers automatically on keywords like "slides", "deck", "presentation", or "powerpoint".

### For Presentations (CLI)

```bash
# Setup
python -m venv ~/.venvs/pptx
~/.venvs/pptx/bin/pip install -r requirements.txt

# Generate demo deck
~/.venvs/pptx/bin/python openteams-pptx/scripts/generate_deck.py \
  --demo \
  --brand openteams-pptx/references/brand.json \
  --out demo.pptx
```

### For Logo Assets

Browse `Assets/` for the variant you need. Use [`assets_index.json`](assets_index.json) for programmatic access. Follow the brand guidelines PDF for usage rules.
