#!/usr/bin/env python3
"""
Debug entry point for python_sample_app

This script provides a convenient way to debug the app with predefined configurations.

Configuration is done by modifying the constants at the top of this file.
All command line arguments are forwarded directly to main.py.

Usage:
    python debug.py                     # Uses internal DEBUG CONFIGURATION
    python debug.py --config ./my_config.json --verbose
"""

import logging
import subprocess
import sys
from pathlib import Path

# =============================================================================
# DEBUG CONFIGURATION - Modify these constants as needed
# =============================================================================

# Default command line options
# CONFIG_PATH: str = "./tests/example/config.json"
# VERBOSE: bool = True

# =============================================================================
# END CONFIGURATION
# =============================================================================


def setup_logging():
	"""Setup logging"""
	logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
		handlers=[logging.StreamHandler(sys.stdout)],
	)


def main():
	"""Main debug entry point"""
	setup_logging()

	# Get project root (go up one level from scripts/ directory)
	project_root = Path(__file__).parent.parent
	app_script = project_root / "main.py"

	if not app_script.exists():
		logging.error("main.py not found at: %s", app_script)
		return 1

	# Build command for main.py
	cmd = [sys.executable, str(app_script)]

	# Check if constants are defined
	has_config = 'CONFIG_PATH' in globals()
	has_verbose = 'VERBOSE' in globals()

	# Forward remaining command line arguments
	args = sys.argv[1:]

	if has_config:
		cmd.extend(["--config", CONFIG_PATH])
		logging.info("Overriding config with: %s", CONFIG_PATH)
		# Remove existing config args from args
		args = [arg for i, arg in enumerate(args) if not (arg.startswith('--config') or arg.startswith('-c')) and (i == 0 or not args[i-1].startswith('--config'))]

	if has_verbose and VERBOSE:
		cmd.append("--verbose")
		logging.info("Overriding verbose with: %s", VERBOSE)
		args = [arg for arg in args if not (arg.startswith('--verbose') or arg.startswith('-v'))]

	cmd.extend(args)
	logging.info("Running command: %s", " ".join(cmd))

	try:
		# Run app main.py
		result = subprocess.run(cmd, cwd=project_root)
		logging.info("Debug run completed with result: %s", result.returncode)
		return result.returncode
	except Exception as e:
		logging.error("Debug run failed: %s", e)
		import traceback
		traceback.print_exc()
		return 1


if __name__ == "__main__":
	sys.exit(main())
