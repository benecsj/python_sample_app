# python_sample_app - Sample python app

## Status
[![Run Tests](https://github.com/fischerjooo/c2puml/actions/workflows/test.yml/badge.svg)](https://github.com/fischerjooo/c2puml/actions/workflows/test.yml)
[![Coverage Reports](https://github.com/fischerjooo/c2puml/actions/workflows/test-coverage.yml/badge.svg)](https://github.com/fischerjooo/c2puml/actions/workflows/test-coverage.yml)
[![Deploy Website](https://github.com/fischerjooo/c2puml/actions/workflows/deploy-website.yml/badge.svg)](https://github.com/fischerjooo/c2puml/actions/workflows/deploy-website.yml)

## Reports

- [📊 Combined Coverage Report](https://fischerjooo.github.io/c2puml/artifacts/coverage/htmlcov/index.html) - Comprehensive coverage report with summary and detailed per-file analysis
- [📝 Test Summary](https://fischerjooo.github.io/c2puml/artifacts/test_reports/test_summary.html) - Test execution summary and statistics

## Documentation

- [📖 Specification](https://github.com/fischerjooo/c2puml/blob/main/docs/specification.md) - Complete technical specification and architecture documentation

## Releases

- [📦 Download ZIP](https://github.com/fischerjooo/c2puml/archive/refs/heads/release.zip) - Download the latest release as ZIP archive
- [📦 Download TAR.GZ](https://github.com/fischerjooo/c2puml/archive/refs/heads/release.tar.gz) - Download the latest release as TAR.GZ archive

## Features

## Installation

### Option 1: Install as Python Package (Recommended)

```bash
git clone https://github.com/fischerjooo/c2puml.git
cd c2puml
python3 -m pip install -e .
```

### Option 2: Use Standalone Script (No Installation Required)

If you prefer not to install the package, you can use the standalone script directly:

```bash
git clone https://github.com/fischerjooo/c2puml.git
cd c2puml
# No installation needed - just run the script directly
python3 main.py --config tests/example/config.json
```

**Prerequisites for standalone usage:**
- Python 3.7 or later
- The complete c2puml source code (including the `src/` directory)

## Quick Start

### Basic Usage

#### Using Installed Package

#### Using Standalone Script (No Installation)

**Note**: Both methods provide identical functionality. Choose the one that best fits your workflow.

### Installation vs Standalone: Which to Choose?

| Feature | Installed Package | Standalone Script |
|---------|-------------------|-------------------|
| **Installation** | `pip install -e .` | None required |
| **Command** | `c2puml` | `python3 main.py` |
| **Portability** | System dependent | High (copy files) |
| **Updates** | `pip install --upgrade` | Manual (update source) |
| **Dependencies** | Automatic via pip | Manual management |
| **Development** | Good | Excellent |
| **CI/CD Integration** | Standard | Easy |
| **Distribution** | Package distribution | Source required |

**Choose installed package if:**
- You plan to use c2puml regularly
- You want automatic dependency management
- You prefer standard Python package workflows

**Choose standalone script if:**
- You want to try c2puml without installation
- You're in a restricted environment
- You need maximum portability
- You're doing development or testing


## Generated Output


## Architecture

**1-step processing pipeline with modular core components:**

### Core Components

## Development Setup

### Manual Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -r requirements-dev.txt

# Install package in development mode
pip install -e .
```

### VSCode Configuration

The project includes pre-configured VSCode settings for:
- Python auto-formatting with Black
- Import sorting with isort
- Linting with flake8
- Auto-save and formatting on save

**VSCode Tasks**: The project includes pre-configured tasks accessible via `Ctrl+Shift+P` → "Tasks: Run Task":
- **Run Full Workflow** - Complete analysis and diagram generation (parse → transform → generate)
- **Run Example** - Quick test with example files and comprehensive verification
- **Run Tests** - Execute comprehensive test suite with coverage reporting
- **Format & Lint** - Code quality checks with Black, isort, and flake8


### Development Commands

```bash
# Run all tests
./scripts/run_all_tests.sh     # Linux/macOS
scripts/run_all_tests.bat      # Windows
python scripts/run_all_tests.py # Cross-platform

# Run tests with coverage
./scripts/run_tests_with_coverage.sh # Linux/macOS (comprehensive coverage)

# Format and lint code
scripts/format_lint.bat        # Windows


# Run full workflow (parse → transform → generate)
./scripts/run_all.sh           # Linux/macOS
scripts/run_all.bat            # Windows

# Run example workflow
./scripts/run_example.sh       # Linux/macOS
scripts/run_example.bat        # Windows
# Or use standalone script directly:
python3 main.py --config tests/example/config.json

# Install dependencies
scripts/install_dependencies.bat # Windows

# Git management utilities
scripts/git_manage.bat         # Windows - Interactive git operations
scripts/git_reset_pull.bat     # Windows - Reset and pull from remote

# Debug and development utilities
python scripts/debug.py        # Development debugging script
python scripts/run_example_with_coverage.py # Example with coverage
```

## Troubleshooting

## License

MIT License
