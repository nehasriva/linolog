# Contributing to LinoLog

Thank you for your interest in contributing to LinoLog! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Issues

Before creating an issue, please:

1. **Search existing issues** to see if your problem has already been reported
2. **Check the documentation** to see if your question is answered there
3. **Provide detailed information** when creating a new issue:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)
   - Relevant logs or error messages

### Suggesting Features

We welcome feature suggestions! When suggesting a feature:

1. **Check existing issues** to see if it's already been suggested
2. **Provide clear use cases** explaining why the feature would be useful
3. **Consider the impact** on existing functionality
4. **Think about implementation** - is it feasible with the current architecture?

### Code Contributions

#### Development Setup

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/nehasriva/linolog.git
   cd linolog
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install the package with dev dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```
5. **Set up your environment**:
   ```bash
   cp env.example .env
   # Edit .env with your settings
   ```

#### Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes** following the coding standards below
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Commit your changes** with a clear message:
   ```bash
   git commit -m "Add feature: brief description"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a pull request**

#### Coding Standards

- **Python**: Follow PEP 8 style guidelines
- **Documentation**: Add docstrings to new functions and classes
- **Testing**: Add tests for new functionality when possible
- **Logging**: Use appropriate log levels and meaningful messages
- **Error Handling**: Include proper exception handling
- **Type Hints**: Use type hints for function parameters and return values

#### Pull Request Guidelines

1. **Clear title** describing the change
2. **Detailed description** of what was changed and why
3. **Reference related issues** using keywords like "Fixes #123"
4. **Include tests** if adding new functionality
5. **Update documentation** if changing user-facing features
6. **Screenshots** for UI changes (if applicable)

## 🏗️ Project Structure

### Core Components

- `src/linolog/main.py`: Application entry point
- `src/linolog/config.py`: Configuration management
- `src/linolog/processor.py`: Main orchestration logic
- `src/linolog/folder_watcher.py`: Folder monitoring system
- `src/linolog/metadata_loader.py`: YAML metadata parsing
- `src/linolog/sheet_writer.py`: Google Sheets integration
- `src/linolog/tools_normalizer.py`: Tool name standardization

### Agent System

- `src/linolog/agents/base_agent.py`: Base class for all agents
- `src/linolog/agents/metadata_filler.py`: Fills missing metadata
- `src/linolog/agents/color_agent.py`: Traditional color detection
- `src/linolog/agents/llm_color_agent.py`: LLM-enhanced color analysis
- `src/linolog/agents/tag_agent.py`: Traditional tag generation
- `src/linolog/agents/llm_tag_agent.py`: LLM-enhanced tag generation

### Adding New Agents

1. **Create a new file** in the `src/linolog/agents/` directory
2. **Inherit from `BaseAgent`**:
   ```python
   from .base_agent import BaseAgent
   
   class YourAgent(BaseAgent):
       def process(self, metadata: Dict[str, Any], folder_path: str) -> Dict[str, Any]:
           # Your processing logic here
           return metadata
   ```
3. **Add to processor** in `src/linolog/processor.py`
4. **Add configuration option** in `src/linolog/config.py`
5. **Update documentation**

### Adding New Utilities

1. **Create a standalone file** (like `tools_normalizer.py`)
2. **Keep it focused** on a single responsibility
3. **Add proper documentation**
4. **Integrate into the processing pipeline** if needed

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=linolog

# Run specific test file
python -m pytest tests/test_processor.py
```

### Writing Tests

- **Test new functionality** thoroughly
- **Use descriptive test names**
- **Mock external dependencies** (Google Sheets API, file system)
- **Test edge cases** and error conditions
- **Keep tests fast** and focused

## 📝 Documentation

### Code Documentation

- **Docstrings**: Use Google-style docstrings
- **Type hints**: Include for all function parameters
- **Comments**: Explain complex logic
- **README**: Keep installation and usage instructions current

### API Documentation

- **Clear examples** for all public functions
- **Parameter descriptions** with types and constraints
- **Return value documentation**
- **Error handling** documentation

## 🚀 Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. **Update version** in relevant files
2. **Run all tests** to ensure everything works
4. **Update documentation** if needed
5. **Create release notes** on GitHub
6. **Tag the release** with version number

## 🤝 Community Guidelines

### Be Respectful

- **Be kind** and respectful to all contributors
- **Assume good intentions** in discussions
- **Provide constructive feedback**
- **Help newcomers** get started

### Communication

- **Use clear language** in issues and PRs
- **Provide context** for your suggestions
- **Ask questions** if something is unclear
- **Be patient** with responses

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check README and project files first

## 🙏 Recognition

Contributors will be recognized in:

- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributors** page

Thank you for contributing to LinoLog! 🎨 