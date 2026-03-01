#!/usr/bin/env python3
"""
Test script to demonstrate LLM-enhanced agents functionality.
"""

import os
import sys
import tempfile
from unittest.mock import patch
from linolog.processor import PrintProcessor
from linolog.config import Config


def test_llm_agents():
    """Test LLM-enhanced agents functionality."""
    print("🧠 Testing LLM-Enhanced Agents")
    print("=" * 40)

    # Check if LLM is enabled
    if not Config.ENABLE_LLM:
        print("⚠️  LLM is not enabled. Set ENABLE_LLM=true in .env to test LLM agents.")
        print("   The system will use traditional agents instead.")
        return

    # Create a temporary test folder
    test_folder = tempfile.mkdtemp(prefix="linolog_test_llm_")

    # Create a metadata file with rich content for LLM analysis
    metadata_content = """
title: "California Redwoods at Sunset"
edition: "3"
size: "9x12"
medium: "Linocut"
paper_type: "mulberry"
blocks_used: "2"
carving_tools: "pfeil gouge, flexcut v-gouge"
brayer_type: "speedball 4 inch"
burnish_type: "wooden spatula"
reduction: "true"
mounted: "false"
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
    test_llm_agents()
