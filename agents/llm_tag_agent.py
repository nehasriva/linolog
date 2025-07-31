import re
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent

class LLMTagAgent(BaseAgent):
    """Enhanced tag agent that uses LLM for better contextual tag generation."""
    
    def __init__(self, llm_client=None):
        super().__init__()
        self.llm_client = llm_client
        self.tag_patterns = {
            'style': {
                'reduction': ['reduction', 'reductive'],
                'multi_block': ['multi-block', 'multi block', 'multiple blocks'],
                'single_block': ['single block', 'one block'],
                'abstract': ['abstract', 'non-representational'],
                'representational': ['representational', 'realistic', 'figurative'],
                'landscape': ['landscape', 'nature', 'outdoor'],
                'portrait': ['portrait', 'figure', 'person'],
                'still_life': ['still life', 'object', 'composition']
            },
            'technique': {
                'carving': ['carving', 'cut', 'gouge'],
                'burnishing': ['burnishing', 'baren', 'spoon'],
                'inking': ['inking', 'brayer', 'roller'],
                'printing': ['printing', 'press', 'hand-pulled']
            },
            'subject': {
                'nature': ['nature', 'natural', 'organic'],
                'urban': ['urban', 'city', 'architecture'],
                'animals': ['animal', 'wildlife', 'creature'],
                'plants': ['plant', 'flora', 'botanical'],
                'geometric': ['geometric', 'geometric', 'angular'],
                'texture': ['texture', 'textural', 'surface']
            },
            'color_scheme': {
                'monochrome': ['black', 'white', 'gray', 'monochrome'],
                'warm': ['red', 'orange', 'yellow', 'brown'],
                'cool': ['blue', 'green', 'purple'],
                'high_contrast': ['black', 'white', 'contrast'],
                'earth_tones': ['brown', 'earth', 'natural', 'organic']
            }
        }
    
    def process(self, metadata: Dict[str, Any], folder_path: str) -> Dict[str, Any]:
        """Generate tags using LLM if available, fallback to pattern matching."""
        updated_metadata = metadata.copy()
        
        # Try LLM tag generation first
        tags = self._generate_tags_with_llm(metadata)
        if not tags:
            print(f"      🔄 LLM tag generation failed, using pattern matching")
            tags = self._generate_tags_traditional(metadata)
        
        if tags:
            updated_metadata['tags'] = tags
            print(f"      🏷️  Generated tags: {tags}")
            self.logger.info(f"Generated tags: {tags}")
        
        return updated_metadata
    
    def _generate_tags_with_llm(self, metadata: Dict[str, Any]) -> Optional[List[str]]:
        """Generate tags using LLM if available."""
        if not self.llm_client:
            return None
        
        try:
            # Create a rich context for the LLM
            context = self._build_metadata_context(metadata)
            
            prompt = f"""Based on this linocut print metadata, generate 5-8 relevant searchable tags for art categorization.

Metadata: {context}

Generate tags that cover:
- Style/technique (e.g., reduction_print, multi_block, hand_pulled)
- Subject matter (e.g., landscape, portrait, abstract, nature)
- Color scheme (e.g., monochrome, earth_tones, high_contrast)
- Mood/theme (e.g., peaceful, dramatic, organic)
- Technical details (e.g., reduction, multi_color, hand_pressed)

Return only the tags separated by commas, no explanations.
Example: reduction_print, california_landscape, forest_theme, earth_tones, hand_pulled"""
            
            # Call LLM
            response = self.llm_client.analyze_text(prompt)
            
            if response:
                # Parse response into tag list
                tags = [tag.strip().replace(' ', '_') for tag in response.split(',')]
                return tags[:8]  # Limit to 8 tags
            
        except Exception as e:
            self.logger.error(f"LLM tag generation failed: {e}")
        
        return None
    
    def _build_metadata_context(self, metadata: Dict[str, Any]) -> str:
        """Build a rich context string from metadata for LLM."""
        context_parts = []
        
        # Add key metadata fields
        if 'title' in metadata:
            context_parts.append(f"Title: {metadata['title']}")
        if 'size' in metadata:
            context_parts.append(f"Size: {metadata['size']}")
        if 'medium' in metadata:
            context_parts.append(f"Medium: {metadata['medium']}")
        if 'paper_type' in metadata:
            context_parts.append(f"Paper: {metadata['paper_type']}")
        if 'blocks_used' in metadata:
            context_parts.append(f"Blocks: {metadata['blocks_used']}")
        if 'colors_used' in metadata:
            context_parts.append(f"Colors: {metadata['colors_used']}")
        if 'carving_tools' in metadata:
            context_parts.append(f"Tools: {metadata['carving_tools']}")
        if 'brayer_type' in metadata:
            context_parts.append(f"Brayer: {metadata['brayer_type']}")
        if 'burnish_type' in metadata:
            context_parts.append(f"Burnish: {metadata['burnish_type']}")
        if 'reduction' in metadata:
            context_parts.append(f"Reduction: {metadata['reduction']}")
        if 'mounted' in metadata:
            context_parts.append(f"Mounted: {metadata['mounted']}")
        
        return ', '.join(context_parts)
    
    def _generate_tags_traditional(self, metadata: Dict[str, Any]) -> List[str]:
        """Traditional tag generation using pattern matching (fallback method)."""
        tags = []
        
        # Extract text content for analysis
        text_content = self._extract_text_content(metadata)
        
        # Generate tags based on patterns
        for category, patterns in self.tag_patterns.items():
            for tag_name, keywords in patterns.items():
                if self._matches_keywords(text_content, keywords):
                    tags.append(tag_name)
        
        # Add size-based tags
        if 'size' in metadata:
            size_tags = self._get_size_tags(metadata['size'])
            tags.extend(size_tags)
        
        # Add color-based tags
        if 'colors_used' in metadata:
            color_tags = self._get_color_tags(metadata['colors_used'])
            tags.extend(color_tags)
        
        # Add technique tags based on tools
        if 'carving_tools' in metadata:
            tool_tags = self._get_tool_tags(metadata['carving_tools'])
            tags.extend(tool_tags)
        
        # Remove duplicates and return
        return list(set(tags))
    
    def _extract_text_content(self, metadata: Dict[str, Any]) -> str:
        """Extract all text content from metadata for analysis."""
        text_parts = []
        
        for key, value in metadata.items():
            if isinstance(value, str):
                text_parts.append(value.lower())
            elif isinstance(value, list):
                text_parts.extend([str(item).lower() for item in value])
            elif value is not None:
                text_parts.append(str(value).lower())
        
        return ' '.join(text_parts)
    
    def _matches_keywords(self, text: str, keywords: List[str]) -> bool:
        """Check if text contains any of the keywords."""
        return any(keyword in text for keyword in keywords)
    
    def _get_size_tags(self, size: str) -> List[str]:
        """Generate tags based on print size."""
        size_lower = size.lower()
        tags = []
        
        if 'small' in size_lower or any(dim in size_lower for dim in ['4x6', '5x7', '6x8']):
            tags.append('small')
        elif 'large' in size_lower or any(dim in size_lower for dim in ['11x14', '12x16', '16x20']):
            tags.append('large')
        elif 'medium' in size_lower or any(dim in size_lower for dim in ['8x10', '9x12', '10x12']):
            tags.append('medium')
        
        return tags
    
    def _get_color_tags(self, colors: List[str]) -> List[str]:
        """Generate tags based on colors used."""
        tags = []
        colors_lower = [color.lower() for color in colors]
        
        if len(colors) == 1:
            tags.append('monochrome')
        elif len(colors) > 3:
            tags.append('multi_color')
        
        if any(color in colors_lower for color in ['black', 'white']):
            tags.append('high_contrast')
        
        if any(color in colors_lower for color in ['brown', 'earth', 'natural']):
            tags.append('earth_tones')
        
        return tags
    
    def _get_tool_tags(self, tools: str) -> List[str]:
        """Generate tags based on carving tools used."""
        tools_lower = tools.lower()
        tags = []
        
        if 'pfeil' in tools_lower:
            tags.append('pfeil_tools')
        if 'flexcut' in tools_lower:
            tags.append('flexcut_tools')
        if 'speedball' in tools_lower:
            tags.append('speedball_tools')
        
        return tags 