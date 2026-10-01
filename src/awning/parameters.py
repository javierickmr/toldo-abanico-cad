"""
Parameter Management Module
============================

Loads and manages configuration parameters from YAML files.
Provides centralized access to all dimensional and material parameters.

All dimensions are in millimeters unless otherwise specified.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class Parameters:
    """
    Central parameter management class.

    Loads configuration from YAML files and provides access to:
    - Dimensional parameters
    - Material properties
    - Project settings
    """

    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize parameters from configuration directory.

        Args:
            config_dir: Path to configuration directory. If None, uses default.
        """
        if config_dir is None:
            # Default to config directory relative to this file
            self.config_dir = Path(__file__).parent.parent.parent / "config"
        else:
            self.config_dir = Path(config_dir)

        self.dimensions: Dict[str, Any] = {}
        self.materials: Dict[str, Any] = {}
        self.project: Dict[str, Any] = {}

        self._load_all()

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load a YAML configuration file."""
        filepath = self.config_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Configuration file not found: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _load_all(self):
        """Load all configuration files."""
        self.dimensions = self._load_yaml("dimensions.yaml")
        self.materials = self._load_yaml("materials.yaml")
        self.project = self._load_yaml("project.yaml")

    def get(self, path: str, default: Any = None) -> Any:
        """
        Get a parameter value using dot notation.

        Args:
            path: Parameter path (e.g., "awning.span_AB")
            default: Default value if parameter not found

        Returns:
            Parameter value or default

        Example:
            >>> params = Parameters()
            >>> params.get("awning.span_AB")
            2600
        """
        parts = path.split('.')

        # Determine which config to search
        if parts[0] in self.dimensions:
            data = self.dimensions
        elif parts[0] in self.materials:
            data = self.materials
        elif parts[0] in self.project:
            data = self.project
        else:
            return default

        # Navigate the path
        for part in parts:
            if isinstance(data, dict) and part in data:
                data = data[part]
            else:
                return default

        return data

    def get_dimension(self, key: str, default: Any = None) -> Any:
        """Get a dimensional parameter."""
        return self.get(f"dimensions.{key}", default) or self.get(key, default)

    def get_material(self, key: str, default: Any = None) -> Any:
        """Get a material parameter."""
        return self.get(f"materials.{key}", default) or self.get(key, default)

    def validate_required(self, path: str) -> Any:
        """
        Get a required parameter, raise error if not found or None.

        Args:
            path: Parameter path

        Returns:
            Parameter value

        Raises:
            ValueError: If parameter is not found or is None/null
        """
        value = self.get(path)
        if value is None:
            raise ValueError(
                f"Required parameter '{path}' is not defined. "
                f"Please set this value in configuration files."
            )
        return value

    def __repr__(self) -> str:
        return f"Parameters(config_dir='{self.config_dir}')"


def load_parameters(config_dir: Optional[Path] = None) -> Parameters:
    """
    Convenience function to load parameters.

    Args:
        config_dir: Path to configuration directory

    Returns:
        Parameters instance
    """
    return Parameters(config_dir=config_dir)
