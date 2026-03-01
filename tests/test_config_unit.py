"""Unit tests for Config."""

import pytest
from linolog.config import Config


class TestValidateConfig:
    def test_raises_when_google_sheet_id_missing(self, monkeypatch):
        monkeypatch.setattr(Config, "GOOGLE_SHEET_ID", None)
        with pytest.raises(ValueError, match="GOOGLE_SHEET_ID"):
            Config.validate_config()

    def test_passes_when_google_sheet_id_set(self, monkeypatch):
        monkeypatch.setattr(Config, "GOOGLE_SHEET_ID", "some-sheet-id")
        assert Config.validate_config() is True


class TestRequiredFields:
    def test_contains_expected_fields(self):
        assert "title" in Config.REQUIRED_FIELDS
        assert "date" in Config.REQUIRED_FIELDS
        assert "edition" in Config.REQUIRED_FIELDS
        assert "size" in Config.REQUIRED_FIELDS
        assert "medium" in Config.REQUIRED_FIELDS
        assert "paper_type" in Config.REQUIRED_FIELDS
        assert "blocks_used" in Config.REQUIRED_FIELDS

    def test_count(self):
        assert len(Config.REQUIRED_FIELDS) == 7


class TestSheetHeaders:
    def test_contains_expected_headers(self):
        assert "Title" in Config.SHEET_HEADERS
        assert "Date" in Config.SHEET_HEADERS
        assert "Colors Used" in Config.SHEET_HEADERS
        assert "Tags" in Config.SHEET_HEADERS

    def test_count(self):
        assert len(Config.SHEET_HEADERS) == 18
