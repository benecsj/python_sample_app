#!/usr/bin/env python3
"""
Test Data Loader for the unified testing framework (generic)

This module provides the TestDataLoader class that handles loading
test data from YAML files and creating temporary files for testing.
"""

import os
import yaml
import tempfile
import json
from typing import Dict, Tuple, Optional


class TestDataLoader:
	"""
	Loads test data from YAML files and creates temporary files for testing
	"""
	def __init__(self):
		pass

	def load_test_data(self, test_id: str) -> Dict:
		# Try to find the YAML file in different test categories
		test_categories = ["unit", "feature", "integration", "example"]
		for category in test_categories:
			yaml_file = f"tests/{category}/test_{test_id}.yml"
			if os.path.exists(yaml_file):
				with open(yaml_file, 'r') as f:
					documents = list(yaml.safe_load_all(f))
				test_data = self._parse_yaml_documents(documents)
				self._validate_test_data(test_data)
				return test_data
		# Legacy numeric format
		try:
			test_num = int(test_id)
			category = self._get_test_category(test_id)
			yaml_file = f"tests/{category}/test-{test_id:03d}.yml"
			if os.path.exists(yaml_file):
				with open(yaml_file, 'r') as f:
					documents = list(yaml.safe_load_all(f))
				test_data = self._parse_yaml_documents(documents)
				self._validate_test_data(test_data)
				return test_data
		except ValueError:
			pass
		raise FileNotFoundError(f"Test data file not found for test ID: {test_id}")

	def _parse_yaml_documents(self, documents: list) -> Dict:
		test_data = {}
		for doc in documents:
			if not doc:
				continue
			if "test" in doc:
				test_data["test"] = doc["test"]
			if "source_files" in doc:
				test_data["source_files"] = doc["source_files"]
			if "config.json" in doc:
				if "source_files" not in test_data:
					test_data["source_files"] = {}
				test_data["source_files"]["config.json"] = doc["config.json"]
			if "assertions" in doc:
				test_data["assertions"] = doc["assertions"]
		return test_data

	def create_temp_files(self, test_data: Dict, test_id: str) -> Tuple[str, str]:
		# Find the test category and create test-specific folder
		test_categories = ["unit", "feature", "integration", "example"]
		test_dir = None
		for category in test_categories:
			category_dir = f"tests/{category}"
			if os.path.exists(category_dir):
				test_dir = os.path.join(category_dir, f"test-{test_id}")
				break
		if not test_dir:
			raise ValueError(f"Could not find test directory for test ID: {test_id}")
		os.makedirs(test_dir, exist_ok=True)
		input_dir = os.path.join(test_dir, "input")
		output_dir = os.path.join(test_dir, "output")
		os.makedirs(input_dir, exist_ok=True)
		os.makedirs(output_dir, exist_ok=True)
		source_dir = self._create_source_files(test_data, input_dir)
		config_path = self._create_config_file(test_data, input_dir)
		return source_dir, config_path

	def _get_test_category(self, test_id: str) -> str:
		test_num = int(test_id)
		if test_num <= 1000:
			return "unit"
		elif test_num <= 2000:
			return "feature"
		elif test_num <= 3000:
			return "integration"
		else:
			return "example"

	def _validate_test_data(self, test_data: Dict) -> None:
		# Example tests may provide only assertions
		has_source_files = "source_files" in test_data
		has_assertions_only = (not has_source_files) and ("assertions" in test_data)
		if not has_source_files and not has_assertions_only:
			raise ValueError("Test data must include 'source_files' or at least 'assertions' for example tests")
		if has_source_files:
			if not isinstance(test_data["source_files"], dict):
				raise ValueError("'source_files' must be a dictionary")
			if not test_data["source_files"]:
				raise ValueError("'source_files' cannot be empty")
			if "config.json" not in test_data["source_files"]:
				raise ValueError("Missing config.json in source_files")
			# Validate that config.json contains valid JSON
			try:
				json.loads(test_data["source_files"]["config.json"])
			except json.JSONDecodeError as e:
				raise ValueError(f"Invalid JSON in config.json: {e}")
		# Validate assertions section if present
		if "assertions" in test_data and not isinstance(test_data["assertions"], dict):
			raise ValueError("'assertions' must be a dictionary")

	def _create_source_files(self, test_data: Dict, temp_dir: str) -> str:
		source_files = test_data["source_files"]
		source_dir = os.path.join(temp_dir, "src")
		os.makedirs(source_dir, exist_ok=True)
		for filename, content in source_files.items():
			if filename == "config.json":
				continue
			file_path = os.path.join(source_dir, filename)
			os.makedirs(os.path.dirname(file_path), exist_ok=True)
			with open(file_path, 'w') as f:
				f.write(content)
		return source_dir

	def _create_config_file(self, test_data: Dict, temp_dir: str) -> str:
		source_files = test_data["source_files"]
		if "config.json" not in source_files:
			raise ValueError("Missing config.json in source_files")
		config_content = source_files["config.json"]
		# Parse JSON to validate it
		try:
			config = json.loads(config_content)
		except json.JSONDecodeError as e:
			raise ValueError(f"Invalid JSON in config.json: {e}")
		# Ensure output_dir points to ../output (relative to input/)
		config["output_dir"] = "../output"
		# Create config file
		config_path = os.path.join(temp_dir, "config.json")
		with open(config_path, 'w') as f:
			json.dump(config, f, indent=2)
		return config_path