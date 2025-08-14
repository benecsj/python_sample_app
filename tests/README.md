# Test Suite (Generic)

This directory contains a generic test suite using a unified testing framework and YAML-based test data.

## Test Organization
- **Unit Tests** (`tests/unit/`)
- **Feature Tests** (`tests/feature/`)
- **Integration Tests** (`tests/integration/`)
- **Example Tests** (`tests/example/`)

## Test File Structure
Each test module pairs 1:1 with a YAML file by base name:
- `test_<id>_<short>.py`
- `test_<id>_<short>.yml`

## YAML Structure
Multi-document YAML separated by `---`:

1. Test Metadata
```yaml
test:
  name: "Test Name"
  description: "Description"
  category: "unit|feature|integration|example"
  id: "101"
```

2. Source Files (optional for example tests)
```yaml
source_files:
  any.txt: |
    content
```

3. Config (required when source_files present)
```yaml
config.json: |
  {
    "test": "Hello World",
    "output_dir": "./output"
  }
```

4. Assertions
```yaml
assertions:
  execution:
    exit_code: 0
    max_execution_time: 30.0
  files:
    output_dir_exists: ./output
    files_exist:
      - ./output/output.txt
    file_content:
      ./output/output.txt:
        contains: ["Hello World"]
        line_count: 1
```

## Running Tests
- Linux/macOS: `./scripts/run_all_tests.sh`
- Windows: `scripts/run_all_tests.bat`
- Cross-platform: `python scripts/run_all_tests.py`