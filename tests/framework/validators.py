#!/usr/bin/env python3
"""
Validators for the unified testing framework (generic)

This module provides validator classes for validating CLI results and files.
"""

import os
import re
from typing import Dict, List
from .executor import CLIResult


class TestError(Exception):
	"""Enhanced exception class for test framework errors with context"""
	def __init__(self, message: str, test_id: str = None, context: Dict = None):
		self.test_id = test_id
		self.context = context or {}
		super().__init__(f"Test '{test_id}' failed: {message}" if test_id else message)


class OutputValidator:
	"""Validates general output files, directories, and content"""
	def _normalize_path(self, path: str) -> str:
		"""Normalize a possibly relative path to an absolute path based on current test context."""
		if os.path.isabs(path):
			return path
		try:
			import inspect
			for frame_info in inspect.stack():
				self_obj = frame_info.frame.f_locals.get('self')
				if hasattr(self_obj, 'current_validation_base_dir'):
					base_dir = getattr(self_obj, 'current_validation_base_dir')
					return os.path.normpath(os.path.join(base_dir, path))
		except Exception:
			pass
		return os.path.normpath(path)

	def assert_output_dir_exists(self, output_path: str) -> None:
		resolved = self._normalize_path(output_path)
		if not os.path.exists(resolved):
			raise AssertionError(f"Output directory does not exist: {resolved}")
		if not os.path.isdir(resolved):
			raise AssertionError(f"Output path is not a directory: {resolved}")

	def assert_file_exists(self, file_path: str) -> None:
		resolved = self._normalize_path(file_path)
		if not os.path.exists(resolved):
			raise AssertionError(f"File does not exist: {resolved}")

	def assert_file_not_exists(self, file_path: str) -> None:
		resolved = self._normalize_path(file_path)
		if os.path.exists(resolved):
			raise AssertionError(f"File exists but should not: {resolved}")

	def assert_directory_empty(self, dir_path: str) -> None:
		resolved = self._normalize_path(dir_path)
		if not os.path.exists(resolved):
			raise AssertionError(f"Directory does not exist: {resolved}")
		files = os.listdir(resolved)
		if files:
			raise AssertionError(f"Directory is not empty: {resolved} contains {files}")

	def assert_directory_not_empty(self, dir_path: str) -> None:
		resolved = self._normalize_path(dir_path)
		if not os.path.exists(resolved):
			raise AssertionError(f"Directory does not exist: {resolved}")
		files = os.listdir(resolved)
		if not files:
			raise AssertionError(f"Directory is empty: {resolved}")

	def assert_file_contains(self, file_path: str, expected_text: str) -> None:
		resolved = self._normalize_path(file_path)
		if not os.path.exists(resolved):
			raise AssertionError(f"File does not exist: {resolved}")
		with open(resolved, 'r', encoding='utf-8') as f:
			content = f.read()
		if expected_text not in content:
			raise AssertionError(f"File '{resolved}' missing expected text: '{expected_text}'")

	def assert_file_not_contains(self, file_path: str, forbidden_text: str) -> None:
		resolved = self._normalize_path(file_path)
		if not os.path.exists(resolved):
			raise AssertionError(f"File does not exist: {resolved}")
		with open(resolved, 'r', encoding='utf-8') as f:
			content = f.read()
		if forbidden_text in content:
			raise AssertionError(f"File '{resolved}' contains forbidden text: '{forbidden_text}'")

	def assert_file_contains_lines(self, file_path: str, expected_lines: List[str]) -> None:
		resolved = self._normalize_path(file_path)
		if not os.path.exists(resolved):
			raise AssertionError(f"File does not exist: {resolved}")
		with open(resolved, 'r', encoding='utf-8') as f:
			content = f.read()
		for line in expected_lines:
			if line not in content:
				raise AssertionError(f"File '{resolved}' missing expected line: '{line}'")

	def assert_file_line_count(self, file_path: str, expected_count: int) -> None:
		resolved = self._normalize_path(file_path)
		if not os.path.exists(resolved):
			raise AssertionError(f"File does not exist: {resolved}")
		with open(resolved, 'r', encoding='utf-8') as f:
			lines = f.readlines()
		actual_count = len(lines)
		if actual_count != expected_count:
			raise AssertionError(f"File '{resolved}' expected {expected_count} lines, got {actual_count}")

	def assert_file_empty(self, file_path: str) -> None:
		resolved = self._normalize_path(file_path)
		if not os.path.exists(resolved):
			raise AssertionError(f"File does not exist: {resolved}")
		if os.path.getsize(resolved) != 0:
			raise AssertionError(f"File is not empty: {resolved}")

	def assert_file_not_empty(self, file_path: str) -> None:
		resolved = self._normalize_path(file_path)
		if not os.path.exists(resolved):
			raise AssertionError(f"File does not exist: {resolved}")
		if os.path.getsize(resolved) == 0:
			raise AssertionError(f"File is empty: {resolved}")

	def assert_log_contains(self, log_content: str, expected_message: str) -> None:
		if expected_message not in log_content:
			raise AssertionError(f"Log missing expected message: '{expected_message}'")

	def assert_log_no_errors(self, log_content: str) -> None:
		error_patterns = ["ERROR", "FATAL", "Exception", "Traceback"]
		for pattern in error_patterns:
			if pattern in log_content:
				raise AssertionError(f"Log contains error pattern: '{pattern}'")

	def assert_log_no_warnings(self, log_content: str) -> None:
		warning_patterns = [r'WARNING', r'Warning', r'warning']
		for pattern in warning_patterns:
			if re.search(pattern, log_content):
				raise AssertionError(f"Log contains warnings: {log_content}")


class FileValidator:
	"""Advanced file validation and manipulation utilities"""
	def assert_files_equal(self, file1_path: str, file2_path: str) -> None:
		if not os.path.exists(file1_path):
			raise AssertionError(f"File 1 does not exist: {file1_path}")
		if not os.path.exists(file2_path):
			raise AssertionError(f"File 2 does not exist: {file2_path}")
		with open(file1_path, 'r', encoding='utf-8') as f1, open(file2_path, 'r', encoding='utf-8') as f2:
			content1 = f1.read()
			content2 = f2.read()
		if content1 != content2:
			raise AssertionError(f"Files '{file1_path}' and '{file2_path}' have different content")

	def assert_file_valid_utf8(self, file_path: str) -> None:
		if not os.path.exists(file_path):
			raise AssertionError(f"File does not exist: {file_path}")
		try:
			with open(file_path, 'r', encoding='utf-8') as f:
				f.read()
		except UnicodeDecodeError as e:
			raise AssertionError(f"File '{file_path}' is not valid UTF-8: {e}")

	def assert_execution_time_under(self, actual_time: float, max_time: float) -> None:
		if actual_time > max_time:
			raise AssertionError(f"Execution time {actual_time:.2f}s exceeds maximum {max_time:.2f}s")


class CLIValidator:
	"""Validates CLI execution results and behavior"""
	def assert_cli_success(self, result: CLIResult, message: str = None) -> None:
		if result.exit_code != 0:
			error_msg = message or f"CLI execution failed with exit code {result.exit_code}"
			if result.stderr:
				error_msg += f"\nStderr: {result.stderr}"
			raise TestError(error_msg, context={"exit_code": result.exit_code, "stderr": result.stderr})

	def assert_cli_failure(self, result: CLIResult, expected_error: str = None, message: str = None) -> None:
		if result.exit_code == 0:
			error_msg = message or "CLI execution succeeded when failure was expected"
			raise TestError(error_msg, context={"exit_code": result.exit_code, "stdout": result.stdout})
		if expected_error and expected_error not in result.stderr:
			error_msg = f"Expected error '{expected_error}' not found in stderr: {result.stderr}"
			raise TestError(error_msg, context={"exit_code": result.exit_code, "stderr": result.stderr})

	def assert_cli_exit_code(self, result: CLIResult, expected_exit_code: int) -> None:
		if result.exit_code != expected_exit_code:
			raise TestError(f"Expected exit code {expected_exit_code}, got {result.exit_code}",
					  context={"exit_code": result.exit_code, "expected_exit_code": expected_exit_code})

	def assert_cli_stdout_contains(self, result: CLIResult, expected_text: str) -> None:
		if expected_text not in result.stdout:
			raise TestError(f"Expected text '{expected_text}' not found in stdout: {result.stdout}",
					  context={"stdout": result.stdout, "expected_text": expected_text})

	def assert_cli_stderr_contains(self, result: CLIResult, expected_text: str) -> None:
		if expected_text not in result.stderr:
			raise TestError(f"Expected text '{expected_text}' not found in stderr: {result.stderr}",
					  context={"stderr": result.stderr, "expected_text": expected_text})

	def assert_cli_execution_time_under(self, result: CLIResult, max_time: float) -> None:
		if result.execution_time > max_time:
			raise TestError(f"Execution time {result.execution_time:.2f}s exceeds maximum {max_time:.2f}s",
					  context={"execution_time": result.execution_time, "max_time": max_time})