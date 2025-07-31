import os
import logging
from typing import Dict, Any, List
from metadata_loader import MetadataLoader
from sheet_writer import SheetWriter
from agents.metadata_filler import MetadataFillerAgent
from agents.color_agent import ColorAgent
from agents.tag_agent import TagAgent
from tools_normalizer import normalize_tools
from agents.llm_color_agent import LLMColorAgent
from agents.llm_tag_agent import LLMTagAgent
from llm_client import LLMClient
from config import Config

class PrintProcessor:
    """Main processor that orchestrates the entire workflow."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.metadata_loader = MetadataLoader()
        self.sheet_writer = SheetWriter()
        self.agents = self._setup_agents()
        self.processed_folders = self._load_processed_folders()
    
    def _setup_agents(self):
        """Set up the agent system."""
        agents = []
        
        # Initialize LLM client if enabled
        llm_client = None
        if Config.ENABLE_LLM:
            llm_client = LLMClient(provider=Config.LLM_PROVIDER)
            if llm_client.is_available():
                self.logger.info(f"LLM client initialized with {Config.LLM_PROVIDER}")
            else:
                self.logger.warning("LLM client not available, using traditional agents")
                llm_client = None
        
        if Config.ENABLE_METADATA_FILLER:
            agents.append(MetadataFillerAgent())
        
        if Config.ENABLE_COLOR_AGENT:
            if llm_client and Config.ENABLE_LLM_COLOR_AGENT:
                agents.append(LLMColorAgent(llm_client))
                self.logger.info("Using LLM-enhanced Color Agent")
            else:
                agents.append(ColorAgent())
        
        if Config.ENABLE_TAG_AGENT:
            if llm_client and Config.ENABLE_LLM_TAG_AGENT:
                agents.append(LLMTagAgent(llm_client))
                self.logger.info("Using LLM-enhanced Tag Agent")
            else:
                agents.append(TagAgent())
        

        
        self.logger.info(f"Initialized {len(agents)} agents")
        return agents
    
    def _load_processed_folders(self) -> set:
        """Load list of already processed folders."""
        processed = set()
        
        if os.path.exists(Config.PROCESSED_LOG_FILE):
            try:
                with open(Config.PROCESSED_LOG_FILE, 'r') as f:
                    processed = set(line.strip() for line in f if line.strip())
            except Exception as e:
                self.logger.warning(f"Failed to load processed folders: {e}")
        
        return processed
    
    def _save_processed_folders(self):
        """Save list of processed folders."""
        try:
            with open(Config.PROCESSED_LOG_FILE, 'w') as f:
                for folder in self.processed_folders:
                    f.write(f"{folder}\n")
        except Exception as e:
            self.logger.error(f"Failed to save processed folders: {e}")
    
    def process_folder(self, folder_path: str):
        """Process a single print folder."""
        try:
            # Check if already processed
            if folder_path in self.processed_folders:
                self.logger.info(f"Folder already processed: {folder_path}")
                return
            
            print(f"\n🔄 Processing folder: {os.path.basename(folder_path)}")
            self.logger.info(f"Processing folder: {folder_path}")
            
            # Load initial metadata
            print("📝 Loading metadata...")
            metadata = self.metadata_loader.load_metadata(folder_path)
            print(f"   Found metadata: {list(metadata.keys())}")
            
            # Run agents to enhance metadata
            print("🤖 Running AI agents...")
            for agent in self.agents:
                if agent.is_enabled():
                    try:
                        print(f"   Running {agent.__class__.__name__}...")
                        metadata = agent.process(metadata, folder_path)
                    except Exception as e:
                        self.logger.error(f"Agent {agent.__class__.__name__} failed: {e}")
                        print(f"   ❌ {agent.__class__.__name__} failed: {e}")
            
            # Normalize tool names
            if Config.ENABLE_TOOLS_NORMALIZER:
                metadata = normalize_tools(metadata)
            
            # Validate required fields
            print("✅ Validating required fields...")
            missing_fields = self._validate_metadata(metadata)
            if missing_fields:
                print(f"   ⚠️  Missing required fields: {missing_fields}")
                self.logger.warning(f"Missing required fields: {missing_fields}")
            
            # Always prompt for metadata review
            print("📝 Prompting for metadata review...")
            metadata = self._prompt_for_missing_fields(metadata, missing_fields)
            
            # Check if record already exists
            title = metadata.get('title', 'Unknown')
            edition = metadata.get('edition', '1')
            
            print(f"📊 Checking if record exists: {title} - Edition {edition}")
            if self.sheet_writer.check_if_exists(title, edition):
                self.logger.info(f"Record already exists: {title} - {edition}")
                print("   ✅ Record already exists in Google Sheets")
                # Mark as processed even if it exists
                self.processed_folders.add(folder_path)
                self._save_processed_folders()
                return
            
            # Write to Google Sheets
            print("📈 Writing to Google Sheets...")
            if self.sheet_writer.add_print_record(metadata):
                self.logger.info(f"Successfully processed: {title}")
                print(f"   ✅ Successfully processed: {title}")
                
                # Save metadata file locally
                print("💾 Saving metadata file locally...")
                if self._save_metadata_file(folder_path, metadata):
                    print(f"   ✅ Saved metadata.yaml to folder")
                else:
                    print(f"   ⚠️  Failed to save metadata.yaml")
                
                # Mark as processed
                self.processed_folders.add(folder_path)
                self._save_processed_folders()
            else:
                self.logger.error(f"Failed to write to Google Sheets: {title}")
                print(f"   ❌ Failed to write to Google Sheets: {title}")
            
        except Exception as e:
            self.logger.error(f"Failed to process folder {folder_path}: {e}")
            print(f"   ❌ Failed to process folder: {e}")
    
    def _validate_metadata(self, metadata: Dict[str, Any]) -> list:
        """Validate that all required fields are present."""
        missing = []
        
        for field in Config.REQUIRED_FIELDS:
            if field not in metadata or not metadata[field]:
                missing.append(field)
        
        return missing
    
    def scan_existing_folders(self):
        """Scan for existing folders that haven't been processed."""
        if not os.path.exists(Config.WATCH_DIRECTORY):
            self.logger.warning(f"Watch directory does not exist: {Config.WATCH_DIRECTORY}")
            return
        
        for item in os.listdir(Config.WATCH_DIRECTORY):
            item_path = os.path.join(Config.WATCH_DIRECTORY, item)
            if os.path.isdir(item_path):
                self.process_folder(item_path)
    
    def _prompt_for_missing_fields(self, metadata: Dict[str, Any], missing_fields: List[str]) -> Dict[str, Any]:
        """Always prompt user for metadata confirmation and editing."""
        print("\n📝 Metadata Review & Edit:")
        print("=" * 40)
        
        # Show all current metadata
        print("Current metadata:")
        for key, value in metadata.items():
            print(f"   {key}: {value}")
        
        print("\n📝 Edit metadata (press Enter to keep current value):")
        
        # Always prompt for all required fields
        for field in Config.REQUIRED_FIELDS:
            current_value = metadata.get(field, '')
            default_value = self._get_default_value(field, metadata)
            
            # Display field name nicely
            display_name = self._get_display_name(field)
            
            if current_value:
                print(f"   {display_name}: {current_value} (current)")
            else:
                print(f"   {display_name}: (missing, default: {default_value})")
            
            # Get user input
            user_input = input(f"   Enter {field}: ").strip()
            
            if user_input:
                # User entered a value
                metadata[field] = user_input
                print(f"   ✅ Set {field} = {user_input}")
            elif current_value:
                # User pressed Enter and there's a current value
                print(f"   ✅ Keeping current value: {current_value}")
            else:
                # User pressed Enter, no current value, use default
                metadata[field] = default_value
                print(f"   ⚠️  Using default: {field} = {default_value}")
        
        # Ask if user wants to add optional fields
        print("\n📝 Optional fields:")
        optional_fields = ['paper_width', 'mounted', 'combined_pieces', 'reduction', 
                         'carving_tools', 'brayer_type', 'burnish_type', 'notes']
        
        for field in optional_fields:
            current_value = metadata.get(field, '')
            display_name = self._get_display_name(field)
            
            if current_value:
                print(f"   {display_name}: {current_value} (current)")
            else:
                print(f"   {display_name}: (optional)")
            
            user_input = input(f"   Enter {display_name} (or press Enter to skip): ").strip()
            if user_input:
                metadata[field] = user_input
                print(f"   ✅ Set {display_name} = {user_input}")
        
        print("\n✅ Metadata review completed!")
        return metadata
    
    def _get_display_name(self, field: str) -> str:
        """Get display name for a field."""
        display_names = {
            'title': 'Title',
            'date': 'Date',
            'edition': 'No. of Editions',
            'size': 'Size',
            'medium': 'Medium',
            'paper_type': 'Paper Type',
            'blocks_used': 'Blocks Used',
            'paper_width': 'Paper Width',
            'mounted': 'Mounted',
            'combined_pieces': 'Combined Pieces',
            'reduction': 'Reduction',
            'carving_tools': 'Carving Tools',
            'brayer_type': 'Brayer Type',
            'burnish_type': 'Burnish Type',
            'notes': 'Notes'
        }
        return display_names.get(field, field)
    
    def _save_metadata_file(self, folder_path: str, metadata: Dict[str, Any]) -> bool:
        """Save the final metadata to a YAML file in the folder."""
        try:
            import yaml
            
            # Create the metadata file path
            metadata_path = os.path.join(folder_path, 'metadata.yaml')
            
            # Sort metadata for better readability
            sorted_metadata = dict(sorted(metadata.items()))
            
            # Write the metadata to YAML file
            with open(metadata_path, 'w', encoding='utf-8') as f:
                yaml.dump(sorted_metadata, f, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False)
            
            self.logger.info(f"Saved metadata to {metadata_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save metadata file: {e}")
            return False
    
    def _save_metadata_file(self, folder_path: str, metadata: Dict[str, Any]) -> bool:
        """Save metadata to YAML file in the folder."""
        try:
            yaml_path = os.path.join(folder_path, 'metadata.yaml')
            with open(yaml_path, 'w', encoding='utf-8') as file:
                import yaml
                yaml.dump(metadata, file, default_flow_style=False, allow_unicode=True, sort_keys=False)
            self.logger.info(f"Saved metadata to {yaml_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save metadata file: {e}")
            return False
    
    def _get_default_value(self, field: str, metadata: Dict[str, Any]) -> str:
        """Get default value for a field."""
        defaults = {
            'title': 'Unknown Print',
            'date': '2025-01-01',
            'edition': '1',
            'size': 'Unknown',
            'medium': 'Linocut',
            'paper_type': 'Unknown',
            'blocks_used': '1'
        }
        return defaults.get(field, 'Unknown')
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return {
            'processed_folders': len(self.processed_folders),
            'enabled_agents': len([a for a in self.agents if a.is_enabled()]),
            'total_agents': len(self.agents)
        } 