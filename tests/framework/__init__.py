#!/usr/bin/env python3
"""
Unified Testing Framework (generic)

Provides CLI execution, YAML-based test data loading, and generic validators.
"""

from .base import UnifiedTestCase, TestResult
from .data_loader import TestDataLoader
from .executor import TestExecutor, CLIResult
from .validators_processor import ValidatorsProcessor
from .validators import (
	OutputValidator,
	FileValidator,
	CLIValidator,
	TestError
)

__all__ = [
	'UnifiedTestCase',
	'TestResult',
	'TestDataLoader',
	'TestExecutor',
	'CLIResult',
	'ValidatorsProcessor',
	'OutputValidator',
	'FileValidator',
	'CLIValidator',
	'TestError'
]