"""
Test suite for CAD exports.
"""

import pytest
from pathlib import Path
import sys
import cadquery as cq

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from awning.exporters import export_step, export_stl, export_dxf, ensure_directory


def test_ensure_directory(tmp_path):
    """Test directory creation."""
    test_file = tmp_path / "subdir" / "test.txt"
    result = ensure_directory(test_file)
    assert result.parent.exists()


def test_export_step(tmp_path):
    """Test STEP export."""
    # Create simple assembly
    box = cq.Workplane("XY").box(10, 10, 10)
    assembly = cq.Assembly()
    assembly.add(box, name="box")

    # Export
    output_path = tmp_path / "test.step"
    result = export_step(assembly, output_path)

    # Validate
    assert result.exists()
    assert result.stat().st_size > 0


def test_export_stl(tmp_path):
    """Test STL export."""
    # Create simple shape
    box = cq.Workplane("XY").box(10, 10, 10)

    # Export
    output_path = tmp_path / "test.stl"
    result = export_stl(box, output_path)

    # Validate
    assert result.exists()
    assert result.stat().st_size > 0


def test_export_dxf(tmp_path):
    """Test DXF export."""
    # Create simple shape
    box = cq.Workplane("XY").box(10, 10, 10)

    # Export
    output_path = tmp_path / "test.dxf"
    result = export_dxf(box, output_path)

    # Validate
    assert result.exists()
    assert result.stat().st_size > 0


def test_simple_box_volume():
    """Test that a simple box has correct volume."""
    # Create a 100 x 50 x 20 mm box
    box = cq.Workplane("XY").box(100, 50, 20)

    # Get volume
    volume = box.val().Volume()

    # Expected volume
    expected = 100 * 50 * 20  # 100000 mm³

    # Validate with tolerance
    assert abs(volume - expected) < 1.0  # 1 mm³ tolerance
