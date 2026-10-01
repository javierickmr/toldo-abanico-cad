"""
Test suite for parameter management.
"""

import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from awning.parameters import Parameters, load_parameters


def test_parameters_load():
    """Test that parameters load without error."""
    params = Parameters()
    assert params is not None


def test_dimensions_loaded():
    """Test that dimensions are loaded."""
    params = Parameters()
    assert params.dimensions is not None
    assert 'units' in params.dimensions
    assert params.dimensions['units'] == 'mm'


def test_known_dimensions():
    """Test that known dimensions are correct."""
    params = Parameters()

    # Test vehicle dimensions
    vehicle_length = params.get('vehicle.length')
    assert vehicle_length == 5365

    # Test awning dimensions
    span_AB = params.get('awning.span_AB')
    span_AC = params.get('awning.span_AC')

    assert span_AB == 2600
    assert span_AC == 2600


def test_get_with_default():
    """Test get method with default values."""
    params = Parameters()

    # Existing value
    assert params.get('awning.span_AB', 0) == 2600

    # Non-existing value
    assert params.get('nonexistent.parameter', 999) == 999


def test_materials_loaded():
    """Test that materials are loaded."""
    params = Parameters()
    assert params.materials is not None


def test_project_loaded():
    """Test that project config is loaded."""
    params = Parameters()
    assert params.project is not None
    assert 'project' in params.project


def test_validate_required_success():
    """Test validate_required with existing parameter."""
    params = Parameters()
    value = params.validate_required('awning.span_AB')
    assert value == 2600


def test_validate_required_failure():
    """Test validate_required with missing parameter."""
    params = Parameters()
    with pytest.raises(ValueError):
        params.validate_required('nonexistent.parameter')


def test_validate_required_null():
    """Test validate_required with null parameter."""
    params = Parameters()
    # tubes.main_frame.outer_diameter should be null/None
    with pytest.raises(ValueError):
        params.validate_required('tubes.main_frame.outer_diameter')


def test_load_parameters_function():
    """Test convenience function."""
    params = load_parameters()
    assert params is not None
    assert isinstance(params, Parameters)
