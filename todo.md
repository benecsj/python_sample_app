# C2PUML Test Framework Unification - Todo

## Executive Summary

This document outlines the comprehensive work required to transform the current c2puml test suite (58 test files across unit, feature, integration, and example categories) into a unified, maintainable, and robust testing framework. The primary focus is on **test-application boundary separation** and **public API testing** to ensure the application remains flexible to internal changes.

**Progress Tracking**: This document serves as the central workflow description to track migration progress. All milestones, completion status, and blocking issues should be updated directly in this file.

**📋 Detailed Recommendations**: See `todo_recommendations.md` for comprehensive file-by-file analysis and progress tracking for all 50 test files.

**🗑️ Framework Cleanup**: The existing framework files (`tests/utils.py`, `tests/feature/base.py`) use internal APIs and will be completely removed after migration.

## Current State Analysis

### Current Test Structure
- **58 test files** across 4 categories:
  - `tests/unit/` (37 files) - Individual component tests
  - `tests/feature/` (12 files) - Complete workflow tests  
  - `tests/integration/` (2 files) - End-to-end scenarios
  - `tests/example/` (1 file) - Example project test (to be preserved)
- **Mixed testing approaches**: Some tests use internal functions, others use public APIs
- **Direct internal access**: Many tests directly import and test internal components

### Public API Surface (Target for Testing)
Based on analysis of the codebase, the public APIs are:

1. **CLI Interface** (`main.py`):
   ```bash
   c2puml --config config.json [parse|transform|generate]
   python3 main.py --config config.json [parse|transform|generate]
   ```

2. **Configuration Interface**:
   - JSON configuration files with standardized schema
   - Input: C/C++ source files and headers
   - Output: model.json, transformed_model.json, .puml files

## Work Items

### 1. Unified Testing Framework Design

#### 1.1 Core Testing Framework (`tests/framework/`)
**Priority: HIGH**

Create a new unified framework with these components:

- **`TestExecutor`**: Runs c2puml through public APIs only
- **`TestDataFactory`**: Generates test C/C++ projects and configurations, handles input-##.json files
- **`ResultValidator`**: Validates outputs (model.json, .puml files, logs)
- **`TestProjectBuilder`**: Builds temporary test projects with complex structures

```python
# Framework structure
tests/framework/
├── __init__.py
├── executor.py      # TestExecutor class
├── data_factory.py  # TestDataFactory class  
├── validator.py     # ResultValidator class
├── builder.py       # TestProjectBuilder class
└── fixtures.py      # Common test fixtures
```

#### 1.2 Test Execution Pattern
**Priority: HIGH**

```python
class UnifiedTestCase(unittest.TestCase):
    def setUp(self):
        self.executor = TestExecutor()
        self.data_factory = TestDataFactory()
        self.model_validator = ModelValidator()
        self.puml_validator = PlantUMLValidator()
        self.output_validator = OutputValidator()
        self.test_name = self.__class__.__name__.lower().replace('test', 'test_')
        self.output_dir = tempfile.mkdtemp()
        self.assertions = self.data_factory.load_test_assertions(self.test_name) if self.data_factory.has_test_assertions(self.test_name) else {}
    
    def test_feature(self):
        # Get paths to test data for CLI execution
        input_path = self.data_factory.load_test_input(self.test_name)
        config_path = self.data_factory.load_test_config(self.test_name)
        
        # Execute through CLI interface only
        result = self.executor.run_full_pipeline(input_path, config_path, self.output_dir)
        
        # Validate CLI execution and results
        self.assertEqual(result.exit_code, 0, f"CLI failed: {result.stderr}")
        self.output_validator.assert_output_dir_exists(self.output_dir)
        
        # Load and validate generated files
        model_file = f"{self.output_dir}/model.json"
        self.model_validator.assert_model_json_syntax_valid(model_file)
        
        puml_files = glob.glob(f"{self.output_dir}/*.puml")
        for puml_file in puml_files:
            self.puml_validator.assert_puml_file_syntax_valid(puml_file)
```

### 2. Public API Testing Strategy

#### 2.1 CLI Interface Testing
**Priority: HIGH**

All tests should execute c2puml through the CLI interface only:
- **CLI execution**: `subprocess.run(['python3', 'main.py', '--config', ...])` ✅
- **Individual steps**: `python3 main.py --config config.json [parse|transform|generate]` ✅

**Forbidden**: Direct imports of any internal modules:
- `from c2puml.core.parser import CParser` ❌
- `from c2puml.core.tokenizer import CTokenizer` ❌

**Only Allowed**: CLI interface through main.py

### 3. Test Data Management

#### 3.1 Test Data Factory API
**Priority: MEDIUM**

```python
class TestDataFactory:
    def load_test_input(self, test_name: str) -> str:
        """Returns path to test_<n>/input/ directory for CLI execution"""
    
    def load_test_config(self, test_name: str, input_file: str = None) -> str:
        """Returns path to config.json (explicit) or extracts config from input_file"""
    
    def load_test_assertions(self, test_name: str, input_file: str = None) -> dict:
        """Loads assertion data from assertions.json or from input_file.assertions"""
    
    def create_temp_project(self, input_files: dict) -> str:
        """Creates temporary project and returns path for CLI execution"""
    
    def load_test_input_json(self, test_name: str, input_file: str = "input-01.json") -> dict:
        """Loads input-##.json from test_<n>/input/ and returns parsed content"""
    
    def generate_source_files_from_input(self, test_name: str, input_file: str) -> str:
        """Generates source files from input-##.json and returns input path for CLI"""
    
    def list_input_json_files(self, test_name: str) -> list:
        """Returns list of all input-##.json files in test_<n>/input/ directory"""

class TestExecutor:
    def run_full_pipeline(self, input_path: str, config_path: str, output_dir: str) -> CLIResult:
    def run_parse_only(self, input_path: str, config_path: str, output_dir: str) -> CLIResult:
    def run_transform_only(self, config_path: str, output_dir: str) -> CLIResult:
    def run_generate_only(self, config_path: str, output_dir: str) -> CLIResult:
```

#### 3.2 Test Folder Structure
**Priority: MEDIUM**

**Test Folder Structure Pattern:**
```
test_<n>/
├── test_<n>.py         # Test implementation
├── input/              # Test input files - choose ONE approach per test
│   # Option 1: Explicit files approach (feature tests ALWAYS use this)
│   ├── config.json     # c2puml configuration
│   ├── main.c          # Source files for testing
│   ├── utils.h         # Header files
│   ├── model.json      # Optional: Pre-parsed model for transformation testing
│   └── subdir/         # Optional: Nested directories
│   # Option 2: Input.json approach (NO config.json or source files)
│   ├── input-01.json   # Test case 1: complete config + source + expected results + assertions
│   ├── input-02.json   # Test case 2: complete config + content + expected results + assertions
│   └── input-03.json   # Test case 3: complete config + scenarios + expected results + assertions
└── assertions.json     # Used ONLY with Option 1 (explicit files approach)
```

**Input Strategy Guidelines:**

**FEATURE TESTS and EXAMPLE TESTS ALWAYS use Option 1 (explicit files)** as they test complete workflows and need comprehensive project structures.

**Use input-##.json for:**
- Small unit test cases (< 50 lines of C code total)
- Multiple test scenarios in one test file
- Tests requiring different inputs per method

**Use explicit files for:**
- Feature tests (ALWAYS)
- Example tests (ALWAYS)
- Large test cases (> 50 lines of C code)
- Complex project structures
- Real-world code examples

**Input JSON Structure (meaningful names):**
```json
// Example: input-simple_struct.json
{
  "test_metadata": {
    "description": "Basic struct parsing test",
    "test_type": "unit",
    "expected_duration": "fast"
  },
  "c2puml_config": {
    "project_name": "test_struct_parsing",
    "source_folders": ["."],
    "output_dir": "./output"
  },
  "source_files": {
    "main.c": "C source code content",
    "utils.h": "Header file content"
  },
  "expected_results": {
    "model_elements": {
      "structs": ["Point"],
      "functions": ["main"]
    },
    "plantuml_elements": {
      "classes": ["Point"]
    }
  }
}
```

**Meaningful Input File Naming Examples:**
- `input-simple_struct.json` - Basic structure parsing
- `input-nested_struct.json` - Nested structure handling
- `input-basic_generation.json` - Simple PlantUML generation
- `input-complex_filters.json` - Complex filtering scenarios
- `input-error_handling.json` - Error condition testing
- `input-multipass_anonymous.json` - Multi-pass anonymous processing

### 4. Result Validation Framework

#### 4.1 Validation Components
**Priority: HIGH**

```python
class ModelValidator:
    def assert_model_structure_valid(self, model: dict)
    def assert_model_function_exists(self, model: dict, func_name: str)
    def assert_model_struct_exists(self, model: dict, struct_name: str)
    def assert_model_includes_exist(self, model: dict, expected_includes: list)

class PlantUMLValidator:
    def assert_puml_file_syntax_valid(self, puml_content: str)
    def assert_puml_contains(self, puml_content: str, expected_text: str)
    def assert_puml_class_exists(self, puml_content: str, class_name: str)

class OutputValidator:
    def assert_output_dir_exists(self, output_path: str)
    def assert_file_exists(self, file_path: str)
    def assert_file_contains(self, file_path: str, expected_text: str)
    def assert_log_no_errors(self, log_content: str)
```

### 5. Test Organization and Refactoring

#### 5.1 Test Categorization
**Priority: MEDIUM**

Reorganize 58 test files into clear categories with self-contained test folders:

```
tests/
├── framework/           # New unified testing framework
├── unit/               # Refactored unit tests (public API only)
│   ├── test_parsing/   # Self-contained test folder
│   ├── test_transformation/
│   └── test_generation/
├── feature/            # Refactored feature tests (ALWAYS use explicit files)
│   ├── test_full_workflow/
│   ├── test_include_processing/
│   └── test_transformations/
├── integration/        # Integration tests
│   ├── test_real_projects/
│   └── test_performance/
└── example/            # Keep existing example test (preserved as-is)
```

### 6. Implementation Plan

#### Phase 1: Framework Foundation (Week 1-2)
1. Create `tests/framework/` structure
2. Implement `TestExecutor` with CLI interface
3. Implement `TestDataFactory` with input-##.json support
4. Implement `ResultValidator` for models and PlantUML
5. **Verify baseline**: Run `run_all.sh` to establish current test suite baseline

#### Phase 2: Public API Migration (Week 3-4)
1. Refactor high-priority unit tests to use CLI-only interface
2. Convert appropriate tests to use input-##.json files
3. **Verify migration**: Run `run_all.sh` after each test file migration

#### Phase 3: Test Reorganization (Week 5-6)
1. Create self-contained test folders
2. Migrate test data into respective test folders (preserve `tests/example/`)
3. **Verify reorganization**: Run `run_all.sh` after test structure changes

#### Phase 4: Validation and Cleanup (Week 7-8)
1. Ensure all tests pass with new framework
2. Performance testing of new test suite
3. Remove deprecated test utilities
4. **Final validation**: Run `run_all.sh` for comprehensive verification

### 7. Success Criteria

#### Technical Criteria
- **Zero internal API usage**: All tests use only CLI interface (main.py)
- **100% test pass rate**: All migrated tests pass consistently via `run_all.sh`
- **Maintainable boundaries**: Clear separation between test and application code
- **Consistent patterns**: All tests follow unified structure and naming

#### Quality Criteria
- **Test readability**: Tests are easy to understand and modify
- **Failure diagnostics**: Test failures provide clear guidance
- **Coverage preservation**: No reduction in test coverage during migration
- **Performance**: Test suite execution time via `run_all.sh` remains reasonable

---

## Test Migration Tracking

### Overview
- **Total Test Files**: 48 test files to migrate (excluding preserved example)
- **Unit Tests**: 37 files
- **Feature Tests**: 10 files  
- **Integration Tests**: 2 files
- **Preserved**: 1 file (`tests/example/test-example.py`)

### Migration Status Legend
- ✅ **Completed** - Migrated to unified framework with self-contained structure
- 🔄 **In Progress** - Currently being migrated
- ⏳ **Pending** - Not yet started
- 🚫 **Skipped** - Preserved as-is or deprecated

### Key Migration Constraints

**Feature Tests and Example Tests Strategy:**
- **ALWAYS use Option 1 (explicit files)** - Feature and example tests require comprehensive project structures
- **No input-##.json files** for feature or example tests - they test complete workflows
- All feature and example test files use single `input/` folder with config.json and source files

**Unit Tests Strategy:**
- Use input-##.json for multiple test scenarios
- Use explicit files only when all test methods can share same input

### Critical Split Requirements
1. **test_transformer.py** (80 methods) → 9 files by transformation type
2. **test_tokenizer.py** (41 methods) → 4 files by token category
3. **test_parser_comprehensive.py** (36 methods) → 7 files by C language construct

### Migration Progress Summary

**Analysis Phase Complete**: ✅ Analyzed all 50 test files with detailed recommendations

- **High Priority**: 24 files (including 3 requiring splits)
- **Medium Priority**: 18 files  
- **Low Priority**: 8 files
- **Input JSON Strategy**: 42 files (unit tests only)
- **Explicit Files Strategy**: 8 files (includes all feature tests)

### Unit Tests Progress Tracking (37 files)

| Test File | Status | Priority | Input Strategy | Notes |
|-----------|--------|----------|----------------|-------|
| `test_absolute_path_bug_detection.py` | ⏳ | Medium | input-path_*.json | Path handling validation |
| `test_anonymous_processor_extended.py` | ⏳ | High | input-anonymous_*.json | Core anonymous structure processing |
| `test_anonymous_structure_handling.py` | ⏳ | Medium | input-anonymous_*.json | Anonymous structure handling |
| `test_config.py` | ⏳ | Medium | input-config_*.json | Configuration loading/validation |
| `test_debug_actual_parsing.py` | ⏳ | Low | Explicit files | Debug functionality |
| `test_debug_field_parsing.py` | ⏳ | Low | Explicit files | Debug functionality |
| `test_debug_field_parsing_detailed.py` | ⏳ | Low | Explicit files | Debug functionality |
| `test_debug_field_processing.py` | ⏳ | Low | Explicit files | Debug functionality |
| `test_debug_tokens.py` | ⏳ | Low | Explicit files | Debug functionality |
| `test_file_specific_configuration.py` | ⏳ | Medium | input-fileconfig_*.json | File-specific config handling |
| `test_function_parameters.py` | ⏳ | Medium | input-params_*.json | Function parameter parsing |
| `test_generator.py` | ⏳ | High | input-generation_*.json | Core PlantUML generation |
| `test_generator_duplicate_includes.py` | ⏳ | Low | Explicit files | Include duplication handling |
| `test_generator_exact_format.py` | ⏳ | Low | input-format_*.json | PlantUML formatting validation |
| `test_generator_grouping.py` | ⏳ | Medium | input-grouping_*.json | Element grouping in output |
| `test_generator_include_tree_bug.py` | ⏳ | Medium | input-tree_*.json | Include tree validation |
| `test_generator_naming_conventions.py` | ⏳ | Medium | input-naming_*.json | Naming convention compliance |
| `test_generator_new_formatting.py` | ⏳ | Medium | input-newformat_*.json | New formatting features |
| `test_generator_visibility_logic.py` | ⏳ | Medium | input-visibility_*.json | Visibility detection logic |
| `test_global_parsing.py` | ⏳ | High | input-globals_*.json | Global variable parsing |
| `test_include_filtering_bugs.py` | ⏳ | Medium | input-filterbug_*.json | Include filtering edge cases |
| `test_include_processing.py` | ⏳ | Medium | input-includes_*.json | Include processing logic |
| `test_multi_pass_anonymous_processing.py` | ⏳ | High | input-multipass_*.json | Multi-pass anonymous processing |
| `test_parser.py` | ⏳ | High | input-parsing_*.json | Core parser functionality |
| `test_parser_comprehensive.py` | ⏳ | High | **SPLIT REQUIRED** | Split into 7 files by C construct |
| `test_parser_filtering.py` | ⏳ | High | input-filter_*.json | Parser filtering logic |
| `test_parser_function_params.py` | ⏳ | Low | input-funcparams_*.json | Function parameter parsing |
| `test_parser_macro_duplicates.py` | ⏳ | Low | input-macrodup_*.json | Macro duplication handling |
| `test_parser_nested_structures.py` | ⏳ | Medium | input-nested_*.json | Nested structure parsing |
| `test_parser_struct_order.py` | ⏳ | Medium | input-structorder_*.json | Struct field order preservation |
| `test_preprocessor_bug.py` | ⏳ | High | input-prepbug_*.json | Preprocessor bug fixes |
| `test_preprocessor_handling.py` | ⏳ | High | input-preproc_*.json | Core preprocessor functionality |
| `test_tokenizer.py` | ⏳ | High | **SPLIT REQUIRED** | Split into 4 files by token category |
| `test_transformation_system.py` | ⏳ | Medium | input-transsys_*.json | Transformation system |
| `test_transformer.py` | ⏳ | High | **SPLIT REQUIRED** | Split into 9 files by transformation type |
| `test_typedef_extraction.py` | ⏳ | Medium | input-typedef_*.json | Typedef extraction logic |
| `test_utils.py` | ⏳ | Low | input-utils_*.json | Utility function testing |
| `test_verifier.py` | ⏳ | Medium | input-verify_*.json | Model verification logic |

### Feature Tests Progress Tracking (12 files)

| Test File | Status | Priority | Input Strategy | Notes |
|-----------|--------|----------|----------------|-------|
| `test_cli_feature.py` | ⏳ | Low | Explicit files | CLI interface testing |
| `test_cli_modes.py` | ⏳ | Low | Explicit files | CLI mode switching |
| `test_component_features.py` | ⏳ | High | Explicit files | Component integration features |
| `test_crypto_filter_pattern.py` | ⏳ | Medium | Explicit files | Crypto filtering patterns |
| `test_crypto_filter_usecase.py` | ⏳ | High | Explicit files | Crypto filtering use cases |
| `test_include_processing_features.py` | ⏳ | High | Explicit files | Include processing features |
| `test_integration.py` | ⏳ | Medium | Explicit files | Feature integration testing |
| `test_invalid_source_paths.py` | ⏳ | High | Explicit files | Error handling for invalid paths |
| `test_multiple_source_folders.py` | ⏳ | High | Explicit files | Multiple source folder handling |
| `test_transformer_features.py` | ⏳ | High | Explicit files | Transformer feature testing |

### Integration Tests Progress Tracking (2 files)

| Test File | Status | Priority | Input Strategy | Notes |
|-----------|--------|----------|----------------|-------|
| `test_comprehensive.py` | ⏳ | High | Explicit files | Comprehensive end-to-end testing |
| `test_new_formatting_comprehensive.py` | ⏳ | Low | Explicit files | New formatting integration |

### Example Tests Progress Tracking (1 file)

| Test File | Status | Priority | Input Strategy | Notes |
|-----------|--------|----------|----------------|-------|
| `test-example.py` | 🚫 | N/A | Explicit files | Preserved as-is with existing structure |

---

## Next Steps

1. **Review and approve** this plan with the development team
2. **Create framework foundation** in `tests/framework/`
3. **Start with pilot migration** of 5-10 representative test files
4. **Execute full migration** following the phase plan

This unified testing approach ensures that c2puml remains flexible to internal changes while providing comprehensive validation of its public API functionality. Feature tests and example tests will always use explicit files to support comprehensive workflow testing, while unit tests can leverage input-##.json files for multiple test scenarios.