# Concerns & Technical Debt

## High Priority

### 1. Deprecated Legacy File Still in Repo
**File:** `build_template.py` (1,559 lines)
**Issue:** Marked deprecated but still present. Larger than the entire modular codebase it was replaced by. Could confuse contributors or be accidentally invoked.
**Recommendation:** Delete it or move to a `legacy/` branch.

### 2. No CI/CD Pipeline
**Issue:** Tests exist but are only run manually. No GitHub Actions, no pre-commit hooks. Easy to push broken code.
**Recommendation:** Add a simple GitHub Actions workflow: install deps, run pytest.

### 3. Emoji Rendering in PowerPoint
**Files:** `slide_renderers.py` — `render_team()` uses `👤`, `render_case_study()` uses `⚡🔧📈`
**Issue:** Emoji in PowerPoint text frames depend on system fonts. On systems without emoji fonts (common in enterprise/Windows Server), these render as empty squares.
**Recommendation:** Replace emoji with text initials (first letter of name) or colored shape icons.

## Medium Priority

### 4. Private API Usage (`shape._element`)
**Files:** `pptx_helpers.py`, `slide_builder.py`
**Issue:** Accessing `shape._element` to manipulate XML directly. This is a private API in python-pptx that could break in future versions.
**Mitigation:** Version-pinned to `<2.0.0`. Monitor python-pptx releases.

### 5. `sys.path` Manipulation
**File:** `generate_deck.py:19`
**Issue:** `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))` modifies Python's import path at runtime. Could shadow stdlib modules if a script file had a conflicting name.
**Risk:** Low — current filenames don't conflict. But fragile.
**Alternative:** Convert to a proper Python package with `__init__.py` and `pyproject.toml`.

### 6. Test Coverage Gaps
**File:** `openteams-pptx/tests/test_core.py`
**Issue:** Renderers are only smoke-tested (no crash). No tests verify:
- Correct colors/fonts in output
- Logo placement positions
- Gradient XML structure
- Card shadow parameters
**Recommendation:** Add a few structural tests that inspect the generated slide XML.

### 7. Hardcoded Virtual Environment Path
**Files:** `SKILL.md`, `README.md`
**Issue:** All docs reference `~/.venvs/pptx/bin/python`. Not portable to other developers/machines.
**Recommendation:** Use `python -m` or document venv setup more generically.

## Low Priority

### 8. `hex_to_rgbcolor` Fallback Fragility
**File:** `pptx_helpers.py:29-33`
**Issue:** When input is invalid, sets `hex_val = _FALLBACK_COLOR` then lstrips `#`. Works because fallback is well-formed, but if `_FALLBACK_COLOR` were ever changed to something invalid, it would silently produce wrong colors.
**Recommendation:** Return `RGBColor(0, 0, 0)` directly on fallback instead of re-parsing.

### 9. Team Member Silent Truncation
**File:** `slide_renderers.py` — `render_team()`
**Issue:** Caps at 6 members. Now logs a warning (recently added), but the user-facing spec doesn't document this limit.
**Recommendation:** Add max member count to `references/slide_types.md`.

### 10. Website Crawler Inline CSS Unbounded
**File:** `refresh_site_style.py:79`
**Issue:** External CSS is capped at 200KB, but inline `<style>` tags are parsed without size limit. Not exploitable in practice (requests has timeouts), but inconsistent.
**Recommendation:** Add `[:200_000]` to inline style text too.

### 11. No Package Structure
**Issue:** Scripts directory uses `sys.path` hacks instead of being a proper Python package. No `__init__.py`, no `setup.py`/`pyproject.toml`.
**Impact:** Can't `pip install` the tool. Can't import from other projects.
**Recommendation:** Low priority — current CLI usage is fine. Convert if reuse grows.

## Security Notes

- **No secrets in codebase** ✅
- **SSRF protection** in crawler via `_is_same_origin()` ✅
- **No user input passed to shell** ✅
- **No network calls during deck generation** ✅ (crawler is separate, manual-only)
- **Logo paths validated with `os.path.exists()`** before loading ✅
