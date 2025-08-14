# python_sample_app - Python Development Starter

A minimal Python sample application demonstrating a clean repository structure, scripts, and a general-purpose test framework. The CLI reads a JSON configuration and writes `output.txt` with the configured message.

## Features
- Simple, dependency-light CLI
- Works with config file or config folder (merges all `*.json` files)
- Cross-platform scripts for running tests and examples
- Unified testing framework with generic validators (CLI, file, and log checks)

## Quick Start

### Run from source
```bash
python3 main.py --config tests/example/config.json
```

You can also omit `--config` to read JSON files from the current directory:
```bash
python3 main.py
```

### As an installed package (optional)
Add an entry point is provided as `python_sample_app`:
```bash
pip install -e .
python_sample_app --config tests/example/config.json
```

## Configuration
Provide a JSON config file or a folder containing JSON files to be merged. The application supports:
- `test` (string): message to write to `output.txt` (default: "Hello World")
- `output_dir` (string): where to write `output.txt` (default: `./output`)

Example `config.json`:
```json
{
  "test": "Hello World",
  "output_dir": "./output"
}
```

## What it does
- Resolves the configuration (file or folder)
- Ensures the `output_dir` exists
- Writes `output.txt` with the `test` value followed by a newline

## Development

### Create a venv and install dev deps
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pip install -e .
```

### Scripts
- Run tests (unittest by default):
  - Linux/macOS: `./scripts/run_all_tests.sh`
  - Windows: `scripts/run_all_tests.bat`
  - Cross-platform: `python scripts/run_all_tests.py`
- Run tests with coverage (if coverage/pytest installed):
  - `./scripts/run_tests_with_coverage.sh`
- Run the example:
  - Linux/macOS: `./scripts/run_example.sh`
  - Windows: `scripts/run_example.bat`

## Troubleshooting
- Ensure you run from repository root so `src/` is on PYTHONPATH (or install in editable mode).
- Pass an explicit `--config` path if running outside the repo root.

## License
MIT License


