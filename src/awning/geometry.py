"""
Geometric Calculations Module
==============================

Provides fundamental geometric calculations for the awning structure.

All coordinates are in millimeters.
Coordinate system (right-handed):
- X: longitudinal (along vehicle length)
- Y: lateral (across vehicle width)
- Z: vertical (height)

Origin: Point A (primary structural anchor)
"""

import math
from typing import Tuple, List
from dataclasses import dataclass


# Type aliases for clarity
Point3D = Tuple[float, float, float]
Vector3D = Tuple[float, float, float]


@dataclass
class Point:
    """Represents a 3D point in space."""
    x: float
    y: float
    z: float
    name: str = ""

    def to_tuple(self) -> Point3D:
        """Convert to tuple representation."""
        return (self.x, self.y, self.z)

    def __repr__(self) -> str:
        if self.name:
            return f"Point({self.name}: x={self.x:.2f}, y={self.y:.2f}, z={self.z:.2f})"
        return f"Point(x={self.x:.2f}, y={self.y:.2f}, z={self.z:.2f})"


def distance(p1: Point3D, p2: Point3D) -> float:
    """
    Calculate Euclidean distance between two points.

    Args:
        p1: First point (x, y, z)
        p2: Second point (x, y, z)

    Returns:
        Distance in millimeters
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)


def vector(p1: Point3D, p2: Point3D) -> Vector3D:
    """
    Calculate vector from p1 to p2.

    Args:
        p1: Start point
        p2: End point

    Returns:
        Vector (dx, dy, dz)
    """
    return (
        p2[0] - p1[0],
        p2[1] - p1[1],
        p2[2] - p1[2]
    )


def magnitude(v: Vector3D) -> float:
    """
    Calculate magnitude (length) of a vector.

    Args:
        v: Vector (x, y, z)

    Returns:
        Magnitude
    """
    return math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])


def normalize(v: Vector3D) -> Vector3D:
    """
    Normalize a vector to unit length.

    Args:
        v: Vector to normalize

    Returns:
        Unit vector in same direction
    """
    mag = magnitude(v)
    if mag == 0:
        raise ValueError("Cannot normalize zero vector")
    return (v[0]/mag, v[1]/mag, v[2]/mag)


def dot_product(v1: Vector3D, v2: Vector3D) -> float:
    """
    Calculate dot product of two vectors.

    Args:
        v1: First vector
        v2: Second vector

    Returns:
        Dot product
    """
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]


def cross_product(v1: Vector3D, v2: Vector3D) -> Vector3D:
    """
    Calculate cross product of two vectors.

    Args:
        v1: First vector
        v2: Second vector

    Returns:
        Cross product vector
    """
    return (
        v1[1]*v2[2] - v1[2]*v2[1],
        v1[2]*v2[0] - v1[0]*v2[2],
        v1[0]*v2[1] - v1[1]*v2[0]
    )


def angle_between(v1: Vector3D, v2: Vector3D, degrees: bool = True) -> float:
    """
    Calculate angle between two vectors.

    Args:
        v1: First vector
        v2: Second vector
        degrees: If True, return angle in degrees; else radians

    Returns:
        Angle between vectors
    """
    # Normalize vectors
    n1 = normalize(v1)
    n2 = normalize(v2)

    # Calculate angle using dot product
    dot = dot_product(n1, n2)
    # Clamp to [-1, 1] to handle numerical errors
    dot = max(-1.0, min(1.0, dot))

    angle_rad = math.acos(dot)

    if degrees:
        return math.degrees(angle_rad)
    return angle_rad


def midpoint(p1: Point3D, p2: Point3D) -> Point3D:
    """
    Calculate midpoint between two points.

    Args:
        p1: First point
        p2: Second point

    Returns:
        Midpoint
    """
    return (
        (p1[0] + p2[0]) / 2,
        (p1[1] + p2[1]) / 2,
        (p1[2] + p2[2]) / 2
    )


def interpolate(p1: Point3D, p2: Point3D, t: float) -> Point3D:
    """
    Linear interpolation between two points.

    Args:
        p1: Start point
        p2: End point
        t: Interpolation parameter (0 = p1, 1 = p2)

    Returns:
        Interpolated point
    """
    return (
        p1[0] + t * (p2[0] - p1[0]),
        p1[1] + t * (p2[1] - p1[1]),
        p1[2] + t * (p2[2] - p1[2])
    )


def are_collinear(p1: Point3D, p2: Point3D, p3: Point3D, tolerance: float = 1e-6) -> bool:
    """
    Check if three points are collinear.

    Args:
        p1, p2, p3: Points to check
        tolerance: Numerical tolerance

    Returns:
        True if points are collinear
    """
    v1 = vector(p1, p2)
    v2 = vector(p1, p3)

    # Points are collinear if cross product is zero
    cross = cross_product(v1, v2)
    return magnitude(cross) < tolerance


def point_on_line_segment(p: Point3D, p1: Point3D, p2: Point3D, tolerance: float = 1e-6) -> bool:
    """
    Check if point p lies on line segment from p1 to p2.

    Args:
        p: Point to check
        p1: Start of line segment
        p2: End of line segment
        tolerance: Numerical tolerance

    Returns:
        True if p is on segment
    """
    # Check if collinear
    if not are_collinear(p, p1, p2, tolerance):
        return False

    # Check if p is between p1 and p2
    # Using dot product method
    v = vector(p1, p2)
    vp = vector(p1, p)

    dot = dot_product(v, vp)
    v_len_sq = dot_product(v, v)

    return -tolerance <= dot <= v_len_sq + tolerance
