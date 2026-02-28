# Technology Stack

## Language & Runtime

- **Python 3.11+** — all scripts target 3.11+ (uses `list[str]` type hints via `from __future__ import annotations`)
- Runtime: CPython via virtual environment at `~/.venvs/pptx/`
- No async code — everything is synchronous

## Core Dependencies

Defined in `requirements.txt` (5 packages):

| Package | Version | Purpose |
|---------|---------|---------|
| `python-pptx` | >=1.0.0,<2.0.0 | PowerPoint file generation — the core library |
| `Pillow` | >=10.0.0,<12.0.0 | Image dimension detection for logo sizing |
| `lxml` | >=4.9.0,<6.0.0 | XML manipulation for gradients, shadows, transparency |
| `requests` | >=2.28.0,<3.0.0 | HTTP client for website style crawling |
| `beautifulsoup4` | >=4.12.0,<5.0.0 | HTML/CSS parsing for style extraction |

Dev dependency (not in requirements.txt): `pytest` for testing.

## Key Libraries Usage

### python-pptx
- `Presentation` object created from scratch (no template file)
- Uses blank slide layout (#6) exclusively — all elements built programmatically
- Shapes added via `slide.shapes.add_shape()`, `add_textbox()`, `add_picture()`
- `Inches()`, `Pt()`, `Emu()` for unit conversion
- **Limitation:** No native API for gradients, transparency, or custom corner radii — these are done via direct XML manipulation with `lxml`

### lxml
- Used heavily in `pptx_helpers.py` for features python-pptx doesn't expose:
  - Gradient fills (`gradFill` XML elements)
  - Shape transparency (`alpha` elements)
  - Rounded rectangle corner radius (`avLst/gd` elements)
  - Card shadows (`effectLst/outerShdw` elements)
- Accesses shape internals via `shape._element` (private API)

### Pillow
- Used only in `SlideBuilder.add_logo()` to get natural image dimensions
- Graceful fallback to hardcoded 1841×483 if PIL unavailable

## Configuration

- **Brand tokens:** `openteams-pptx/references/brand.json` — colors, fonts, spacing, logo paths, card/button styles
- **Slide schemas:** `openteams-pptx/references/slide_types.md` — markdown documentation of all 11 slide types
- **Website styles:** `site_style.json` (root) — scraped CSS tokens from openteams.com

## Build & Run

No build step. Direct script execution:

```bash
~/.venvs/pptx/bin/python openteams-pptx/scripts/generate_deck.py --demo --brand openteams-pptx/references/brand.json --out demo.pptx
```

## Environment

- Virtual environment: `~/.venvs/pptx/`
- `sys.path.insert(0, ...)` in `generate_deck.py` ensures same-directory imports work when invoked as a script
- Logo assets accessed via symlink: `openteams-pptx/assets/logos -> ../../Assets`
