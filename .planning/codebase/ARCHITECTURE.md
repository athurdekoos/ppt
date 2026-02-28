# Architecture

## Pattern

**Pipeline architecture** with clear data flow:

```
brand.json → BrandConfig → ThemeConfig → SlideBuilder → Renderers → .pptx
```

No framework, no dependency injection, no event system. Simple procedural Python with dataclasses for config.

## Layers

### 1. Configuration Layer (`brand_engine.py`, 214 lines)

Loads `brand.json` and produces typed config objects.

- `BrandConfig` — raw brand tokens as dicts (colors, typography, spacing, logos, etc.)
- `ThemeConfig` — resolved runtime values (hex strings, font names, absolute paths, computed styles)
- `load_brand(path)` → `BrandConfig` — reads JSON, resolves relative logo paths to absolute
- `build_theme(brand)` → `ThemeConfig` — maps raw tokens to typed fields

**Key detail:** Logo paths in `brand.json` are relative to skill directory. `load_brand()` resolves them using `Path(brand_json_path).resolve().parent.parent` as the skill root.

### 2. Low-Level Helpers (`pptx_helpers.py`, 188 lines)

XML-level operations that `python-pptx` doesn't natively support:

- Color utilities: `hex_to_rgbcolor()`, `luminance()`, `contrast_ratio()`, `auto_text_color()`
- Shape manipulation: `set_shape_fill()`, `set_no_border()`, `set_shape_rounded_rect_radius()`
- Advanced rendering: `make_gradient_rect()`, `set_shape_alpha()`
- Slide background: `add_slide_bg_color()`
- XML access: `get_spPr()` — finds spPr element across p: and a: namespaces

### 3. High-Level Builder (`slide_builder.py`, 378 lines)

`SlideBuilder` class wrapping `Presentation` + `ThemeConfig`:

- All methods enforce brand rules (colors from theme, fonts from theme)
- Provides: `add_title()`, `add_body()`, `add_card()`, `add_button()`, `add_logo()`, `add_footer()`, `add_metric_card()`, etc.
- `ACCENT_ROTATION` — canonical color cycle `[day_blue, night_navy, yellow, salmon]`
- Renderers call SlideBuilder methods, never raw python-pptx APIs

### 4. Renderers (`slide_renderers.py`, 518 lines)

One function per slide type, all with signature `render_<type>(sb: SlideBuilder, spec: dict) -> None`:

- 11 renderers: `cover`, `section_divider`, `agenda`, `content`, `two_column`, `quote`, `metrics`, `team`, `case_study`, `closing`, `blank`
- `RENDERERS` dict maps type strings to functions
- Each creates one slide, adds shapes via `SlideBuilder`

### 5. CLI Entry Point (`generate_deck.py`, 246 lines)

- Argument parsing (`--spec`, `--demo`, `--brand`, `--out`, stdin pipe)
- `validate_spec()` — checks required fields per slide type before rendering
- `DEMO_SPEC` — built-in 10-slide spec for `--demo` mode
- `generate()` — orchestrates: validate → load brand → build theme → create presentation → render slides → save

## Data Flow

```
User JSON spec ──→ validate_spec() ──→ spec dict
                                          │
brand.json ──→ load_brand() ──→ BrandConfig ──→ build_theme() ──→ ThemeConfig
                                                                       │
                                          ┌────────────────────────────┘
                                          ▼
                              SlideBuilder(Presentation, ThemeConfig)
                                          │
                    For each slide in spec:│
                                          ▼
                              RENDERERS[type](sb, slide_spec)
                                          │
                                          ▼
                              Presentation.save("output.pptx")
```

## Entry Points

| Entry Point | File | Invocation |
|-------------|------|-----------|
| Deck generation | `openteams-pptx/scripts/generate_deck.py` | `python generate_deck.py --spec X --brand Y --out Z` |
| Website style refresh | `openteams-pptx/scripts/refresh_site_style.py` | `python refresh_site_style.py --url U --brand-json B` |
| Brand compliance audit | `review/audit_brand.py` | `python audit_brand.py <file.pptx>` |
| Legacy builder (deprecated) | `build_template.py` | Deprecated — kept for reference only |

## Key Abstractions

1. **SlideBuilder as facade** — renderers never touch python-pptx or XML directly
2. **ThemeConfig as single source** — no hardcoded colors/fonts in renderers
3. **JSON spec as intermediate** — decouples content authoring from rendering
4. **RENDERERS registry** — adding a slide type = one function + one dict entry
