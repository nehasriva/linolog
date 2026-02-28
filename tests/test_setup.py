#!/usr/bin/env python3
"""
Test script for LinoLog setup verification.
"""

import os
import sys
import logging
from linolog.config import Config
from linolog.metadata_loader import MetadataLoader
from linolog.sheet_writer import SheetWriter


def test_config():
    """Test configuration loading."""
    print("🔧 Testing configuration...")
    try:
        Config.validate_config()
        print("✅ Configuration is valid")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


def test_google_sheets():
    """Test Google Sheets connection."""
    print("📊 Testing Google Sheets connection...")
    try:
        sheet_writer = SheetWriter()
        sheet_writer.ensure_headers()
        print("✅ Google Sheets connection successful")
        return True
    except Exception as e:
        print(f"❌ Google Sheets error: {e}")
        return False


def test_metadata_loader():
    """Test metadata loader."""
    print("📝 Testing metadata loader...")
    try:
        loader = MetadataLoader()
        print("✅ Metadata loader initialized")
        return True
    except Exception as e:
        print(f"❌ Metadata loader error: {e}")
        return False


def test_watch_directory():
    """Test watch directory."""
    print("📁 Testing watch directory...")
    try:
        if not os.path.exists(Config.WATCH_DIRECTORY):
            os.makedirs(Config.WATCH_DIRECTORY, exist_ok=True)
            print(f"✅ Created watch directory: {Config.WATCH_DIRECTORY}")
        else:
            print(f"✅ Watch directory exists: {Config.WATCH_DIRECTORY}")
        return True
    except Exception as e:
        print(f"❌ Watch directory error: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 LinoLog Setup Test")
    print("=" * 30)

    tests = [
        test_config,
        test_google_sheets,
        test_metadata_loader,
        test_watch_directory,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 30)
    print(f"📊 Test Results: {passed}/{total} passed")

    if passed == total:
        print("🎉 All tests passed! LinoLog is ready to use.")
        print("Run 'linolog' to start the system.")
    else:
        print("⚠️  Some tests failed. Please check the setup instructions.")
        sys.exit(1)


if __name__ == "__main__":
    main()
