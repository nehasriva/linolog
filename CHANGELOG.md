# Changelog

All notable changes to LinoLog will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Enhanced folder watching with robust dropped-in folder detection
- LLM integration for enhanced color and tag analysis
- Tools normalization utility for standardizing tool names
- Periodic scanning backup detection mechanism
- Better error handling and logging
- Comprehensive documentation updates

### Changed
- Refactored tools normalizer from agent to utility function
- Improved folder detection with 2-second delay and duplicate prevention
- Enhanced event filtering to ignore parent directory events
- Updated processing flow with better user feedback

### Fixed
- Folder watcher now properly detects dropped-in folders
- Fixed race conditions in folder processing
- Improved handling of permission and access errors
- Better duplicate prevention for folder processing

## [1.0.0] - 2024-01-XX

### Added
- Initial release of LinoLog
- Core folder watching functionality
- Google Sheets integration
- Agent system with metadata filler, color detection, and tag generation
- YAML metadata support
- Configuration management
- Processing tracking to prevent duplicates

### Features
- **Metadata Filler Agent**: Extracts title and edition from folder names
- **Color Agent**: K-means clustering for color detection
- **Tag Agent**: Generates searchable tags based on metadata
- **Google Sheets Integration**: Structured logging with proper headers
- **YAML Support**: Optional metadata files for manual overrides
- **Modular Design**: Toggle agents on/off via configuration

### Technical Details
- Python 3.8+ compatibility
- Environment-based configuration
- Comprehensive logging
- Error handling and recovery
- Cross-platform support

---

## Version History

- **1.0.0**: Initial release with core functionality
- **Unreleased**: Enhanced folder watching, LLM integration, tools normalization

## Contributing

To add entries to this changelog:

1. **Added**: for new features
2. **Changed**: for changes in existing functionality
3. **Deprecated**: for soon-to-be removed features
4. **Removed**: for now removed features
5. **Fixed**: for any bug fixes
6. **Security**: in case of vulnerabilities

## Release Process

1. Update version in relevant files
2. Add entries to this changelog
3. Create a git tag for the version
4. Create a GitHub release with release notes 