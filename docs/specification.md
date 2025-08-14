# python_sample_app – Component Specification

This repository provides a minimal Python sample application and a generic testing framework.

## Functional Requirements
- The application accepts a configuration path via `--config` pointing to either a JSON file or a folder.
- When a folder is provided, all `*.json` files are merged (later files override earlier keys).
- Configuration keys:
  - `test` (string, default: "Hello World"): the message to write
  - `output_dir` (string, default: `./output`): output directory for artifacts
- On execution, the application creates `output_dir` if missing and writes `output.txt` containing the `test` value followed by a newline.

## Non-Functional Requirements
- Cross-platform operation (Linux, macOS, Windows) when run with Python 3.8+.
- Minimal dependencies; standard library only for the CLI.

## Testing Framework
- YAML-driven tests with generic validators for:
  - CLI execution (exit code, stdout/stderr contains, timing)
  - File system checks (existence, content, UTF-8 validation)
  - Log content checks
- Example tests may provide only assertions and rely on external `config.json`.
