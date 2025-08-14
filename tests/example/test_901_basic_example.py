#!/usr/bin/env python3
"""
Example test using the unified framework and external example files
"""

import os
import sys
import json
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from tests.framework import UnifiedTestCase  # noqa: E402


class TestBasicExample(UnifiedTestCase):
	"""Validate example project end-to-end via CLI using YAML assertions"""

	def test_basic_example(self):
		"""Run the app with external config and validate outputs"""
		test_data = self.data_loader.load_test_data("901_basic_example")
		workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
		# Run using top-level config in tests/example/config.json
		result = self.executor.run_full_pipeline("tests/example/config.json", workspace_root)
		self.cli_validator.assert_cli_success(result)
		# Process assertions (checks artifacts/output_example/output.txt exists)
		self.validators_processor.process_assertions(test_data["assertions"], {}, {}, result, self)


if __name__ == "__main__":
	unittest.main()