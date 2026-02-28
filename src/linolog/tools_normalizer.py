import re
from typing import Dict, Any, List

# Standardized tool categories and their known variations
TOOL_STANDARDS = {
    "carving_tools": {
        "pfeil": ["pfeil", "pfiel", "pfiel tools", "pfiel gouge"],
        "flexcut": ["flexcut", "flex cut", "flex-cut"],
        "speedball": ["speedball", "speed ball", "speed-ball"],
        "v-gouge": ["v-gouge", "v gouge", "v gouge", "v-gauge"],
        "u-gouge": ["u-gouge", "u gouge", "u gouge", "u-gauge"],
        "flat-gouge": ["flat-gouge", "flat gouge", "flat gouge"],
        "veiner": ["veiner", "veining tool"],
        "scraper": ["scraper", "scraping tool"],
        "knife": ["knife", "cutting knife", "x-acto", "xacto"],
        "chisel": ["chisel", "wood chisel"],
    },
    "brayer_type": {
        "speedball_soft": [
            "speedball soft",
            "speedball soft rubber",
            "soft rubber brayer",
        ],
        "speedball_hard": [
            "speedball hard",
            "speedball hard rubber",
            "hard rubber brayer",
        ],
        "speedball_4inch": ["speedball 4 inch", 'speedball 4"', "4 inch brayer"],
        "speedball_6inch": ["speedball 6 inch", 'speedball 6"', "6 inch brayer"],
        "hand_roller": ["hand roller", "manual roller"],
        "press_roller": ["press roller", "printing press roller"],
    },
    "burnish_type": {
        "baren": ["baren", "japanese baren", "traditional baren"],
        "spoon": ["spoon", "wooden spoon", "metal spoon"],
        "bone_folder": ["bone folder", "bone folder", "bone creaser"],
        "wooden_spatula": ["wooden spatula", "spatula", "wooden tool"],
        "hand_pressure": ["hand pressure", "hand burnishing", "manual pressure"],
        "press": ["press", "printing press", "mechanical press"],
    },
    "paper_type": {
        "mulberry": ["mulberry", "mulberry paper", "kozo"],
        "rice_paper": ["rice paper", "rice", "asian rice paper"],
        "cotton_rag": ["cotton rag", "cotton", "rag paper"],
        "arches": ["arches", "arches paper", "arches cotton"],
        "stonehenge": ["stonehenge", "stonehenge paper"],
        "bristol": ["bristol", "bristol board", "bristol paper"],
        "newsprint": ["newsprint", "newsprint paper", "practice paper"],
    },
}


def normalize_tools(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize tool names in metadata."""
    updated_metadata = metadata.copy()

    print(f"      🔧 Normalizing tool names...")

    # Normalize each tool field
    for field, standards in TOOL_STANDARDS.items():
        if field in updated_metadata and updated_metadata[field]:
            original_value = updated_metadata[field]
            normalized_value = _normalize_tools(original_value, standards)

            if normalized_value != original_value:
                print(f"         {field}: '{original_value}' → '{normalized_value}'")
                updated_metadata[field] = normalized_value

    return updated_metadata


def _normalize_tools(value: str, standards: Dict[str, List[str]]) -> str:
    """Normalize a tool value to standard format."""
    if not value:
        return value

    # Handle lists (multiple tools)
    if isinstance(value, list):
        normalized_list = []
        for tool in value:
            normalized_tool = _normalize_single_tool(tool, standards)
            normalized_list.append(normalized_tool)
        return ", ".join(normalized_list)

    # Handle single tool
    return _normalize_single_tool(value, standards)


def _normalize_single_tool(tool: str, standards: Dict[str, List[str]]) -> str:
    """Normalize a single tool name."""
    if not tool:
        return tool

    tool_lower = tool.lower().strip()

    # Check against known standards
    for standard_name, variations in standards.items():
        for variation in variations:
            if tool_lower == variation.lower():
                return standard_name

    # If no match found, return original but cleaned up
    return tool.strip()


def get_known_tools() -> Dict[str, List[str]]:
    """Get list of all known tool variations."""
    all_tools = {}
    for category, standards in TOOL_STANDARDS.items():
        all_tools[category] = list(standards.keys())
    return all_tools
