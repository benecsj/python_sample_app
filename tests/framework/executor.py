"""
TestExecutor - CLI-Only Execution Engine (generic)

Executes the application via its CLI using main.py. Captures stdout/stderr/exit code and timing.
"""

import os
import subprocess
import time
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class CLIResult:
	"""Standard result from CLI execution"""
	exit_code: int
	stdout: str
	stderr: str
	execution_time: float
	command: List[str]
	working_dir: str


class TestExecutor:
	"""Executes the sample app via CLI only."""
	def __init__(self):
		# Absolute path to main.py (project root)
		workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
		main_script_path = os.path.join(workspace_root, "main.py")
		self.main_script_command = ["python3", main_script_path]

	def run_full_pipeline(self, config_path: str, working_dir: str = None) -> CLIResult:
		"""Run the application once (single-step CLI)."""
		if working_dir is None:
			working_dir = os.path.dirname(config_path) if os.path.isfile(config_path) else config_path
		command = self._build_command(["--config", config_path])
		return self._execute_command(command, working_dir)

	def run_with_verbose(self, config_path: str, working_dir: str = None) -> CLIResult:
		if working_dir is None:
			working_dir = os.path.dirname(config_path) if os.path.isfile(config_path) else config_path
		command = self._build_command(["--config", config_path, "--verbose"]) 
		return self._execute_command(command, working_dir)

	def get_test_output_dir(self, test_name: str, scenario: str = None) -> str:
		test_dir = f"tests/{self._get_test_category(test_name)}/{test_name}"
		if scenario:
			return os.path.join(test_dir, f"output-{scenario}")
		else:
			return os.path.join(test_dir, "output")

	def cleanup_output_dir(self, output_dir: str) -> None:
		if os.path.exists(output_dir):
			import shutil
			shutil.rmtree(output_dir)
		os.makedirs(output_dir, exist_ok=True)

	def _build_command(self, args: List[str]) -> List[str]:
		return self.main_script_command + args

	def _execute_command(self, command: List[str], working_dir: str,
						timeout: Optional[int] = None, env: Optional[Dict[str, str]] = None) -> CLIResult:
		start_time = time.time()
		try:
			process_env = os.environ.copy()
			if env:
				process_env.update(env)
			result = subprocess.run(
				command,
				cwd=working_dir,
				env=process_env,
				capture_output=True,
				text=True,
				timeout=timeout
			)
			execution_time = time.time() - start_time
			return CLIResult(
				exit_code=result.returncode,
				stdout=result.stdout,
				stderr=result.stderr,
				execution_time=execution_time,
				command=command,
				working_dir=working_dir
			)
		except subprocess.TimeoutExpired:
			execution_time = time.time() - start_time
			return CLIResult(
				exit_code=-1,
				stdout="",
				stderr=f"Command timed out after {timeout} seconds",
				execution_time=execution_time,
				command=command,
				working_dir=working_dir
			)
		except Exception as e:
			execution_time = time.time() - start_time
			return CLIResult(
				exit_code=-1,
				stdout="",
				stderr=f"Command failed: {e}",
				execution_time=execution_time,
				command=command,
				working_dir=working_dir
			)

	def _get_test_category(self, test_name: str) -> str:
		if test_name.startswith("test_example_"):
			return "example"
		elif "integration" in test_name:
			return "integration"
		elif "feature" in test_name or "comprehensive" in test_name:
			return "feature"
		else:
			return "unit"