import os
import yaml
import re
from datetime import datetime
from typing import Dict, Any, Optional

class MetadataLoader:
    """Loads and parses metadata from print folders."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def load_metadata(self, folder_path: str) -> Dict[str, Any]:
        """Load metadata from a print folder."""
        metadata = {}
        
        # Try to load from metadata.yaml file
        yaml_path = os.path.join(folder_path, 'metadata.yaml')
        if os.path.exists(yaml_path):
            print(f"   📄 Found metadata.yaml file")
            metadata.update(self._load_yaml_metadata(yaml_path))
        else:
            print(f"   📄 No metadata.yaml found, extracting from folder name")
        
        # Extract metadata from folder name
        folder_name = os.path.basename(folder_path)
        print(f"   📁 Extracting from folder name: {folder_name}")
        folder_metadata = self._extract_from_folder_name(folder_name)
        metadata.update(folder_metadata)
        
        # Add current date if not present
        if 'date' not in metadata:
            metadata['date'] = datetime.now().strftime('%Y-%m-%d')
            print(f"   📅 Added current date: {metadata['date']}")
        
        return metadata
    
    def _load_yaml_metadata(self, yaml_path: str) -> Dict[str, Any]:
        """Load metadata from YAML file."""
        try:
            with open(yaml_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                return data if data else {}
        except Exception as e:
            self.logger.warning(f"Failed to load YAML metadata from {yaml_path}: {e}")
            return {}
    
    def _extract_from_folder_name(self, folder_name: str) -> Dict[str, Any]:
        """Extract metadata from folder name using pattern matching."""
        metadata = {}
        
        # Pattern: title_edition_X or title_edition_X_other_info
        pattern = r'^(.+?)_edition_(\d+)(?:_(.+))?$'
        match = re.match(pattern, folder_name)
        
        if match:
            title = match.group(1).replace('_', ' ').title()
            edition = match.group(2)
            
            metadata['title'] = title
            metadata['edition'] = edition
            
            # Extract additional info if present
            if match.group(3):
                additional_info = match.group(3).replace('_', ' ')
                # Could be used for size, medium, etc.
                if 'size' not in metadata:
                    metadata['size'] = additional_info
        
        return metadata
    
    def save_metadata(self, folder_path: str, metadata: Dict[str, Any]) -> bool:
        """Save metadata to YAML file."""
        try:
            yaml_path = os.path.join(folder_path, 'metadata.yaml')
            with open(yaml_path, 'w', encoding='utf-8') as file:
                yaml.dump(metadata, file, default_flow_style=False, allow_unicode=True)
            self.logger.info(f"Saved metadata to {yaml_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save metadata: {e}")
            return False
    
    def get_print_image_path(self, folder_path: str) -> Optional[str]:
        """Find the main print image in the folder."""
        image_extensions = ['.jpg', '.jpeg', '.png']
        
        for file in os.listdir(folder_path):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                # Prefer files with 'final' or 'print' in the name
                if 'final' in file.lower() or 'print' in file.lower():
                    return os.path.join(folder_path, file)
        
        # If no preferred file found, return first image
        for file in os.listdir(folder_path):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                return os.path.join(folder_path, file)
        
        return None

import logging 