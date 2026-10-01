"""
Validation Module
=================

Provides validation functions for geometric and parametric correctness.

All validations should include appropriate tolerance for numerical precision.
Failed validations raise ValueError with descriptive messages.
"""

from typing import Optional
from .geometry import Point3D, distance


class ValidationError(ValueError):
    """Custom exception for validation failures."""
    pass


def validate_positive(value: float, name: str, strict: bool = True) -> None:
    """
    Validate that a value is positive.

    Args:
        value: Value to validate
        name: Parameter name for error message
        strict: If True, value must be > 0; if False, value must be >= 0

    Raises:
        ValidationError: If validation fails
    """
    if strict and value <= 0:
        raise ValidationError(f"{name} must be positive, got {value}")
    elif not strict and value < 0:
        raise ValidationError(f"{name} must be non-negative, got {value}")


def validate_range(value: float, name: str, min_val: float, max_val: float) -> None:
    """
    Validate that a value is within a range.

    Args:
        value: Value to validate
        name: Parameter name for error message
        min_val: Minimum allowed value
        max_val: Maximum allowed value

    Raises:
        ValidationError: If validation fails
    """
    if not (min_val <= value <= max_val):
        raise ValidationError(
            f"{name} must be between {min_val} and {max_val}, got {value}"
        )


def validate_distance(
    p1: Point3D,
    p2: Point3D,
    expected: float,
    tolerance: float = 0.01,
    name: str = "distance"
) -> None:
    """
    Validate that distance between two points matches expected value.

    Args:
        p1: First point
        p2: Second point
        expected: Expected distance
        tolerance: Allowed deviation
        name: Description for error message

    Raises:
        ValidationError: If distance doesn't match within tolerance
    """
    actual = distance(p1, p2)
    error = abs(actual - expected)

    if error > tolerance:
        raise ValidationError(
            f"{name}: expected {expected:.2f} mm, got {actual:.2f} mm "
            f"(error: {error:.2f} mm, tolerance: {tolerance:.2f} mm)"
        )


def validate_not_coincident(
    p1: Point3D,
    p2: Point3D,
    tolerance: float = 0.01,
    name: str = "points"
) -> None:
    """
    Validate that two points are not coincident.

    Args:
        p1: First point
        p2: Second point
        tolerance: Minimum allowed distance
        name: Description for error message

    Raises:
        ValidationError: If points are too close
    """
    dist = distance(p1, p2)
    if dist < tolerance:
        raise ValidationError(
            f"{name} are coincident or too close: distance = {dist:.4f} mm "
            f"(minimum: {tolerance:.2f} mm)"
        )


def validate_tube_dimensions(
    outer_diameter: float,
    wall_thickness: float,
    name: str = "tube"
) -> None:
    """
    Validate tube dimensions are physically reasonable.

    Args:
        outer_diameter: Outer diameter of tube
        wall_thickness: Wall thickness
        name: Tube name for error message

    Raises:
        ValidationError: If dimensions are invalid
    """
    # Check positive values
    validate_positive(outer_diameter, f"{name} outer diameter")
    validate_positive(wall_thickness, f"{name} wall thickness")

    # Check wall thickness vs diameter
    if wall_thickness >= outer_diameter / 2:
        raise ValidationError(
            f"{name} wall thickness ({wall_thickness} mm) must be less than "
            f"half the outer diameter ({outer_diameter / 2} mm)"
        )

    # Check for reasonable dimensions
    inner_diameter = outer_diameter - 2 * wall_thickness
    if inner_diameter < 1:
        raise ValidationError(
            f"{name} inner diameter too small ({inner_diameter:.2f} mm). "
            f"Check wall thickness."
        )


def validate_volume(
    volume: float,
    expected: float,
    tolerance: float = 0.01,
    name: str = "volume"
) -> None:
    """
    Validate that a volume matches expected value.

    Args:
        volume: Actual volume
        expected: Expected volume
        tolerance: Relative tolerance (fraction, e.g., 0.01 = 1%)
        name: Description for error message

    Raises:
        ValidationError: If volume doesn't match within tolerance
    """
    if expected == 0:
        if abs(volume) > 1e-6:
            raise ValidationError(f"{name}: expected zero volume, got {volume}")
        return

    relative_error = abs(volume - expected) / expected

    if relative_error > tolerance:
        raise ValidationError(
            f"{name}: expected {expected:.2f} mm³, got {volume:.2f} mm³ "
            f"(relative error: {relative_error*100:.2f}%, tolerance: {tolerance*100:.2f}%)"
        )


def validate_non_null(value: any, name: str) -> None:
    """
    Validate that a parameter is not None.

    Args:
        value: Value to check
        name: Parameter name for error message

    Raises:
        ValidationError: If value is None
    """
    if value is None:
        raise ValidationError(
            f"Parameter '{name}' is required but is None/null. "
            f"Please set this value in configuration."
        )


def validate_file_exists(filepath, name: str = "file") -> None:
    """
    Validate that a file exists.

    Args:
        filepath: Path to file
        name: Description for error message

    Raises:
        ValidationError: If file doesn't exist
    """
    from pathlib import Path
    path = Path(filepath)
    if not path.exists():
        raise ValidationError(f"{name} not found: {filepath}")


def validate_file_not_empty(filepath, name: str = "file") -> None:
    """
    Validate that a file exists and is not empty.

    Args:
        filepath: Path to file
        name: Description for error message

    Raises:
        ValidationError: If file doesn't exist or is empty
    """
    from pathlib import Path
    path = Path(filepath)

    validate_file_exists(filepath, name)

    if path.stat().st_size == 0:
        raise ValidationError(f"{name} is empty: {filepath}")
