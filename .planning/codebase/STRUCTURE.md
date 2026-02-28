# Directory Structure

## Top Level

```
ppt/                                       # Repository root
├── README.md                              # Repo overview
├── CLAUDE.md                              # AI assistant guidance (project context)
├── .gitignore                             # macOS files, Office temp files, __pycache__
├── requirements.txt                       # Python dependencies (5 packages)
├── OpenTeams_Brand_Guidelines_2025.pdf    # Official brand guidelines (36MB)
├── assets_index.json                      # Machine-readable index of all logo paths
├── site_style.json                        # Website CSS tokens (scraped)
├── build_template.py                      # DEPRECATED — legacy monolithic builder (1559 lines)
│
├── Assets/                                # Logo files — all formats and variants
│   ├── OT_Colored_Logos/                  # Full-color (horizontal, vertical, favicon)
│   │   ├── Colored-Horizontal-transparent-logo/
│   │   ├── Colored-vertical-transparent-logo/
│   │   ├── Favicon-transparent-background/
│   │   └── ... (SVG, white-bg variants)
│   ├── OT_White_Logos/                    # White variants for dark backgrounds
│   ├── OT_Black_Logos/                    # Black variants for light backgrounds
│   ├── OT_ai_Logos/                       # Adobe Illustrator source files
│   ├── Email signature OT logo/           # Email-sized logos
│   └── Horizontal-PDF-logo/              # PDF format
│
├── openteams-pptx/                        # Main skill — modular PPTX generator
│   ├── SKILL.md                           # Pi agent skill definition
│   ├── README.md                          # User-facing documentation
│   ├── .gitignore
│   ├── assets/
│   │   └── logos -> ../../Assets          # Symlink to root Assets/
│   ├── references/
│   │   ├── brand.json                     # Brand tokens (99 lines)
│   │   └── slide_types.md                 # Slide type catalog (231 lines)
│   ├── scripts/
│   │   ├── generate_deck.py               # CLI entry point (246 lines)
│   │   ├── brand_engine.py                # Config loader (214 lines)
│   │   ├── slide_builder.py               # SlideBuilder class (378 lines)
│   │   ├── slide_renderers.py             # 11 render functions (518 lines)
│   │   ├── pptx_helpers.py                # Low-level XML helpers (188 lines)
│   │   └── refresh_site_style.py          # Website crawler (179 lines)
│   ├── tests/
│   │   ├── test_core.py                   # 22 tests (181 lines)
│   │   └── test_ai_readiness.json         # Sample 8-slide e2e spec
│   └── docs/
│       └── ARCHITECTURE.md                # System design doc
│
├── review/                                # Brand compliance audit
│   ├── COMPLIANCE_REPORT.md               # Audit findings
│   └── audit_brand.py                     # Automated PPTX brand checker (131 lines)
│
├── docs/plans/                            # Implementation plans (historical)
│   ├── 2026-02-28-openteams-pptx-skill.md
│   ├── 2026-02-28-folder-cleanup.md
│   ├── 2026-02-28-pptx-brand-compliance-review.md
│   └── 2026-02-28-fix-cover-decorative-dots.md
│
└── .planning/                             # GSD planning directory
    └── codebase/                          # This codebase map
```

## Key Locations

| What | Where |
|------|-------|
| Brand config (colors, fonts, logos) | `openteams-pptx/references/brand.json` |
| Slide type schemas | `openteams-pptx/references/slide_types.md` |
| Main generation script | `openteams-pptx/scripts/generate_deck.py` |
| Slide rendering logic | `openteams-pptx/scripts/slide_renderers.py` |
| Shape builder helpers | `openteams-pptx/scripts/slide_builder.py` |
| Low-level XML helpers | `openteams-pptx/scripts/pptx_helpers.py` |
| Logo files | `Assets/` (accessed via symlink at `openteams-pptx/assets/logos`) |
| Tests | `openteams-pptx/tests/test_core.py` |
| Brand audit tool | `review/audit_brand.py` |
| Agent skill definition | `openteams-pptx/SKILL.md` |

## Naming Conventions

- **Python files:** `snake_case.py`
- **Classes:** `PascalCase` (`SlideBuilder`, `BrandConfig`, `ThemeConfig`)
- **Functions:** `snake_case` (`render_cover`, `add_title`, `hex_to_rgbcolor`)
- **Render functions:** `render_<slide_type>` pattern — matches the JSON `type` field
- **Constants:** `UPPER_SNAKE` (`RENDERERS`, `REQUIRED_FIELDS`, `DEMO_SPEC`, `_CURRENT_YEAR`)
- **Brand JSON keys:** `snake_case` (`night_navy`, `day_blue`, `headline_font`)
- **Directories:** lowercase with hyphens (`openteams-pptx`, `OT_Colored_Logos`)

## Code Size

Total Python: ~1,723 lines across 6 active modules + 1 test file + 1 audit script.
Legacy `build_template.py` is 1,559 lines but deprecated.
