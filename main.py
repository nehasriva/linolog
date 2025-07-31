#!/usr/bin/env python3
"""
LinoLog - Linocut Print Metadata Logger
Main entry point for the application.
"""

import os
import sys
import logging
import time
from datetime import datetime

from config import Config
from folder_watcher import FolderWatcher
from processor import PrintProcessor

def setup_logging():
    """Set up logging configuration."""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format=log_format,
        handlers=[
            logging.FileHandler(Config.LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Main entry point for LinoLog."""
    print("🖨️  LinoLog - Linocut Print Metadata Logger")
    print("=" * 50)
    
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Validate configuration
        Config.validate_config()
        logger.info("Configuration validated successfully")
        
        # Initialize processor
        processor = PrintProcessor()
        logger.info("Processor initialized")
        
        # Print startup information
        stats = processor.get_processing_stats()
        print(f"📊 Processing Stats:")
        print(f"   - Processed folders: {stats['processed_folders']}")
        print(f"   - Enabled agents: {stats['enabled_agents']}")
        print(f"   - Total agents: {stats['total_agents']}")
        print()
        
        # Scan existing folders first
        print("🔍 Scanning existing folders...")
        processor.scan_existing_folders()
        
        # Set up folder watcher
        def on_new_folder(folder_path):
            """Callback for new folder detection."""
            print(f"📁 Processing folder: {os.path.basename(folder_path)}")
            processor.process_folder(folder_path)
        
        watcher = FolderWatcher(Config.WATCH_DIRECTORY, on_new_folder)
        
        # Start watching
        print(f"👀 Watching directory: {Config.WATCH_DIRECTORY}")
        print("📋 Folder handling improvements:")
        print("   - Handles dropped-in folders with 2-second delay")
        print("   - Waits for folder content to be fully available")
        print("   - Prevents duplicate processing")
        print("   - Handles copied, moved, and created folders")
        print("Press Ctrl+C to stop...")
        print()
        
        watcher.start()
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping LinoLog...")
            watcher.stop()
            logger.info("LinoLog stopped by user")
            
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Please check your .env file and ensure all required values are set.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 