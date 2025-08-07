# C2PUML Test Framework - Component Responsibilities

This document outlines the responsibilities of each component in the unified testing framework to ensure clear separation of concerns and avoid duplication.

## Test Folder Structure

### New Test Organization
Each test creates a dedicated folder structure for isolation and clarity:

```
tests/
├── unit/
│   ├── test_simple_c_file_parsing.py
│   ├── test_simple_c_file_parsing.yml
│   └── test-simple_c_file_parsing/          # Generated during test execution
│       ├── input/
│       │   ├── config.json
│       │   └── src/
│       │       └── simple.c
│       └── output/
│           ├── model.json
│           ├── model_transformed.json
│           └── simple.puml
├── feature/
│   └── test-###/                            # Similar structure for each test
├── integration/
│   └── test-###/                            # Similar structure for each test
└── example/
    ├── test_basic_example.py
    ├── test_basic_example.yml               # Contains ONLY assertions
    ├── config.json                          # External config file (tracked by git)
    ├── source/                              # External source folder (tracked by git)
    │   ├── main.c
    │   └── header.h
    └── test-basic_example/                  # Generated during test execution
        └── output/                          # Only output folder for example tests
            ├── model.json
            ├── model_transformed.json
            └── example.puml
```

### Test Types and Structures

#### **Standard Tests** (Unit, Feature, Integration)
- **YAML Content**: Complete with source_files, config.json, and assertions
- **Temp Files**: Creates input/ and output/ folders
- **Source Files**: Embedded in YAML, generated as temporary files
- **Config**: Embedded in YAML, generated as temporary config.json

#### **Example Tests** (Special Structure)
- **YAML Content**: Only test metadata and assertions
- **Temp Files**: Creates only output/ folder
- **Source Files**: External source/ folder (tracked by git)
- **Config**: External config.json file (tracked by git)

### Folder Structure Details
- **`test-###/`**: Test-specific folder created during execution (git-ignored)
  - **`input/`**: Contains all input files for the test (standard tests only)
    - `config.json`: c2puml configuration
    - `src/`: Source files (C, H files)
  - **`output/`**: Contains all generated output files
    - `model.json`: Parsed model
    - `model_transformed.json`: Transformed model
    - `*.puml`: PlantUML diagram files

### Git Integration
- **Ignored**: All `test-###/` folders (generated during test execution)
- **Tracked**: Test files (`test_*.py`, `test_*.yml`)
- **Example Tests**: External `config.json` and `source/` folders are tracked
- **Cleanup**: Existing test folders are automatically deleted before each test run

## Framework Components

### 1. `base.py` - UnifiedTestCase Base Class
**Primary Responsibility**: Test setup, teardown, and component initialization

**Responsibilities**:
- ✅ Initialize framework components (executor, data_loader, assertion_processor, validators)
- ✅ Create temporary directories for test execution
- ✅ Provide component access to all validators and framework components

**What it does NOT do**:
- ❌ Create test files (handled by `data_loader.py`)
- ❌ Process complex assertions (handled by `assertion_processor.py`)
- ❌ Execute c2puml (handled by `executor.py`)
- ❌ Validate specific content (handled by `validators.py`)
- ❌ Provide assertion methods (handled by validators)

### 2. `data_loader.py` - TestDataLoader
**Primary Responsibility**: Load test data from YAML and create temporary files

**Responsibilities**:
- ✅ Load multi-document YAML test files
- ✅ Parse YAML documents into structured test data
- ✅ Validate YAML structure and content
- ✅ **Standard Tests**: Create temporary source files and config.json from YAML content
- ✅ **Example Tests**: Use external config.json and source/ folder (no temp files created)
- ✅ Manage test-specific temp directories:
  - Standard tests: `tests/*/test-<id>/` with input/ and output/ folders
  - Example tests: `tests/example/test-<id>/` with output/ folder only
- ✅ Support meaningful test IDs and file discovery
- ✅ Automatically clean up existing test folders before creation

**What it does NOT do**:
- ❌ Execute tests (handled by test classes)
- ❌ Process assertions (handled by `assertion_processor.py`)
- ❌ Validate output (handled by `validators.py`)

### 3. `executor.py` - TestExecutor
**Primary Responsibility**: Execute c2puml via CLI interface

**Responsibilities**:
- ✅ Execute c2puml through CLI interface only (no internal API access)
- ✅ Support different execution modes:
  - `run_full_pipeline()` - Complete workflow
  - `run_parse_only()` - Parse step only
  - `run_transform_only()` - Transform step only
  - `run_generate_only()` - Generate step only
- ✅ **Working Directory Management**:
  - Standard tests: Uses temp input directory as working directory
  - Example tests: Uses example directory (where config.json is located)
- ✅ Provide execution results (CLIResult)
- ✅ Support verbose output and environment variables
- ✅ Manage command building and execution

**What it does NOT do**:
- ❌ Load test data (handled by `data_loader.py`)
- ❌ Create files (handled by `data_loader.py`)
- ❌ Process assertions (handled by `assertion_processor.py`)
- ❌ Validate output (handled by `validators.py`)

### 4. `assertion_processor.py` - AssertionProcessor
**Primary Responsibility**: Process assertions from YAML data

**Responsibilities**:
- ✅ Process execution assertions (exit codes, output files)
- ✅ Process model validation assertions (structs, enums, functions, etc.)
- ✅ Process PlantUML validation assertions (content, syntax)
- ✅ Apply assertions using appropriate validators
- ✅ Handle YAML assertion structure (execution, model, puml sections)

**What it does NOT do**:
- ❌ Load test data (handled by `data_loader.py`)
- ❌ Execute c2puml (handled by `executor.py`)
- ❌ Provide basic assertions (handled by validators)
- ❌ Validate specific content (handled by `validators.py`)

### 5. `validators.py` - Validation Classes
**Primary Responsibility**: Validate specific types of content and files

**Responsibilities**:
- ✅ **ModelValidator**: Validate model.json structure and content
  - Struct existence and fields
  - Enum existence and values
  - Function existence
  - Global variable existence
  - Include file existence
  - Element counts
- ✅ **PlantUMLValidator**: Validate .puml files and content
  - File existence and syntax
  - Content validation
  - Class and relationship validation
- ✅ **OutputValidator**: Validate general output files and directories
  - File existence and content
  - Directory structure
  - Log validation
  - **C2PUML-specific output validation**:
    - `assert_model_file_exists()` - Check for model.json
    - `assert_transformed_model_file_exists()` - Check for model_transformed.json
    - `assert_puml_files_exist()` - Check for .puml files
- ✅ **FileValidator**: Advanced file operations
  - File comparison
  - JSON validation
  - UTF-8 validation
  - Whitespace validation
- ✅ **CLIValidator**: Validate CLI execution results
  - `assert_cli_success()` - Verify successful execution
  - `assert_cli_failure()` - Verify expected failures
  - `assert_cli_exit_code()` - Check specific exit codes
  - `assert_cli_stdout_contains()` - Check stdout content
  - `assert_cli_stderr_contains()` - Check stderr content
  - `assert_cli_execution_time_under()` - Check execution time

**What it does NOT do**:
- ❌ Load test data (handled by `data_loader.py`)
- ❌ Execute c2puml (handled by `executor.py`)
- ❌ Process assertions (handled by `assertion_processor.py`)
- ❌ Provide test setup (handled by `base.py`)

### 6. `__init__.py` - Package Initialization
**Primary Responsibility**: Package setup and exports

**Responsibilities**:
- ✅ Import all framework components
- ✅ Define `__all__` for package exports
- ✅ Provide clean import interface for tests

## Responsibility Separation Rules

### ✅ **Good Separation**
- Each component has a single, well-defined responsibility
- Components use other components through their public interfaces
- No circular dependencies between components
- Clear data flow: data_loader → executor → validators → assertion_processor

### ❌ **Avoided Overlaps**
- **File Creation**: Only `data_loader.py` creates files
- **Assertion Processing**: Only `assertion_processor.py` processes complex assertions
- **Execution**: Only `executor.py` executes c2puml
- **Validation**: Only `validators.py` validates specific content
- **Test Setup**: Only `base.py` handles test setup and component initialization

### 🔄 **Data Flow**
```
Test Class
    ↓
base.py (setup) → data_loader.py (load data) → executor.py (execute) → validators.py (validate) → assertion_processor.py (process assertions)
```

## Usage Patterns

### Standard Test Implementation
```python
class TestExample(UnifiedTestCase):
    def test_something(self):
        # 1. Load test data (data_loader.py responsibility)
        test_data = self.data_loader.load_test_data("test_id")
        source_dir, config_path = self.data_loader.create_temp_files(test_data, "test_id")
        
        # 2. Get folder structure
        test_folder = os.path.dirname(source_dir)  # input/ folder
        test_dir = os.path.dirname(test_folder)    # test-###/ folder
        
        # 3. Execute c2puml (executor.py responsibility)
        config_filename = os.path.basename(config_path)
        result = self.executor.run_full_pipeline(config_filename, test_folder)
        
        # 4. Basic CLI validation (CLIValidator responsibility)
        self.cli_validator.assert_cli_success(result)
        
        # 5. Load output for validation (OutputValidator responsibility)
        output_dir = os.path.join(test_dir, "output")
        model_file = self.output_validator.assert_model_file_exists(output_dir)
        puml_files = self.output_validator.assert_puml_files_exist(output_dir)
        
        # 6. Load content for validation
        model_data = json.load(open(model_file))
        puml_content = open(puml_files[0]).read()
        
        # 7. Process assertions (assertion_processor.py responsibility)
        self.assertion_processor.process_assertions(
            test_data["assertions"], model_data, puml_content, result, self
        )
```

### Example Test Implementation
```python
class TestBasicExample(UnifiedTestCase):
    def test_basic_example(self):
        # 1. Load test data (data_loader.py responsibility) - assertions only
        test_data = self.data_loader.load_test_data("basic_example")
        
        # 2. Get the example directory (where config.json and source/ are located)
        example_dir = os.path.dirname(__file__)
        
        # 3. Execute c2puml (executor.py responsibility)
        result = self.executor.run_full_pipeline("config.json", example_dir)
        
        # 4. Basic CLI validation (CLIValidator responsibility)
        self.cli_validator.assert_cli_success(result)
        
        # 5. Load output for validation (OutputValidator responsibility)
        test_dir = os.path.join(example_dir, "test-basic_example")
        output_dir = os.path.join(test_dir, "output")
        model_file = self.output_validator.assert_model_file_exists(output_dir)
        puml_files = self.output_validator.assert_puml_files_exist(output_dir)
        
        # 6. Load content for validation
        model_data = json.load(open(model_file))
        puml_content = open(puml_files[0]).read()
        
        # 7. Process assertions (assertion_processor.py responsibility)
        self.assertion_processor.process_assertions(
            test_data["assertions"], model_data, puml_content, result, self
        )
```

## Validator Usage Examples

### CLIValidator
```python
# Check successful execution
self.cli_validator.assert_cli_success(result)

# Check expected failure
self.cli_validator.assert_cli_failure(result, expected_error="Config file not found")

# Check specific exit code
self.cli_validator.assert_cli_exit_code(result, 1)

# Check stdout/stderr content
self.cli_validator.assert_cli_stdout_contains(result, "Processing complete")
self.cli_validator.assert_cli_stderr_contains(result, "Warning")
```

### OutputValidator
```python
# Check C2PUML output files
model_file = self.output_validator.assert_model_file_exists(output_dir)
transformed_file = self.output_validator.assert_transformed_model_file_exists(output_dir)
puml_files = self.output_validator.assert_puml_files_exist(output_dir, min_count=2)

# Check general files
self.output_validator.assert_file_exists("some_file.txt")
self.output_validator.assert_file_contains("log.txt", "Success")
```

## Key Concepts

### Test Isolation
- Each test creates its own dedicated folder structure
- No interference between tests
- Automatic cleanup of existing test folders
- Clear separation of input and output files

### Framework Flexibility
- Supports both embedded (standard tests) and external (example tests) file structures
- YAML-based configuration with multi-document support
- Comprehensive validation framework
- CLI-only execution for public API testing

### Git Integration
- Generated test folders are properly ignored
- External files for example tests are tracked
- Clean repository without temporary files
- Easy to understand what's tracked vs. generated

This clear separation ensures maintainability, testability, and prevents duplication of responsibilities across the framework.