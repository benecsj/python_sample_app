#!/usr/bin/env python3
"""
Feature test: CLI basic run
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from tests.framework import UnifiedTestCase


class TestCLIBasicRun(UnifiedTestCase):
	"""Test CLI run and output generation"""

	def test_cli_basic_run(self):
		result = self.run_test("201_cli_modes")
		self.validate_execution_success(result)
		self.validate_test_output(result)


if __name__ == "__main__":
	unittest.main()