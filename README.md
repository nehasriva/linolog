# LinoLog - Linocut Print Metadata Logger

A lightweight, Python-based, agent-assisted logging system that watches a folder for new linocut print drops, auto-generates metadata, and logs everything into a structured Google Sheet.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

## ✨ Features

- 🖼️ **Smart Folder Watching**: Automatically detects new print folders with robust handling for dropped-in folders
- 🧠 **AI Agents**: Metadata filler, color detection, tag suggestions, and LLM-enhanced analysis
- 📊 **Google Sheets Integration**: Structured logging with editable rows
- 🔧 **Modular Design**: Toggle agents on/off via configuration
- 📝 **YAML Support**: Optional metadata files for manual overrides
- 🛠️ **Tools Normalization**: Standardizes tool names across different variations
- 🤖 **LLM Integration**: Optional LLM-powered color and tag analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Cloud account (for Google Sheets API)
- Optional: LLM API key (OpenAI, Anthropic, etc.) for enhanced analysis

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nehasriva/linolog.git
   cd linolog
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Service Account**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Google Sheets API:
     - Go to "APIs & Services" > "Library"
     - Search for "Google Sheets API" and enable it
   - Create Service Account:
     - Go to "APIs & Services" > "Credentials"
     - Click "Create Credentials" > "Service Account"
     - Fill in details and create
   - Download JSON key:
     - Click on the service account
     - Go to "Keys" tab
     - Click "Add Key" > "Create new key" > "JSON"
     - Download and save as `creds.json` in project root
   - Create Google Sheet and share with service account email

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run the system**
   ```bash
   python main.py
   ```

## 📁 Folder Structure

```
~/LinocutArchive/
├── redwoods_edition_5/
│   ├── final_print.jpg
│   ├── layers/
│   └── metadata.yaml  ← optional
```

## 📊 Metadata Fields

### Required Fields
- `title`: Print title
- `date`: Creation date
- `edition`: Number of editions
- `size`: Print dimensions
- `medium`: Print medium (usually "Linocut")
- `paper_type`: Type of paper used
- `blocks_used`: Number of blocks used

### Optional Fields
- `paper_width`: Paper weight/thickness
- `mounted`: Whether print is mounted
- `combined_pieces`: Number of combined pieces
- `reduction`: Whether it's a reduction print
- `carving_tools`: Tools used for carving (auto-normalized)
- `brayer_type`: Type of brayer used (auto-normalized)
- `burnish_type`: Burnishing method (auto-normalized)
- `colors_used`: Colors in the print (auto-detected)
- `series`: Series name for grouping related prints
- `tags`: Searchable tags (auto-generated)
- `notes`: Additional notes

## 🤖 Agent System

### Metadata Filler Agent
- Fills in missing required fields using heuristics
- Extracts title and edition from folder name
- Suggests default values for missing fields

### Color Agents
- **Traditional Color Agent**: Uses K-means clustering for color detection
- **LLM Color Agent**: Enhanced analysis using LLM for more accurate color identification
- Analyzes final print image for color detection
- Suggests color names for the `colors_used` field

### Tag Agents
- **Traditional Tag Agent**: Generates searchable tags based on metadata
- **LLM Tag Agent**: Enhanced tag generation using LLM for better categorization
- Suggests tags for style, subject, technique, etc.
- Helps with organization and searchability

### Tools Normalizer
- **Not an agent**: Direct utility function for tool standardization
- Normalizes tool names across different variations
- Supports: carving tools, brayer types, burnish types, paper types
- Converts variations like "pfeil" → "pfeil", "flex cut" → "flexcut"

## 🔍 Enhanced Folder Watching

The system now includes robust folder detection:

- **Dropped-in folders**: Handles folders moved/copied into the watch directory
- **Delayed processing**: 2-second delay ensures folders are fully copied
- **Duplicate prevention**: Prevents processing the same folder multiple times
- **Periodic scanning**: Backup detection mechanism every 5 seconds
- **Better error handling**: Graceful handling of permission and access issues

## ⚙️ Configuration

Edit `.env` to customize behavior:

```env
# Google Sheets
GOOGLE_SHEET_ID=your_sheet_id_here
GOOGLE_SHEET_NAME=Sheet1

# Agents
ENABLE_METADATA_FILLER=true
ENABLE_COLOR_AGENT=true
ENABLE_LLM_COLOR_AGENT=true
ENABLE_TAG_AGENT=true
ENABLE_LLM_TAG_AGENT=true
ENABLE_TOOLS_NORMALIZER=true

# LLM Configuration (optional)
LLM_API_KEY=your_llm_api_key_here
LLM_MODEL=gpt-4-vision-preview

# Folder Watching
WATCH_DIRECTORY=/LinocutArchive
```

## 📝 Usage

1. **Drop a new print folder** into `~/LinocutArchive/`
2. **Run the system**: `python main.py`
3. **System automatically**:
   - Detects the new folder (with 2-second delay)
   - Loads existing metadata if present
   - Runs enabled agents for enhancement
   - Normalizes tool names
   - Prompts for missing required fields
   - Adds row to Google Sheet
4. **Check Google Sheet** for new row with metadata

## 🔄 Processing Flow

1. **Folder Detection**: Robust detection of dropped-in folders
2. **Metadata Loading**: Loads from YAML file if present
3. **Agent Processing**: Runs enabled agents in sequence
4. **Tools Normalization**: Standardizes tool names
5. **Validation**: Ensures required fields are present
6. **User Review**: Prompts for missing/incorrect data
7. **Sheet Writing**: Adds structured data to Google Sheets

## 🛠️ Troubleshooting

### Common Issues

- **Service Account Issues**: Ensure the service account email has edit access to your Google Sheet
- **Missing Dependencies**: Run `pip install -r requirements.txt`
- **Permission Errors**: Check folder permissions for `/LinocutArchive/`
- **LLM Issues**: Ensure API key is set if using LLM agents
- **Folder Detection**: Check logs for detailed event information

### Debug Mode

Enable detailed logging by setting the log level in your `.env`:

```env
LOG_LEVEL=DEBUG
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📋 Development

The system is modular and extensible:

- **Add new agents**: Create files in `agents/` directory implementing `BaseAgent`
- **Add new utilities**: Create standalone functions like `tools_normalizer.py`
- **Modify processing**: Edit `processor.py` for custom workflows
- **Extend normalization**: Add new categories to `TOOL_STANDARDS` in `tools_normalizer.py`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for the linocut printmaking community
- Inspired by the need for better print documentation
- Thanks to all contributors and users

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/nehasriva/linolog/issues)
- **Discussions**: [GitHub Discussions](https://github.com/nehasriva/linolog/discussions)
- **Documentation**: [Wiki](https://github.com/nehasriva/linolog/wiki)

---

**Made with ❤️ for the printmaking community** 