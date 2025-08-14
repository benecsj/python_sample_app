#!/usr/bin/env python3
"""
Individual test for basic output generation
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from tests.framework import UnifiedTestCase


class TestBasicOutputGeneration(UnifiedTestCase):
	"""Test class for basic output generation"""

	def test_basic_output_generation(self):
		"""Run the test_101_gen_basic scenario through the CLI interface."""
		result = self.run_test("101_gen_basic")
		self.validate_execution_success(result)
		self.validate_test_output(result)


if __name__ == "__main__":
	unittest.main()
