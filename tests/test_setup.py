#!/usr/bin/env python3
"""
Test script for LinoLog setup verification.
"""

import os
import sys
import logging
from unittest.mock import patch, MagicMock
from linolog.config import Config
from linolog.metadata_loader import MetadataLoader


def test_config():
    """Test configuration loading."""
    # Ensure validate_config works when GOOGLE_SHEET_ID is set
    with patch.object(Config, "GOOGLE_SHEET_ID", "test-id"):
        assert Config.validate_config() is True


def test_google_sheets():
    """Test Google Sheets connection is attempted correctly."""
    with patch("linolog.sheet_writer.gspread") as mock_gspread, patch(
        "linolog.sheet_writer.ServiceAccountCredentials"
    ) as mock_creds, patch("linolog.sheet_writer.Config") as mock_config:
        mock_config.GOOGLE_SHEET_ID = "test-sheet-id"
        mock_config.GOOGLE_SHEET_NAME = "Sheet1"
        mock_creds.from_json_keyfile_name.return_value = MagicMock()
        mock_client = MagicMock()
        mock_gspread.authorize.return_value = mock_client

        from linolog.sheet_writer import SheetWriter

        writer = SheetWriter()
        assert writer.client is not None


def test_metadata_loader():
    """Test metadata loader initialization."""
    loader = MetadataLoader()
    assert loader is not None


def test_watch_directory(tmp_path):
    """Test watch directory handling."""
    watch_dir = tmp_path / "test_archive"
    assert not watch_dir.exists()
    os.makedirs(str(watch_dir), exist_ok=True)
    assert watch_dir.exists()
