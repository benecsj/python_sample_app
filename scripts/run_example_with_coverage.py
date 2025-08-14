#!/usr/bin/env python3
"""
Run example with coverage tracking for python_sample_app.
"""

import os
import subprocess
import sys
from pathlib import Path


def print_header(text: str) -> None:
	print(f"\n{'=' * 60}")
	print(f"  {text}")
	print(f"{'=' * 60}\n")


def print_info(text: str) -> None:
	print(f"ℹ️  {text}")


def print_success(text: str) -> None:
	print(f"✅ {text}")


def print_error(text: str) -> None:
	print(f"❌ {text}")


def run_example():
	print_header("Running Example with Coverage")
	workspace_dir = Path(__file__).parent.parent
	os.chdir(workspace_dir)

	cmd = [
		"coverage", "run", "-a", "-m", "python_sample_app.main",
		"--config", "tests/example/config.json",
	]
	print_info(f"Running: {' '.join(cmd)}")
	try:
		result = subprocess.run(cmd, capture_output=True, text=True)
		if result.returncode == 0:
			print_success("Command completed successfully")
			if result.stdout:
				print(result.stdout)
		else:
			print_error(f"Command failed with return code {result.returncode}")
			if result.stderr:
				print(result.stderr)
			return False
	except Exception as e:
		print_error(f"Error running command: {e}")
		return False

	# Check expected output
	expected = Path("artifacts/output_example/output.txt")
	print_info("\nChecking generated output...")
	if expected.exists():
		print_success(f"Generated: {expected}")
		return True
	else:
		print_error(f"Missing: {expected}")
		return False


def main():
	print_header("Example Coverage Runner")
	try:
		subprocess.run(["coverage", "--version"], check=True, capture_output=True)
	except (subprocess.CalledProcessError, FileNotFoundError):
		print_error("Coverage not installed. Install with: pip install coverage")
		return 1

	success = run_example()
	if success:
		print_header("Example Run Complete!")
		print_success("Example executed with coverage")
	else:
		return 1
	return 0


if __name__ == "__main__":
	sys.exit(main())
