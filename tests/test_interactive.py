#!/usr/bin/env python3
"""
Test script to demonstrate interactive metadata prompting.
"""

import os
import sys
import tempfile
from unittest.mock import patch
from linolog.processor import PrintProcessor
from linolog.config import Config


def test_interactive_metadata():
    """Test interactive metadata prompting."""
    print("🧪 Testing Interactive Metadata Prompting")
    print("=" * 50)

    # Create a temporary test folder
    test_folder = tempfile.mkdtemp(prefix="linolog_test_interactive_")

    # Create a metadata file with some missing fields (to test defaults)
    metadata_content = """
# Some fields missing - should use defaults when pressing Enter
title: "Test Print"
edition: "5"
# Missing: date, size, medium, paper_type, blocks_used
"""

    with open(os.path.join(test_folder, "metadata.yaml"), "w") as f:
        f.write(metadata_content)

    print(f"📁 Created test folder: {test_folder}")

    # Initialize processor with mocked external dependencies
    with patch("linolog.processor.SheetWriter"), patch(
        "linolog.processor.MetadataLoader"
    ):
        processor = PrintProcessor()

    print("\n✅ Test completed!")


if __name__ == "__main__":
    test_interactive_metadata()
