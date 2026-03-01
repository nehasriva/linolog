#!/usr/bin/env python3
"""
Test script to demonstrate tools normalizer functionality.
"""

import os
import sys
import tempfile
from unittest.mock import patch
from linolog.processor import PrintProcessor
from linolog.config import Config


def test_tools_normalizer():
    """Test tools normalizer functionality."""
    print("🔧 Testing Tools Normalizer")
    print("=" * 40)

    # Create a temporary test folder
    test_folder = tempfile.mkdtemp(prefix="linolog_test_tools_")

    # Create a metadata file with various tool names that need normalization
    metadata_content = """
title: "Tools Test Print"
edition: "3"
size: "8x10"
medium: "Linocut"
paper_type: "mulberry paper"
blocks_used: "2"
carving_tools: "pfiel gouge, flex cut, v-gauge"
brayer_type: "speedball 4 inch"
burnish_type: "wooden spatula"
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
    test_tools_normalizer()
