#!/usr/bin/env python3
"""
Test script to demonstrate tools normalizer functionality.
"""

import os
import sys
from processor import PrintProcessor
from config import Config

def test_tools_normalizer():
    """Test tools normalizer functionality."""
    print("🔧 Testing Tools Normalizer")
    print("=" * 40)
    
    # Create a test folder
    test_folder = "/Users/nehasrivastava/LinocutArchive/test_tools_normalizer"
    os.makedirs(test_folder, exist_ok=True)
    
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
    print("📄 Created metadata.yaml with various tool names")
    print("\n🔄 Processing folder (should normalize tool names)...")
    print("-" * 50)
    
    # Initialize processor
    processor = PrintProcessor()
    
    # Process the folder (this should trigger tool normalization)
    processor.process_folder(test_folder)
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    test_tools_normalizer() 