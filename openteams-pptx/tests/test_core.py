"""
Core tests for the OpenTeams PPTX generator.
Covers: spec validation, color utilities, and smoke test for all renderers.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

import pytest

# Ensure scripts dir is importable
SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, SCRIPTS_DIR)

from pptx_helpers import (
    hex_to_rgbcolor, luminance, contrast_ratio, auto_text_color,
)
from generate_deck import validate_spec, DEMO_SPEC, generate

BRAND_JSON = os.path.join(os.path.dirname(__file__), "..", "references", "brand.json")


# ---------------------------------------------------------------------------
# hex_to_rgbcolor
# ---------------------------------------------------------------------------

class TestHexToRGBColor:
    def test_valid_hex_with_hash(self):
        c = hex_to_rgbcolor("#FF0000")
        assert str(c) == "FF0000"

    def test_valid_hex_without_hash(self):
        c = hex_to_rgbcolor("00FF00")
        assert str(c) == "00FF00"

    def test_invalid_hex_falls_back_to_black(self):
        c = hex_to_rgbcolor("not-a-color")
        assert str(c) == "000000"

    def test_empty_string_falls_back_to_black(self):
        c = hex_to_rgbcolor("")
        assert str(c) == "000000"


# ---------------------------------------------------------------------------
# luminance & contrast_ratio
# ---------------------------------------------------------------------------

class TestColorUtilities:
    def test_white_luminance(self):
        assert luminance("#FFFFFF") == pytest.approx(1.0, abs=0.01)

    def test_black_luminance(self):
        assert luminance("#000000") == pytest.approx(0.0, abs=0.01)

    def test_contrast_ratio_black_white(self):
        cr = contrast_ratio("#000000", "#FFFFFF")
        assert cr == pytest.approx(21.0, abs=0.1)

    def test_contrast_ratio_same_color(self):
        cr = contrast_ratio("#4D75FE", "#4D75FE")
        assert cr == pytest.approx(1.0, abs=0.01)


# ---------------------------------------------------------------------------
# auto_text_color
# ---------------------------------------------------------------------------

class TestAutoTextColor:
    def test_dark_bg_gets_white_text(self):
        assert auto_text_color("#022791") == "#FFFFFF"

    def test_light_bg_gets_black_text(self):
        assert auto_text_color("#FFFFFF") == "#000000"

    def test_mid_tone_picks_higher_contrast(self):
        result = auto_text_color("#808080")
        assert result in ("#FFFFFF", "#000000")


# ---------------------------------------------------------------------------
# validate_spec
# ---------------------------------------------------------------------------

class TestValidateSpec:
    def test_valid_minimal_spec(self):
        spec = {"slides": [{"type": "cover", "title": "Hello"}]}
        assert validate_spec(spec) == []

    def test_missing_slides_key(self):
        errors = validate_spec({})
        assert len(errors) == 1
        assert "slides" in errors[0].lower()

    def test_missing_type_field(self):
        spec = {"slides": [{"title": "No type"}]}
        errors = validate_spec(spec)
        assert any("type" in e.lower() for e in errors)

    def test_unknown_type(self):
        spec = {"slides": [{"type": "unicorn"}]}
        errors = validate_spec(spec)
        assert any("unknown" in e.lower() for e in errors)

    def test_missing_required_field(self):
        spec = {"slides": [{"type": "quote"}]}  # missing "text"
        errors = validate_spec(spec)
        assert any("text" in e for e in errors)

    def test_demo_spec_is_valid(self):
        assert validate_spec(DEMO_SPEC) == []

    def test_all_slide_types_have_validation(self):
        from generate_deck import REQUIRED_FIELDS
        from slide_renderers import RENDERERS
        assert set(REQUIRED_FIELDS.keys()) == set(RENDERERS.keys())

    def test_blank_slide_no_required_fields(self):
        spec = {"slides": [{"type": "blank"}]}
        assert validate_spec(spec) == []


# ---------------------------------------------------------------------------
# Smoke test: generate demo deck without errors
# ---------------------------------------------------------------------------

class TestGeneration:
    def test_demo_deck_generates(self):
        """All 11 slide types render without crashing."""
        if not os.path.exists(BRAND_JSON):
            pytest.skip("brand.json not found")

        with tempfile.NamedTemporaryFile(suffix=".pptx", delete=False) as f:
            out_path = f.name

        try:
            generate(DEMO_SPEC, BRAND_JSON, out_path)
            assert os.path.exists(out_path)
            assert os.path.getsize(out_path) > 10_000  # sanity: file isn't empty
        finally:
            os.unlink(out_path)

    def test_single_cover_slide(self):
        """Minimal single-slide deck generates."""
        if not os.path.exists(BRAND_JSON):
            pytest.skip("brand.json not found")

        spec = {"slides": [{"type": "cover", "title": "Test"}]}
        with tempfile.NamedTemporaryFile(suffix=".pptx", delete=False) as f:
            out_path = f.name

        try:
            generate(spec, BRAND_JSON, out_path)
            assert os.path.exists(out_path)
        finally:
            os.unlink(out_path)

    def test_team_slide_with_many_members(self):
        """Team slide with >6 members doesn't crash (truncates with warning)."""
        if not os.path.exists(BRAND_JSON):
            pytest.skip("brand.json not found")

        spec = {"slides": [{
            "type": "team",
            "title": "Big Team",
            "members": [
                {"name": f"Person {i}", "role": "Role", "bio": "Bio"}
                for i in range(10)
            ]
        }]}
        with tempfile.NamedTemporaryFile(suffix=".pptx", delete=False) as f:
            out_path = f.name

        try:
            generate(spec, BRAND_JSON, out_path)
            assert os.path.exists(out_path)
        finally:
            os.unlink(out_path)
