"""Unit tests for tools_normalizer module."""

from linolog.tools_normalizer import (
    normalize_tools,
    _normalize_tools,
    _normalize_single_tool,
    get_known_tools,
    TOOL_STANDARDS,
)


class TestNormalizeSingleTool:
    def test_exact_match(self):
        standards = TOOL_STANDARDS["carving_tools"]
        assert _normalize_single_tool("pfiel", standards) == "pfeil"

    def test_case_insensitive_match(self):
        standards = TOOL_STANDARDS["carving_tools"]
        assert _normalize_single_tool("PFIEL", standards) == "pfeil"

    def test_no_match_returns_stripped(self):
        standards = TOOL_STANDARDS["carving_tools"]
        assert _normalize_single_tool("  unknown tool  ", standards) == "unknown tool"

    def test_empty_string(self):
        standards = TOOL_STANDARDS["carving_tools"]
        assert _normalize_single_tool("", standards) == ""

    def test_brayer_match(self):
        standards = TOOL_STANDARDS["brayer_type"]
        assert (
            _normalize_single_tool("speedball 4 inch", standards) == "speedball_4inch"
        )

    def test_burnish_match(self):
        standards = TOOL_STANDARDS["burnish_type"]
        assert _normalize_single_tool("wooden spatula", standards) == "wooden_spatula"

    def test_paper_match(self):
        standards = TOOL_STANDARDS["paper_type"]
        assert _normalize_single_tool("mulberry paper", standards) == "mulberry"


class TestNormalizeTools:
    def test_string_input(self):
        standards = TOOL_STANDARDS["carving_tools"]
        assert _normalize_tools("pfiel", standards) == "pfeil"

    def test_list_input(self):
        standards = TOOL_STANDARDS["carving_tools"]
        result = _normalize_tools(["pfiel", "flex cut"], standards)
        assert result == "pfeil, flexcut"

    def test_empty_value(self):
        standards = TOOL_STANDARDS["carving_tools"]
        assert _normalize_tools("", standards) == ""

    def test_none_returns_none(self):
        standards = TOOL_STANDARDS["carving_tools"]
        assert _normalize_tools(None, standards) is None


class TestNormalizeToolsMetadata:
    def test_normalizes_carving_tools(self):
        metadata = {"title": "Test", "carving_tools": "pfiel"}
        result = normalize_tools(metadata)
        assert result["carving_tools"] == "pfeil"

    def test_normalizes_brayer_type(self):
        metadata = {"brayer_type": "speedball 4 inch"}
        result = normalize_tools(metadata)
        assert result["brayer_type"] == "speedball_4inch"

    def test_normalizes_burnish_type(self):
        metadata = {"burnish_type": "wooden spatula"}
        result = normalize_tools(metadata)
        assert result["burnish_type"] == "wooden_spatula"

    def test_normalizes_paper_type(self):
        metadata = {"paper_type": "mulberry paper"}
        result = normalize_tools(metadata)
        assert result["paper_type"] == "mulberry"

    def test_no_matching_fields_unchanged(self):
        metadata = {"title": "Test", "date": "2025-01-01"}
        result = normalize_tools(metadata)
        assert result == metadata

    def test_does_not_mutate_original(self):
        metadata = {"carving_tools": "pfiel"}
        normalize_tools(metadata)
        assert metadata["carving_tools"] == "pfiel"

    def test_empty_field_skipped(self):
        metadata = {"carving_tools": ""}
        result = normalize_tools(metadata)
        assert result["carving_tools"] == ""


class TestGetKnownTools:
    def test_returns_all_categories(self):
        tools = get_known_tools()
        assert "carving_tools" in tools
        assert "brayer_type" in tools
        assert "burnish_type" in tools
        assert "paper_type" in tools

    def test_contains_standard_names(self):
        tools = get_known_tools()
        assert "pfeil" in tools["carving_tools"]
        assert "flexcut" in tools["carving_tools"]
        assert "baren" in tools["burnish_type"]
