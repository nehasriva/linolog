#!/usr/bin/env python3
"""
Test script to demonstrate interactive metadata prompting.
"""

import os
import sys
import tempfile
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
    print("📄 Created metadata.yaml with some missing fields")
    print("📝 Instructions:")
    print("   - Press Enter on 'Date' to use default (2025-01-01)")
    print("   - Press Enter on 'Size' to use default (Unknown)")
    print("   - Press Enter on 'Medium' to use default (Linocut)")
    print("   - Press Enter on 'Paper Type' to use default (Unknown)")
    print("   - Press Enter on 'Blocks Used' to use default (1)")
    print("   - Press Enter on 'No. of Editions' to use default (1)")
    print("\n🔄 Now processing folder...")
    print("-" * 50)

    # Initialize processor
    processor = PrintProcessor()

    # Process the folder (this should trigger prompts)
    processor.process_folder(test_folder)

    print("\n✅ Test completed!")


if __name__ == "__main__":
    test_interactive_metadata()
