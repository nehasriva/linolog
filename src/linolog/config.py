import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for LinoLog application."""

    # Google Sheets Configuration
    GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
    GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "Sheet1")

    # Folder Watching
    WATCH_DIRECTORY = os.getenv(
        "WATCH_DIRECTORY", os.path.expanduser("~/LinocutArchive")
    )

    # Agent Configuration
    ENABLE_METADATA_FILLER = (
        os.getenv("ENABLE_METADATA_FILLER", "true").lower() == "true"
    )
    ENABLE_COLOR_AGENT = os.getenv("ENABLE_COLOR_AGENT", "true").lower() == "true"
    ENABLE_TAG_AGENT = os.getenv("ENABLE_TAG_AGENT", "true").lower() == "true"
    ENABLE_TOOLS_NORMALIZER = (
        os.getenv("ENABLE_TOOLS_NORMALIZER", "true").lower() == "true"
    )

    # LLM Configuration
    ENABLE_LLM = os.getenv("ENABLE_LLM", "false").lower() == "true"
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")  # 'openai' or 'anthropic'
    ENABLE_LLM_COLOR_AGENT = (
        os.getenv("ENABLE_LLM_COLOR_AGENT", "true").lower() == "true"
    )
    ENABLE_LLM_TAG_AGENT = os.getenv("ENABLE_LLM_TAG_AGENT", "true").lower() == "true"

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "linolog.log")

    # Processing
    PROCESSED_LOG_FILE = os.getenv("PROCESSED_LOG_FILE", "processed_folders.txt")

    # Required metadata fields
    REQUIRED_FIELDS = [
        "title",
        "date",
        "edition",
        "size",
        "medium",
        "paper_type",
        "blocks_used",
    ]

    # Google Sheets column headers
    SHEET_HEADERS = [
        "Title",
        "Date",
        "No. of Editions",
        "Size",
        "Medium",
        "Paper Type",
        "Paper Width",
        "Mounted",
        "Combined Pieces",
        "Blocks Used",
        "Reduction",
        "Carving Tools",
        "Brayer Type",
        "Burnish Type",
        "Colors Used",
        "Series",
        "Tags",
        "Notes",
    ]

    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present."""
        missing = []

        if not cls.GOOGLE_SHEET_ID:
            missing.append("GOOGLE_SHEET_ID")

        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")

        return True
