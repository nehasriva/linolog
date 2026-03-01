"""Unit tests for PrintProcessor."""

from unittest.mock import patch, MagicMock
from linolog.processor import PrintProcessor
from linolog.config import Config


def _create_processor():
    """Create a PrintProcessor with mocked external dependencies."""
    with patch("linolog.processor.SheetWriter"), patch(
        "linolog.processor.MetadataLoader"
    ):
        return PrintProcessor()


class TestValidateMetadata:
    def setup_method(self):
        self.processor = _create_processor()

    def test_all_present(self):
        metadata = {field: "value" for field in Config.REQUIRED_FIELDS}
        result = self.processor._validate_metadata(metadata)
        assert result == []

    def test_missing_fields(self):
        metadata = {"title": "Test"}
        result = self.processor._validate_metadata(metadata)
        assert "date" in result
        assert "edition" in result

    def test_empty_values_count_as_missing(self):
        metadata = {"title": "", "date": "2025-01-01"}
        result = self.processor._validate_metadata(metadata)
        assert "title" in result

    def test_none_values_count_as_missing(self):
        metadata = {"title": None}
        result = self.processor._validate_metadata(metadata)
        assert "title" in result


class TestGetDefaultValue:
    def setup_method(self):
        self.processor = _create_processor()

    def test_title(self):
        assert self.processor._get_default_value("title", {}) == "Unknown Print"

    def test_date(self):
        assert self.processor._get_default_value("date", {}) == "2025-01-01"

    def test_edition(self):
        assert self.processor._get_default_value("edition", {}) == "1"

    def test_size(self):
        assert self.processor._get_default_value("size", {}) == "Unknown"

    def test_medium(self):
        assert self.processor._get_default_value("medium", {}) == "Linocut"

    def test_paper_type(self):
        assert self.processor._get_default_value("paper_type", {}) == "Unknown"

    def test_blocks_used(self):
        assert self.processor._get_default_value("blocks_used", {}) == "1"

    def test_unknown_field(self):
        assert self.processor._get_default_value("unknown", {}) == "Unknown"


class TestGetDisplayName:
    def setup_method(self):
        self.processor = _create_processor()

    def test_known_fields(self):
        assert self.processor._get_display_name("title") == "Title"
        assert self.processor._get_display_name("paper_type") == "Paper Type"
        assert self.processor._get_display_name("carving_tools") == "Carving Tools"
        assert self.processor._get_display_name("brayer_type") == "Brayer Type"

    def test_unknown_field_returns_raw_name(self):
        assert self.processor._get_display_name("unknown_field") == "unknown_field"


class TestGetProcessingStats:
    def setup_method(self):
        self.processor = _create_processor()

    def test_returns_expected_keys(self):
        stats = self.processor.get_processing_stats()
        assert "processed_folders" in stats
        assert "enabled_agents" in stats
        assert "total_agents" in stats

    def test_initial_state(self):
        self.processor.processed_folders = set()
        stats = self.processor.get_processing_stats()
        assert stats["processed_folders"] == 0


class TestSetupAgents:
    def test_agents_initialized(self):
        processor = _create_processor()
        assert isinstance(processor.agents, list)

    def test_no_llm_agents_when_disabled(self, monkeypatch):
        monkeypatch.setattr("linolog.processor.Config.ENABLE_LLM", False)
        processor = _create_processor()
        agent_names = [a.__class__.__name__ for a in processor.agents]
        assert "LLMColorAgent" not in agent_names
        assert "LLMTagAgent" not in agent_names


class TestProcessFolder:
    def setup_method(self):
        self.processor = _create_processor()

    def test_already_processed_skips(self):
        self.processor.processed_folders.add("/path/to/folder")
        # Should return without calling any agents or sheet_writer
        self.processor.process_folder("/path/to/folder")
        self.processor.sheet_writer.add_print_record.assert_not_called()
