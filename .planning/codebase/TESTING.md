# Testing

## Framework

- **pytest** (installed in `~/.venvs/pptx/`, not in `requirements.txt`)
- Test file: `openteams-pptx/tests/test_core.py` (181 lines, 22 tests)
- No fixtures, no conftest.py — simple test classes

## Running Tests

```bash
~/.venvs/pptx/bin/python -m pytest openteams-pptx/tests/ -v
```

## Test Structure

Tests are organized into 4 classes:

### `TestHexToRGBColor` (4 tests)
Unit tests for `pptx_helpers.hex_to_rgbcolor()`:
- Valid hex with `#` prefix
- Valid hex without prefix
- Invalid input → fallback to black
- Empty string → fallback to black

### `TestColorUtilities` (4 tests)
Unit tests for `luminance()` and `contrast_ratio()`:
- White luminance ≈ 1.0
- Black luminance ≈ 0.0
- Black/white contrast ≈ 21:1
- Same-color contrast ≈ 1:1

### `TestAutoTextColor` (3 tests)
Unit tests for `auto_text_color()`:
- Dark background → white text
- Light background → black text
- Mid-tone → picks higher contrast option

### `TestValidateSpec` (8 tests)
Spec validation logic in `generate_deck.py`:
- Valid minimal spec passes
- Missing `slides` key → error
- Missing `type` field → error
- Unknown slide type → error
- Missing required field (e.g., `text` on `quote`) → error
- `DEMO_SPEC` passes validation
- `RENDERERS` keys match `REQUIRED_FIELDS` keys (registry consistency)
- `blank` slide requires no fields

### `TestGeneration` (3 tests)
Integration / smoke tests:
- Demo deck (all 10 slides) generates without error, file >10KB
- Single cover slide generates
- Team slide with 10 members (>6 cap) generates without crash

## Test Patterns

- Tests that need `brand.json` skip if file not found: `pytest.skip("brand.json not found")`
- Generated files use `tempfile.NamedTemporaryFile` and are cleaned up in `finally` blocks
- `BRAND_JSON` path resolved relative to test file location
- `sys.path.insert(0, SCRIPTS_DIR)` at top of test file for imports

## Coverage Gaps

The following areas are **not tested**:

| Area | Risk |
|------|------|
| Individual renderer output correctness | Medium — only smoke-tested (no crash), not visually verified |
| `SlideBuilder` methods in isolation | Low — exercised through renderer smoke tests |
| `brand_engine.py` loading/resolution | Low — exercised through generation tests |
| `refresh_site_style.py` crawler | Medium — no tests, requires network |
| `review/audit_brand.py` auditor | Low — standalone tool, used manually |
| Logo placement correctness | Medium — only tested indirectly |
| Gradient/shadow XML output | Medium — no unit tests on XML structure |
| Edge cases: empty items lists, very long text | Low-Medium — not tested |

## E2E Test Spec

`openteams-pptx/tests/test_ai_readiness.json` is a sample 8-slide spec for manual end-to-end testing. Not executed by pytest — used for ad-hoc verification.

## CI/CD

No CI pipeline exists. Tests are run manually before commits.
