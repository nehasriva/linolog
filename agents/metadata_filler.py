import os
import re
from typing import Dict, Any
from .base_agent import BaseAgent
from config import Config

class MetadataFillerAgent(BaseAgent):
    """Agent that fills in missing required metadata fields using heuristics."""
    
    def process(self, metadata: Dict[str, Any], folder_path: str) -> Dict[str, Any]:
        """Fill in missing required fields with sensible defaults."""
        updated_metadata = metadata.copy()
        
        # Fill in missing required fields
        for field in Config.REQUIRED_FIELDS:
            if field not in updated_metadata or not updated_metadata[field]:
                value = self._get_default_value(field, updated_metadata, folder_path)
                if value:
                    updated_metadata[field] = value
                    print(f"      🔧 Filled {field} = {value}")
                    self.logger.info(f"Filled missing field '{field}' with value: {value}")
        
        return updated_metadata
    
    def _get_default_value(self, field: str, metadata: Dict[str, Any], folder_path: str) -> Any:
        """Get default value for a missing field."""
        if field == 'title':
            return self._extract_title_from_folder(folder_path)
        elif field == 'edition':
            return self._extract_edition_from_folder(folder_path)
        elif field == 'date':
            from datetime import datetime
            return datetime.now().strftime('%Y-%m-%d')
        elif field == 'size':
            return self._suggest_size(folder_path)
        elif field == 'medium':
            return 'Battleship Grey'  # Default for this system
        elif field == 'paper_type':
            return 'Unknown'  # Would need user input
        elif field == 'blocks_used':
            return 1  # Default to single block
        
        return None
    
    def _extract_title_from_folder(self, folder_path: str) -> str:
        """Extract title from folder name."""
        folder_name = os.path.basename(folder_path)
        
        # Remove edition pattern and clean up
        title = re.sub(r'_edition_\d+.*$', '', folder_name)
        title = title.replace('_', ' ').title()
        
        return title
    
    def _extract_edition_from_folder(self, folder_path: str) -> str:
        """Extract edition number from folder name."""
        folder_name = os.path.basename(folder_path)
        
        # Look for edition pattern
        match = re.search(r'_edition_(\d+)', folder_name)
        if match:
            return match.group(1)
        
        return '1'  # Default edition
    
    def _suggest_size(self, folder_path: str) -> str:
        """Suggest size based on folder name or image analysis."""
        folder_name = os.path.basename(folder_path)
        
        # Look for size patterns in folder name
        size_patterns = [
            r'(\d+x\d+)',  # 8x10, 9x12, etc.
            r'(\d+["\']x\d+["\'])',  # 8"x10", etc.
            r'(\d+cmx\d+cm)',  # 20cmx30cm, etc.
        ]
        
        for pattern in size_patterns:
            match = re.search(pattern, folder_name, re.IGNORECASE)
            if match:
                return match.group(1)
        
        # Default size
        return 'Unknown' 