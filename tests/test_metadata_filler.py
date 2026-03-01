"""Unit tests for MetadataFillerAgent."""

from unittest.mock import patch
from linolog.agents.metadata_filler import MetadataFillerAgent


class TestExtractTitleFromFolder:
    def setup_method(self):
        self.agent = MetadataFillerAgent()

    def test_with_edition(self):
        result = self.agent._extract_title_from_folder(
            "/path/to/sunset_landscape_edition_3"
        )
        assert result == "Sunset Landscape"

    def test_without_edition(self):
        result = self.agent._extract_title_from_folder("/path/to/ocean_waves")
        assert result == "Ocean Waves"

    def test_single_word(self):
        result = self.agent._extract_title_from_folder("/path/to/abstract")
        assert result == "Abstract"


class TestExtractEditionFromFolder:
    def setup_method(self):
        self.agent = MetadataFillerAgent()

    def test_with_edition_pattern(self):
        result = self.agent._extract_edition_from_folder("/path/to/sunset_edition_5")
        assert result == "5"

    def test_no_edition_returns_default(self):
        result = self.agent._extract_edition_from_folder("/path/to/sunset")
        assert result == "1"


class TestSuggestSize:
    def setup_method(self):
        self.agent = MetadataFillerAgent()

    def test_dimension_in_name(self):
        result = self.agent._suggest_size("/path/to/print_8x10")
        assert result == "8x10"

    def test_no_dimension_returns_unknown(self):
        result = self.agent._suggest_size("/path/to/sunset_landscape")
        assert result == "Unknown"


class TestGetDefaultValue:
    def setup_method(self):
        self.agent = MetadataFillerAgent()

    def test_title(self):
        result = self.agent._get_default_value("title", {}, "/path/to/sunset_print")
        assert result == "Sunset Print"

    def test_edition(self):
        result = self.agent._get_default_value(
            "edition", {}, "/path/to/sunset_edition_3"
        )
        assert result == "3"

    def test_date(self):
        result = self.agent._get_default_value("date", {}, "/path/to/test")
        # Should return a date string in YYYY-MM-DD format
        assert len(result) == 10
        assert result[4] == "-"
        assert result[7] == "-"

    def test_size(self):
        result = self.agent._get_default_value("size", {}, "/path/to/print_8x10")
        assert result == "8x10"

    def test_medium(self):
        result = self.agent._get_default_value("medium", {}, "/path/to/test")
        assert result == "Battleship Grey"

    def test_paper_type(self):
        result = self.agent._get_default_value("paper_type", {}, "/path/to/test")
        assert result == "Unknown"

    def test_blocks_used(self):
        result = self.agent._get_default_value("blocks_used", {}, "/path/to/test")
        assert result == 1

    def test_unknown_field(self):
        result = self.agent._get_default_value("unknown_field", {}, "/path/to/test")
        assert result is None


class TestProcess:
    def setup_method(self):
        self.agent = MetadataFillerAgent()

    def test_fills_missing_fields(self, monkeypatch):
        monkeypatch.setattr(
            "linolog.agents.metadata_filler.Config.REQUIRED_FIELDS",
            ["title", "edition"],
        )
        metadata = {}
        result = self.agent.process(metadata, "/path/to/sunset_edition_3")
        assert result["title"] == "Sunset"
        assert result["edition"] == "3"

    def test_does_not_overwrite_existing(self, monkeypatch):
        monkeypatch.setattr(
            "linolog.agents.metadata_filler.Config.REQUIRED_FIELDS",
            ["title"],
        )
        metadata = {"title": "My Custom Title"}
        result = self.agent.process(metadata, "/path/to/sunset")
        assert result["title"] == "My Custom Title"

    def test_does_not_mutate_original(self, monkeypatch):
        monkeypatch.setattr(
            "linolog.agents.metadata_filler.Config.REQUIRED_FIELDS",
            ["title"],
        )
        metadata = {}
        self.agent.process(metadata, "/path/to/sunset")
        assert "title" not in metadata
