#!/usr/bin/env python3
"""
Minimal CLI for python_sample_app

Behavior:
- Reads a JSON configuration from a file path or a folder (merging *.json files in folder)
- Expects a key 'test' (string) in the configuration
- Writes output.txt into the configured output_dir (default: ./output)
  containing the value of the 'test' key followed by a newline
- Returns exit code 0 on success, non-zero on error

This CLI accepts an optional trailing command argument for compatibility,
which is ignored (kept only to avoid breaking existing scripts).
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict


def setup_logging(verbose: bool = False) -> None:
	level = logging.DEBUG if verbose else logging.INFO
	logging.basicConfig(
		level=level,
		format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
		handlers=[logging.StreamHandler(sys.stdout)],
	)


def load_config_from_path(config_path: str) -> Dict[str, Any]:
	path = Path(config_path)
	if path.is_file():
		with open(path, "r", encoding="utf-8") as f:
			return json.load(f)
	elif path.is_dir():
		# Merge all .json files in the folder (later files override earlier ones)
		config: Dict[str, Any] = {}
		for file in sorted(path.glob("*.json")):
			with open(file, "r", encoding="utf-8") as f:
				data = json.load(f)
				if isinstance(data, dict):
					config.update(data)
		return config
	else:
		raise FileNotFoundError(f"Config path not found: {config_path}")


def main() -> int:
	parser = argparse.ArgumentParser(
		description="python_sample_app - minimal CLI",
		formatter_class=argparse.RawDescriptionHelpFormatter,
	)
	parser.add_argument(
		"--config",
		"-c",
		type=str,
		default=None,
		help="Path to config.json or a folder containing JSON files (default: current directory)",
	)
	parser.add_argument(
		"command",
		nargs="?",
		help="Optional command argument (ignored; kept for compatibility)",
	)
	parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
	args = parser.parse_args()

	setup_logging(args.verbose)

	# Determine config path
	config_path = args.config or os.getcwd()
	logging.info("Using config: %s", config_path)

	# Load config
	try:
		config = load_config_from_path(config_path)
	except Exception as e:
		logging.error("Failed to load configuration: %s", e)
		return 1

	# Resolve output directory
	output_dir = config.get("output_dir") or os.path.join(os.getcwd(), "output")
	output_dir = os.path.abspath(output_dir)
	os.makedirs(output_dir, exist_ok=True)
	logging.info("Output directory: %s", output_dir)

	# Get the 'test' value
	test_value = config.get("test", "Hello World")
	if not isinstance(test_value, str):
		logging.error("Configuration 'test' must be a string. Got: %r", type(test_value))
		return 1

	# Write output.txt with the test value
	output_file = os.path.join(output_dir, "output.txt")
	try:
		with open(output_file, "w", encoding="utf-8") as f:
			f.write(test_value + "\n")
		logging.info("Wrote output to: %s", output_file)
	except Exception as e:
		logging.error("Failed to write output: %s", e)
		return 1

	return 0


if __name__ == "__main__":
	sys.exit(main())
