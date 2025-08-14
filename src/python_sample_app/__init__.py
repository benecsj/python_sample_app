"""
python_sample_app - Sample Python application scaffold

A minimal Python CLI that reads a JSON config and writes output.txt.
"""

__version__ = "0.1.0"
__author__ = "python_sample_app Team"

from .main import main  # CLI entry point

__all__ = [
	"main",
	"__version__",
	"__author__",
]