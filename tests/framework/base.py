#!/usr/bin/env python3
"""
Unified Test Case Base Class (generic)

Provides common setup, teardown, and component initialization for CLI/file tests.
"""

import os
import sys
import unittest
import tempfile
import json
import shutil
from typing import Dict, Any, List

from .executor import TestExecutor, CLIResult
from .data_loader import TestDataLoader
from .validators_processor import ValidatorsProcessor
from .validators import OutputValidator, FileValidator, CLIValidator


class TestResult:
	"""Result object containing test execution results and metadata"""
	def __init__(self, cli_result: CLIResult, test_dir: str, output_dir: str, artifacts: List[str] = None):
		self.cli_result = cli_result
		self.test_dir = test_dir
		self.output_dir = output_dir
		self.artifacts = artifacts or []


class UnifiedTestCase(unittest.TestCase):
	"""Base class for tests using the unified testing framework (generic)."""
	def setUp(self):
		self.executor = TestExecutor()
		self.data_loader = TestDataLoader()
		self.validators_processor = ValidatorsProcessor()
		self.output_validator = OutputValidator()
		self.file_validator = FileValidator()
		self.cli_validator = CLIValidator()
		self._cleanup_existing_test_folders()
		self.temp_dir = tempfile.mkdtemp()
		self.output_dir = os.path.join(self.temp_dir, "output")
		os.makedirs(self.output_dir, exist_ok=True)
		self.test_name = self.__class__.__name__
		self.test_method = self._testMethodName

	def tearDown(self):
		pass

	def run_test(self, test_id: str) -> TestResult:
		# Load test data from YAML
		test_data = self.data_loader.load_test_data(test_id)
		# Create temporary files
		source_dir, config_path = self.data_loader.create_temp_files(test_data, test_id)
		# Calculate paths
		test_folder = os.path.dirname(source_dir)
		test_dir = os.path.dirname(test_folder)
		output_dir = os.path.join(test_dir, "output")
		os.makedirs(output_dir, exist_ok=True)
		config_filename = os.path.basename(config_path)
		# Execute
		cli_result = self.executor.run_full_pipeline(config_filename, test_folder)
		# Collect artifacts (generic: look for output.txt)
		artifacts = []
		candidate = os.path.join(output_dir, "output.txt")
		if os.path.exists(candidate):
			artifacts.append(candidate)
		return TestResult(cli_result, test_dir, output_dir, artifacts)

	def validate_execution_success(self, result: TestResult):
		self.cli_validator.assert_cli_success(result.cli_result)

	def validate_test_output(self, result: TestResult):
		# Load test data to get assertions
		test_id = os.path.basename(result.test_dir).replace('test-', '')
		test_data = self.data_loader.load_test_data(test_id)
		# Expose paths for validators to normalize relative paths
		self.current_validation_base_dir = result.test_dir
		self.current_validation_output_dir = result.output_dir
		# Process assertions
		self.validators_processor.process_assertions(
			test_data.get("assertions", {}), {}, {}, result.cli_result, self
		)

	def _cleanup_existing_test_folders(self):
		"""Clean up any existing test-* folders in test directories"""
		test_categories = ['unit', 'feature', 'integration', 'example']
		for category in test_categories:
			category_path = os.path.join(os.path.dirname(__file__), '..', category)
			if os.path.exists(category_path):
				for item in os.listdir(category_path):
					item_path = os.path.join(category_path, item)
					if os.path.isdir(item_path) and item.startswith('test-'):
						try:
							shutil.rmtree(item_path)
						except Exception as e:
							print(f"Warning: Could not clean up {item_path}: {e}")