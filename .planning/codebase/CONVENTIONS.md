# Code Conventions

## Python Style

- **Python 3.11+** with `from __future__ import annotations` in every file
- Type hints on function signatures (return types, parameter types)
- Dataclasses for config objects (`BrandConfig`, `ThemeConfig`)
- No class inheritance — flat class hierarchy
- `logging` module for output (not print), except in CLI `audit_brand.py`

## Import Style

```python
# Standard library first
from __future__ import annotations
import os
import json
import logging

# Third-party
from pptx import Presentation
from pptx.util import Inches, Pt
from lxml import etree

# Local
from pptx_helpers import hex_to_rgbcolor, set_shape_fill
from brand_engine import ThemeConfig
from slide_builder import SlideBuilder
```

- Explicit imports (no `from module import *`)
- Local imports use bare module names (enabled by `sys.path.insert` in entry point)

## Error Handling

- **Validation first:** `validate_spec()` catches all spec errors before rendering begins
- **Graceful degradation:** Missing PIL → hardcoded dimensions. Missing logo file → skip. Bad hex color → fallback to black with warning.
- **Try/except in renderers:** Individual slide rendering failures are caught and logged, don't crash the whole deck
- **sys.exit(1)** on fatal validation errors in CLI

```python
# Pattern: validate upfront, degrade gracefully at runtime
errors = validate_spec(spec)
if errors:
    sys.exit(1)

# In render loop:
try:
    renderer(sb, slide_spec)
except Exception as e:
    log.error(f"Slide {i} ({stype}): {e}")
```

## Logging

- `logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")`
- Module-level loggers: `log = logging.getLogger(__name__)`
- INFO for progress (`✓ Slide 1: cover`)
- WARNING for non-fatal issues (`Team slide: showing 6 of N members`)
- ERROR for failures with traceback

## Configuration Pattern

All brand/style values flow through `brand.json` → `BrandConfig` → `ThemeConfig`:

```python
# ✅ Correct — always use theme
color = sb.theme.night_navy
font = sb.theme.headline_font

# ❌ Never hardcode
color = "#022791"
font = "Inter Tight"
```

Exception: `"#FFFFFF"` and `"#000000"` are used directly for true white/black backgrounds.

## Renderer Pattern

Every slide renderer follows the same structure:

```python
def render_<type>(sb: SlideBuilder, spec: dict) -> None:
    """Docstring describing the slide."""
    slide = sb.new_slide()
    add_slide_bg_color(slide, "<color>")

    sb.add_logo(slide, "<variant>", "<position>", ...)

    # Extract fields from spec with defaults
    title = spec.get("title", "Default Title")

    # Build layout using sb.add_*() methods
    sb.add_title(slide, title, ...)
    sb.add_body(slide, ...)

    sb.add_footer(slide, show_logo=True)
```

## Commit Conventions

- Conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`
- No `Co-Authored-By` lines (per CLAUDE.md)
- Descriptive body for multi-file changes

## Documentation

- Docstrings on all modules, classes, and public functions
- `references/slide_types.md` documents the user-facing JSON schema
- `ARCHITECTURE.md` documents internal design
- `CLAUDE.md` provides AI assistant context
- `SKILL.md` defines the pi agent interface
