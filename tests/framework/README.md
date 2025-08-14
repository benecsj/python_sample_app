# Test Framework (Generic)

This directory contains the unified testing framework for generic CLI/file tests. The framework provides a standardized approach to testing via YAML assertions.

## Simple pattern
```python
class TestSomething(UnifiedTestCase):
	def test_something(self):
		result = self.run_test("101_some_test")
		self.validate_execution_success(result)
		self.validate_test_output(result)
```

## Components
- `UnifiedTestCase`: Base class with helpers
- `TestDataLoader`: Loads YAML test data and creates temp files
- `TestExecutor`: Runs `main.py` with `--config`
- `ValidatorsProcessor`: Applies `execution` and `files` assertions
- Validators:
  - `CLIValidator`: exit code/stdout/stderr/time checks
  - `OutputValidator`: file/dir and content checks
  - `FileValidator`: UTF-8 and equality checks

## YAML assertions (supported)
```yaml
assertions:
  execution:
    exit_code: 0
    stdout_contains: "..."
    stderr_contains: "..."
    max_execution_time: 30.0
  files:
    output_dir_exists: ./output
    files_exist: [./output/output.txt]
    files_not_exist: [./output/extra.txt]
    utf8_files: [./output/output.txt]
    file_content:
      ./output/output.txt:
        contains: ["Hello World"]
        not_contains: ["ERROR"]
        contains_lines: ["Hello World"]
        line_count: 1
        not_empty: true
```
