"""
Awning CAD Package
==================

Parametric CAD design package for folding awning structures.

This package provides:
- Parameter loading from YAML configuration
- Geometric calculations and validation
- CAD component generation using CadQuery
- Export to STEP, STL, DXF formats
- Assembly management
"""

__version__ = "0.1.0"
__author__ = "Awning CAD Project"

from . import parameters
from . import geometry
from . import validation

__all__ = [
    'parameters',
    'geometry',
    'validation',
]
