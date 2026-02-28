# Phase 1: Self-Contained Skill — Research

**Researched:** 2026-02-28
**Question:** What do we need to know to plan making openteams-pptx self-contained?

## Current State Analysis

### Symlink Problem
- `openteams-pptx/assets/logos` is a **symlink** → `../../Assets`
- This means the skill directory is not portable — copying it elsewhere breaks logo resolution
- The symlink resolves through the large `Assets/` tree (AI files, PDFs, email logos, etc.) but only 6 PNGs are actually used

### Logo Files Actually Used (from brand.json `logo_assets`)
| Key | Relative Path | Size |
|-----|--------------|------|
| `colored_horizontal_png` | `assets/logos/OT_Colored_Logos/Colored-Horizontal-transparent-logo/OT-new-logo-final.png` | 32K |
| `colored_vertical_png` | `assets/logos/OT_Colored_Logos/Colored-vertical-transparent-logo/OT-new-logo-vertical-lockup.png` | 20K |
| `white_horizontal_png` | `assets/logos/OT_White_Logos/White-Horizontal-transparent-logo/OT-new-logo-final-white-horizontal-lockup.png` | 28K |
| `black_horizontal_png` | `assets/logos/OT_Black_Logos/Black-Horizontal-transparent/OpenTeams_logo_horizontal_lockup_black.png` | 12K |
| `favicon_colored_png` | `assets/logos/OT_Colored_Logos/Favicon-transparent-background/OpenTeams-favicon-01.png` | 88K |
| `favicon_white_png` | `assets/logos/OT_White_Logos/White-Horizontal-transparent-logo/OT-new-logo-final-white-favicon.png` | 20K |

**Total: ~200KB** — trivial to bundle directly.

### Absolute Path References (in SKILL.md)
6 occurrences of `/home/mia/.venvs/pptx/bin/python` in SKILL.md:
- Lines 59, 124, 132, 140, 145, 152
- Also references `/home/mia/dev/ppt/openteams-pptx` as an example skill-dir path (line 145)

### Scripts — Already Portable
- `generate_deck.py` uses `argparse` with `--brand` and `--out` — no hardcoded paths
- `brand_engine.py` resolves logo paths relative to `skill_dir` (derived from brand.json location) — already correct
- `slide_builder.py`, `slide_renderers.py`, `pptx_helpers.py` — no path issues found
- `refresh_site_style.py` — no hardcoded paths in the script itself, only in SKILL.md usage examples

### brand.json Logo Paths
The `logo_assets` section uses **relative paths** like `assets/logos/OT_Colored_Logos/...`. These are resolved by `brand_engine.py` at runtime using the skill directory. The paths work today through the symlink.

**Key insight:** If we flatten the logo directory structure, we need to update BOTH:
1. The actual file locations in `assets/logos/`
2. The `logo_assets` paths in `brand.json`

## Approach Options

### Option A: Flatten to 6 PNGs in `assets/logos/`
- Remove symlink, create real `assets/logos/` directory
- Copy 6 PNGs directly with clean names (e.g., `logo-colored-horizontal.png`)
- Update `brand.json` paths to `assets/logos/logo-colored-horizontal.png`
- **Pros:** Simplest structure, smallest footprint, clearest naming
- **Cons:** Loses original directory structure (but originals remain in `Assets/`)

### Option B: Preserve subdirectory structure
- Remove symlink, recreate only the needed subdirectory branches
- Copy 6 PNGs into their original subdirectory paths
- `brand.json` paths stay the same
- **Pros:** No brand.json changes needed
- **Cons:** Deep nested directories for 6 files seems wasteful

**Recommendation:** Option A — flatten. The directory structure in Assets/ is for organizing a large brand package. Inside a portable skill, flat is better. The brand.json update is trivial.

## Implementation Steps

1. **Remove symlink** `openteams-pptx/assets/logos`
2. **Create real directory** `openteams-pptx/assets/logos/`
3. **Copy 6 PNGs** from `Assets/` with clean names
4. **Update `brand.json`** `logo_assets` to point to flattened paths
5. **Update `SKILL.md`** — replace all `/home/mia/.venvs/pptx/bin/python` with `python3`, remove hardcoded skill-dir example
6. **Scan all files** for any remaining absolute paths
7. **Test** — run `generate_deck.py --demo` and verify output

## Risks & Edge Cases

- **`__pycache__` dirs**: Should be in `.gitignore`, not an issue for portability
- **`refresh_site_style.py`**: Requires `requests` + `beautifulsoup4` — separate concern from core generation, but SKILL.md usage examples need path fixes too
- **Python dependency**: `python-pptx` must be installed. The skill can't control this, but SKILL.md should say `python3` not a venv path
- **Font availability**: Inter Tight / Roboto must be installed on the machine — not a phase 1 concern but worth noting

## Validation Architecture

### Dimension 1: File Structure
- `assets/logos/` is a real directory (not a symlink)
- Contains exactly 6 PNG files

### Dimension 2: Path Integrity
- Every path in `brand.json` `logo_assets` resolves to a real file when joined with the skill directory
- No file in the skill tree contains `/home/mia/` or any absolute home directory path

### Dimension 3: Functional Test
- `python3 generate_deck.py --demo --brand ../references/brand.json --out /tmp/test.pptx` succeeds
- Output file is a valid .pptx (non-zero, openable)

---
*Research completed: 2026-02-28*
