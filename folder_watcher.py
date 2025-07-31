import os
import logging
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

class PrintFolderHandler(FileSystemEventHandler):
    """Handler for detecting new print folders."""
    
    def __init__(self, callback_func, watch_directory):
        self.callback_func = callback_func
        self.watch_directory = watch_directory
        self.logger = logging.getLogger(__name__)
        self.processing_folders = set()  # Track folders being processed
        self.pending_folders = {}  # Track folders waiting to be processed
        self.known_folders = set()  # Track folders we've seen
        self.last_scan_time = 0
        
        # Start periodic scanning
        self.scan_timer = threading.Timer(5.0, self._periodic_scan)
        self.scan_timer.start()
    
    def on_created(self, event):
        """Called when a new folder is created."""
        self.logger.info(f"Event: on_created - {event.src_path} (is_dir: {event.is_directory})")
        if event.is_directory:
            # Only process if it's a direct subfolder of the watch directory
            if self._is_valid_subfolder(event.src_path):
                self.logger.info(f"New folder created: {event.src_path}")
                self._schedule_processing(event.src_path)
            else:
                self.logger.info(f"Ignoring created folder (not valid subfolder): {event.src_path}")
    
    def on_moved(self, event):
        """Called when a folder is moved/renamed."""
        self.logger.info(f"Event: on_moved - {event.src_path} -> {event.dest_path} (is_dir: {event.is_directory})")
        if event.is_directory:
            # Only process if the destination is a direct subfolder of the watch directory
            if self._is_valid_subfolder(event.dest_path):
                self.logger.info(f"Folder moved: {event.src_path} -> {event.dest_path}")
                self._schedule_processing(event.dest_path)
            else:
                self.logger.info(f"Ignoring moved folder (not valid subfolder): {event.dest_path}")
    
    def on_modified(self, event):
        """Called when a folder is modified (useful for copied folders)."""
        self.logger.info(f"Event: on_modified - {event.src_path} (is_dir: {event.is_directory})")
        if event.is_directory:
            # Only process if it's a direct subfolder of the watch directory
            if self._is_valid_subfolder(event.src_path):
                self.logger.info(f"Folder modified: {event.src_path}")
                self._schedule_processing(event.src_path)
            else:
                self.logger.info(f"Ignoring modified folder (not valid subfolder): {event.src_path}")
    
    def _is_valid_subfolder(self, folder_path):
        """Check if the folder is a valid subfolder of the watch directory."""
        try:
            # Get the parent directory of the folder
            parent_dir = os.path.dirname(folder_path)
            # Check if the parent is the watch directory
            is_valid = os.path.abspath(parent_dir) == os.path.abspath(self.watch_directory)
            self.logger.info(f"Subfolder check: {folder_path} -> parent: {parent_dir} -> valid: {is_valid}")
            return is_valid
        except Exception as e:
            self.logger.error(f"Error checking subfolder validity: {e}")
            return False
    
    def _periodic_scan(self):
        """Periodically scan for new folders that might have been missed by events."""
        try:
            current_folders = set()
            if os.path.exists(self.watch_directory):
                for item in os.listdir(self.watch_directory):
                    item_path = os.path.join(self.watch_directory, item)
                    if os.path.isdir(item_path):
                        current_folders.add(item_path)
            
            # Find new folders
            new_folders = current_folders - self.known_folders
            if new_folders:
                self.logger.info(f"Periodic scan found new folders: {new_folders}")
                for folder_path in new_folders:
                    if self._is_valid_subfolder(folder_path):
                        self._schedule_processing(folder_path)
            
            # Update known folders
            self.known_folders = current_folders
            
        except Exception as e:
            self.logger.error(f"Error in periodic scan: {e}")
        
        # Schedule next scan
        self.scan_timer = threading.Timer(5.0, self._periodic_scan)
        self.scan_timer.start()
    
    def _schedule_processing(self, folder_path):
        """Schedule folder processing with delay to ensure folder is ready."""
        if folder_path in self.processing_folders:
            self.logger.info(f"Folder already being processed: {folder_path}")
            return
        
        # Cancel any existing pending processing for this folder
        if folder_path in self.pending_folders:
            self.pending_folders[folder_path].cancel()
        
        # Schedule processing with a delay
        timer = threading.Timer(2.0, self._process_folder, args=[folder_path])
        self.pending_folders[folder_path] = timer
        timer.start()
        
        self.logger.info(f"Scheduled processing for: {folder_path} (2 second delay)")
    
    def _process_folder(self, folder_path):
        """Process a folder after ensuring it's ready."""
        try:
            # Remove from pending
            if folder_path in self.pending_folders:
                del self.pending_folders[folder_path]
            
            # Check if folder still exists and is accessible
            if not os.path.exists(folder_path):
                self.logger.warning(f"Folder no longer exists: {folder_path}")
                return
            
            # Check if folder is ready (has some content)
            try:
                items = os.listdir(folder_path)
                if not items:
                    self.logger.info(f"Folder appears empty, waiting longer: {folder_path}")
                    # Schedule another check in 3 seconds
                    timer = threading.Timer(3.0, self._process_folder, args=[folder_path])
                    self.pending_folders[folder_path] = timer
                    timer.start()
                    return
            except (OSError, PermissionError) as e:
                self.logger.warning(f"Cannot access folder yet: {folder_path} - {e}")
                # Schedule another check in 2 seconds
                timer = threading.Timer(2.0, self._process_folder, args=[folder_path])
                self.pending_folders[folder_path] = timer
                timer.start()
                return
            
            # Mark as processing
            self.processing_folders.add(folder_path)
            
            # Process the folder
            self.logger.info(f"Processing folder: {folder_path}")
            self.callback_func(folder_path)
            
            # Remove from processing set
            self.processing_folders.discard(folder_path)
            
        except Exception as e:
            self.logger.error(f"Error processing folder {folder_path}: {e}")
            self.processing_folders.discard(folder_path)

class FolderWatcher:
    """Watches for new print folders in the archive directory."""
    
    def __init__(self, watch_directory, callback_func):
        self.watch_directory = watch_directory
        self.callback_func = callback_func
        self.observer = Observer()
        self.logger = logging.getLogger(__name__)
    
    def start(self):
        """Start watching the directory."""
        if not os.path.exists(self.watch_directory):
            self.logger.warning(f"Watch directory does not exist: {self.watch_directory}")
            os.makedirs(self.watch_directory, exist_ok=True)
            self.logger.info(f"Created watch directory: {self.watch_directory}")
        
        event_handler = PrintFolderHandler(self.callback_func, self.watch_directory)
        self.observer.schedule(event_handler, self.watch_directory, recursive=False)
        self.observer.start()
        self.logger.info(f"Started watching directory: {self.watch_directory}")
    
    def stop(self):
        """Stop watching the directory."""
        # Cancel any pending timers
        if hasattr(self.observer, '_handlers'):
            for handler in self.observer._handlers:
                if hasattr(handler, 'pending_folders'):
                    for timer in handler.pending_folders.values():
                        timer.cancel()
                if hasattr(handler, 'scan_timer'):
                    handler.scan_timer.cancel()
        
        self.observer.stop()
        self.observer.join()
        self.logger.info("Stopped watching directory")
    
    def scan_existing_folders(self):
        """Scan for existing folders that haven't been processed yet."""
        if not os.path.exists(self.watch_directory):
            return
        
        for item in os.listdir(self.watch_directory):
            item_path = os.path.join(self.watch_directory, item)
            if os.path.isdir(item_path):
                self.logger.info(f"Found existing folder: {item_path}")
                self.callback_func(item_path) 