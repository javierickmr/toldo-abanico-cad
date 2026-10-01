"""
Test suite for geometric calculations.
"""

import pytest
import math
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from awning.geometry import (
    Point, distance, vector, magnitude, normalize,
    dot_product, cross_product, angle_between,
    midpoint, interpolate, are_collinear, point_on_line_segment
)


def test_point_creation():
    """Test Point class creation."""
    p = Point(1, 2, 3, "A")
    assert p.x == 1
    assert p.y == 2
    assert p.z == 3
    assert p.name == "A"


def test_point_to_tuple():
    """Test Point to tuple conversion."""
    p = Point(1, 2, 3)
    assert p.to_tuple() == (1, 2, 3)


def test_distance_calculation():
    """Test distance between points."""
    p1 = (0, 0, 0)
    p2 = (3, 4, 0)
    assert distance(p1, p2) == 5.0

    p3 = (0, 0, 0)
    p4 = (1, 1, 1)
    assert abs(distance(p3, p4) - math.sqrt(3)) < 1e-10


def test_distance_awning_points():
    """Test known awning dimensions."""
    # Point A at origin
    A = (0, 0, 0)

    # Point B at 2600mm in Y direction (lateral)
    B = (0, 2600, 0)

    # Point C at 2600mm in X direction (longitudinal)
    C = (2600, 0, 0)

    # Validate distances
    assert abs(distance(A, B) - 2600) < 0.01
    assert abs(distance(A, C) - 2600) < 0.01


def test_vector_calculation():
    """Test vector calculation."""
    p1 = (1, 2, 3)
    p2 = (4, 6, 8)
    v = vector(p1, p2)
    assert v == (3, 4, 5)


def test_magnitude():
    """Test vector magnitude."""
    v = (3, 4, 0)
    assert magnitude(v) == 5.0

    v2 = (1, 1, 1)
    assert abs(magnitude(v2) - math.sqrt(3)) < 1e-10


def test_normalize():
    """Test vector normalization."""
    v = (3, 4, 0)
    n = normalize(v)
    assert abs(magnitude(n) - 1.0) < 1e-10
    assert abs(n[0] - 0.6) < 1e-10
    assert abs(n[1] - 0.8) < 1e-10


def test_normalize_zero_vector():
    """Test that normalizing zero vector raises error."""
    v = (0, 0, 0)
    with pytest.raises(ValueError):
        normalize(v)


def test_dot_product():
    """Test dot product."""
    v1 = (1, 0, 0)
    v2 = (0, 1, 0)
    assert dot_product(v1, v2) == 0

    v3 = (1, 2, 3)
    v4 = (4, 5, 6)
    assert dot_product(v3, v4) == 32  # 1*4 + 2*5 + 3*6


def test_cross_product():
    """Test cross product."""
    v1 = (1, 0, 0)
    v2 = (0, 1, 0)
    cp = cross_product(v1, v2)
    assert cp == (0, 0, 1)


def test_angle_between():
    """Test angle calculation."""
    v1 = (1, 0, 0)
    v2 = (0, 1, 0)
    angle = angle_between(v1, v2, degrees=True)
    assert abs(angle - 90) < 1e-10

    v3 = (1, 0, 0)
    v4 = (1, 0, 0)
    angle2 = angle_between(v3, v4, degrees=True)
    assert abs(angle2) < 1e-10


def test_midpoint():
    """Test midpoint calculation."""
    p1 = (0, 0, 0)
    p2 = (10, 10, 10)
    mid = midpoint(p1, p2)
    assert mid == (5, 5, 5)


def test_interpolate():
    """Test linear interpolation."""
    p1 = (0, 0, 0)
    p2 = (10, 10, 10)

    # At t=0, should be p1
    assert interpolate(p1, p2, 0) == p1

    # At t=1, should be p2
    assert interpolate(p1, p2, 1) == p2

    # At t=0.5, should be midpoint
    assert interpolate(p1, p2, 0.5) == (5, 5, 5)


def test_are_collinear():
    """Test collinearity check."""
    p1 = (0, 0, 0)
    p2 = (1, 1, 1)
    p3 = (2, 2, 2)

    assert are_collinear(p1, p2, p3)

    p4 = (1, 0, 0)
    assert not are_collinear(p1, p2, p4)


def test_point_on_line_segment():
    """Test point on line segment check."""
    p1 = (0, 0, 0)
    p2 = (10, 0, 0)

    # Point in the middle
    p_mid = (5, 0, 0)
    assert point_on_line_segment(p_mid, p1, p2)

    # Point on the line but outside segment
    p_outside = (15, 0, 0)
    assert not point_on_line_segment(p_outside, p1, p2)

    # Point not on line
    p_off = (5, 5, 0)
    assert not point_on_line_segment(p_off, p1, p2)
