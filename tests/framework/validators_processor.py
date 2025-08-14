#!/usr/bin/env python3
"""
Validators Processor for the unified testing framework (generic)

Coordinates CLI and file validations based on YAML assertions.
"""

from typing import Dict, Any
from .executor import CLIResult
from .validators import CLIValidator, OutputValidator, FileValidator


class ValidatorsProcessor:
	"""Process assertions from YAML using generic validators"""
	def __init__(self):
		self.cli_validator = CLIValidator()
		self.output_validator = OutputValidator()
		self.file_validator = FileValidator()

	def process_assertions(self, assertions: Dict[str, Any], _model_data: Dict,
						_puml_files: Dict[str, str], cli_result: CLIResult, _test_case) -> None:
		# Execution assertions
		if "execution" in assertions:
			exec_a = assertions["execution"]
			if "exit_code" in exec_a:
				expected = exec_a["exit_code"]
				if expected == 0:
					self.cli_validator.assert_cli_success(cli_result)
				else:
					self.cli_validator.assert_cli_exit_code(cli_result, expected)
			if "stdout_contains" in exec_a:
				self.cli_validator.assert_cli_stdout_contains(cli_result, exec_a["stdout_contains"])
			if "stderr_contains" in exec_a:
				self.cli_validator.assert_cli_stderr_contains(cli_result, exec_a["stderr_contains"])
			if "max_execution_time" in exec_a:
				self.cli_validator.assert_cli_execution_time_under(cli_result, exec_a["max_execution_time"])
			if exec_a.get("success_expected") is False:
				self.cli_validator.assert_cli_failure(cli_result, exec_a.get("expected_error"))

		# File assertions
		if "files" in assertions:
			files_a = assertions["files"]
			if "output_dir_exists" in files_a:
				self.output_validator.assert_output_dir_exists(files_a["output_dir_exists"])
			for path in files_a.get("files_exist", []):
				self.output_validator.assert_file_exists(path)
			for path in files_a.get("files_not_exist", []):
				self.output_validator.assert_file_not_exists(path)
			for path in files_a.get("utf8_files", []):
				self.file_validator.assert_file_valid_utf8(path)
			# File content checks
			for file_path, content_assertions in files_a.get("file_content", {}).items():
				for expected in content_assertions.get("contains", []):
					self.output_validator.assert_file_contains(file_path, expected)
				for forbidden in content_assertions.get("not_contains", []):
					self.output_validator.assert_file_not_contains(file_path, forbidden)
				if "contains_lines" in content_assertions:
					self.output_validator.assert_file_contains_lines(file_path, content_assertions["contains_lines"])
				if "line_count" in content_assertions:
					self.output_validator.assert_file_line_count(file_path, content_assertions["line_count"])
				if content_assertions.get("empty"):
					self.output_validator.assert_file_empty(file_path)
				if content_assertions.get("not_empty"):
					self.output_validator.assert_file_not_empty(file_path)