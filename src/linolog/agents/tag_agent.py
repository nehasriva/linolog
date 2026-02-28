import re
from typing import Dict, Any, List
from .base_agent import BaseAgent


class TagAgent(BaseAgent):
    """Agent that generates searchable tags based on metadata."""

    def __init__(self):
        super().__init__()
        self.tag_patterns = {
            "style": {
                "reduction": ["reduction", "reductive"],
                "multi_block": ["multi-block", "multi block", "multiple blocks"],
                "single_block": ["single block", "one block"],
                "abstract": ["abstract", "non-representational"],
                "representational": ["representational", "realistic", "figurative"],
                "landscape": ["landscape", "nature", "outdoor"],
                "portrait": ["portrait", "figure", "person"],
                "still_life": ["still life", "object", "composition"],
            },
            "technique": {
                "carving": ["carving", "cut", "gouge"],
                "burnishing": ["burnishing", "baren", "spoon"],
                "inking": ["inking", "brayer", "roller"],
                "printing": ["printing", "press", "hand-pulled"],
            },
            "subject": {
                "nature": ["nature", "natural", "organic"],
                "urban": ["urban", "city", "architecture"],
                "animals": ["animal", "wildlife", "creature"],
                "plants": ["plant", "flora", "botanical"],
                "geometric": ["geometric", "geometric", "angular"],
                "texture": ["texture", "textural", "surface"],
            },
            "color_scheme": {
                "monochrome": ["black", "white", "gray", "monochrome"],
                "warm": ["red", "orange", "yellow", "brown"],
                "cool": ["blue", "green", "purple"],
                "high_contrast": ["black", "white", "contrast"],
                "earth_tones": ["brown", "earth", "natural", "organic"],
            },
        }

    def process(self, metadata: Dict[str, Any], folder_path: str) -> Dict[str, Any]:
        """Generate tags based on metadata content."""
        updated_metadata = metadata.copy()

        tags = self._generate_tags(metadata)
        if tags:
            updated_metadata["tags"] = tags
            print(f"      🏷️  Generated tags: {tags}")
            self.logger.info(f"Generated tags: {tags}")

        return updated_metadata

    def _generate_tags(self, metadata: Dict[str, Any]) -> List[str]:
        """Generate tags based on metadata content."""
        tags = []

        # Extract text content for analysis
        text_content = self._extract_text_content(metadata)

        # Generate tags based on patterns
        for category, patterns in self.tag_patterns.items():
            for tag_name, keywords in patterns.items():
                if self._matches_keywords(text_content, keywords):
                    tags.append(tag_name)

        # Add size-based tags
        if "size" in metadata:
            size_tags = self._get_size_tags(metadata["size"])
            tags.extend(size_tags)

        # Add color-based tags
        if "colors_used" in metadata:
            color_tags = self._get_color_tags(metadata["colors_used"])
            tags.extend(color_tags)

        # Add technique tags based on tools
        if "carving_tools" in metadata:
            tool_tags = self._get_tool_tags(metadata["carving_tools"])
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

        return " ".join(text_parts)

    def _matches_keywords(self, text: str, keywords: List[str]) -> bool:
        """Check if text contains any of the keywords."""
        return any(keyword in text for keyword in keywords)

    def _get_size_tags(self, size: str) -> List[str]:
        """Generate tags based on print size."""
        size_lower = size.lower()
        tags = []

        if "small" in size_lower or any(
            dim in size_lower for dim in ["4x6", "5x7", "6x8"]
        ):
            tags.append("small")
        elif "large" in size_lower or any(
            dim in size_lower for dim in ["11x14", "12x16", "16x20"]
        ):
            tags.append("large")
        elif "medium" in size_lower or any(
            dim in size_lower for dim in ["8x10", "9x12", "10x12"]
        ):
            tags.append("medium")

        return tags

    def _get_color_tags(self, colors: List[str]) -> List[str]:
        """Generate tags based on colors used."""
        tags = []
        colors_lower = [color.lower() for color in colors]

        if len(colors) == 1:
            tags.append("monochrome")
        elif len(colors) > 3:
            tags.append("multi_color")

        if any(color in colors_lower for color in ["black", "white"]):
            tags.append("high_contrast")

        if any(color in colors_lower for color in ["brown", "earth", "natural"]):
            tags.append("earth_tones")

        return tags

    def _get_tool_tags(self, tools: str) -> List[str]:
        """Generate tags based on carving tools used."""
        tools_lower = tools.lower()
        tags = []

        if "pfeil" in tools_lower:
            tags.append("pfeil_tools")
        if "flexcut" in tools_lower:
            tags.append("flexcut_tools")
        if "speedball" in tools_lower:
            tags.append("speedball_tools")

        return tags
