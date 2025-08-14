#!/usr/bin/env python3
"""
Simple configuration object for python_sample_app.

This module intentionally exposes a single optional attribute with no validation.
"""

import json
from dataclasses import dataclass
from typing import Optional, Any, Dict


@dataclass
class Config:
    """Minimal configuration container with a single optional attribute."""
    output_dir: Optional[str] = None

    @classmethod
    def load(cls, config_file: str) -> "Config":
        """Load configuration from a JSON file without validation."""
        with open(config_file, "r", encoding="utf-8") as f:
            data: Any = json.load(f)
        if isinstance(data, dict):
            # Ignore unknown keys and do not validate types
            output_dir_value = data.get("output_dir")
            return cls(output_dir=output_dir_value)
        # If the JSON is not a dict, return defaults
        return cls()

    def save(self, config_file: str) -> None:
        """Save configuration to a JSON file (only the single attribute)."""
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump({"output_dir": self.output_dir}, f, indent=2, ensure_ascii=False)

    def __repr__(self) -> str:
        return f"Config(output_dir={self.output_dir!r})"
