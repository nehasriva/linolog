import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import Dict, Any, List
import logging
from config import Config

class SheetWriter:
    """Handles writing metadata to Google Sheets."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = None
        self.sheet = None
        self._setup_client()
    
    def _setup_client(self):
        """Set up Google Sheets client with service account credentials."""
        try:
            # Define the scope
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            
            # Load credentials from JSON file
            creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
            self.client = gspread.authorize(creds)
            
            # Open the spreadsheet
            self.sheet = self.client.open_by_key(Config.GOOGLE_SHEET_ID).worksheet(Config.GOOGLE_SHEET_NAME)
            
            self.logger.info("Successfully connected to Google Sheets")
            
        except Exception as e:
            self.logger.error(f"Failed to set up Google Sheets client: {e}")
            raise
    
    def ensure_headers(self):
        """Ensure the sheet has the correct headers."""
        try:
            # Get current headers
            current_headers = self.sheet.row_values(1)
            
            # If no headers or wrong headers, set them
            if not current_headers or current_headers != Config.SHEET_HEADERS:
                self.sheet.clear()
                self.sheet.append_row(Config.SHEET_HEADERS)
                self.logger.info("Set up sheet headers")
            
        except Exception as e:
            self.logger.error(f"Failed to ensure headers: {e}")
            raise
    
    def add_print_record(self, metadata: Dict[str, Any]) -> bool:
        """Add a new print record to the sheet."""
        try:
            # Ensure headers are present
            self.ensure_headers()
            
            # Convert metadata to row format
            row_data = self._metadata_to_row(metadata)
            
            # Add the row
            self.sheet.append_row(row_data)
            
            self.logger.info(f"Added print record: {metadata.get('title', 'Unknown')}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add print record: {e}")
            return False
    
    def _metadata_to_row(self, metadata: Dict[str, Any]) -> List[str]:
        """Convert metadata dictionary to row format for Google Sheets."""
        row = []
        
        # Map metadata fields to sheet columns
        field_mapping = {
            'title': 'Title',
            'date': 'Date',
            'edition': 'No. of Editions',
            'size': 'Size',
            'medium': 'Medium',
            'paper_type': 'Paper Type',
            'paper_width': 'Paper Width',
            'mounted': 'Mounted',
            'combined_pieces': 'Combined Pieces',
            'blocks_used': 'Blocks Used',
            'reduction': 'Reduction',
            'carving_tools': 'Carving Tools',
            'brayer_type': 'Brayer Type',
            'burnish_type': 'Burnish Type',
            'colors_used': 'Colors Used',
            'series': 'Series',
            'tags': 'Tags',
            'notes': 'Notes'
        }
        
        # Build row in the correct order
        for field in Config.SHEET_HEADERS:
            # Find the corresponding metadata key
            metadata_key = None
            for key, sheet_field in field_mapping.items():
                if sheet_field == field:
                    metadata_key = key
                    break
            
            if metadata_key and metadata_key in metadata:
                value = metadata[metadata_key]
                
                # Handle different data types
                if isinstance(value, list):
                    value = ', '.join(str(item) for item in value)
                elif isinstance(value, bool):
                    value = 'Yes' if value else 'No'
                else:
                    value = str(value) if value is not None else ''
                
                row.append(value)
            else:
                row.append('')  # Empty cell for missing data
        
        return row
    
    def check_if_exists(self, title: str, edition: str) -> bool:
        """Check if a print record already exists in the sheet."""
        try:
            # Get all values
            all_values = self.sheet.get_all_values()
            
            if len(all_values) <= 1:  # Only headers or empty
                return False
            
            # Check for matching title and edition
            for row in all_values[1:]:  # Skip header row
                if len(row) >= 3:  # Ensure we have title and edition columns
                    if row[0] == title and row[2] == edition:  # Title and Edition columns
                        return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to check if record exists: {e}")
            return False
    
    def update_record(self, title: str, edition: str, metadata: Dict[str, Any]) -> bool:
        """Update an existing print record."""
        try:
            # Find the row with matching title and edition
            all_values = self.sheet.get_all_values()
            
            for i, row in enumerate(all_values[1:], start=2):  # Start from row 2 (after headers)
                if len(row) >= 3 and row[0] == title and row[2] == edition:
                    # Convert metadata to row format
                    new_row_data = self._metadata_to_row(metadata)
                    
                    # Update the row
                    self.sheet.update(f'A{i}:Z{i}', [new_row_data])
                    
                    self.logger.info(f"Updated print record: {title}")
                    return True
            
            self.logger.warning(f"Record not found for update: {title} - {edition}")
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to update record: {e}")
            return False 