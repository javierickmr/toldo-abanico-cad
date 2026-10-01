# Geometric Relationships

## Overview

This document defines the geometric relationships between structural points and components.

## Structural Point Cloud

### Primary Points (Known)

- **Point A**: Origin
  - Coordinates: (0, 0, 0)
  - Type: Primary anchor
  - Status: KNOWN (by definition)

- **Point B**: Lateral support
  - Distance from A: 2600 mm
  - Status: KNOWN
  - Coordinates: TBD (pending mounting geometry)

- **Point C**: Longitudinal support
  - Distance from A: 2600 mm
  - Status: KNOWN
  - Coordinates: TBD (pending mounting geometry)

### Secondary Points (TBD)

Points D, E, F, G, H will define:
- Deployment mechanism pivots
- Rib endpoints
- Canvas attachment points
- Additional structural supports

## Distance Constraints

### Known Distances (CONFIRMED)

```
d(A, B) = 2600 mm  ± 0.01 mm
d(A, C) = 2600 mm  ± 0.01 mm
```

These are **validated in tests** and must always be satisfied.

### Unknown Distances (TBD)

All other inter-point distances are TBD pending:
- Deployment mechanism design
- Rib geometry
- Mounting configuration

## Angular Relationships

### TBD
- Deployment angle from stowed to deployed
- Rib angles in deployed configuration
- Mounting angles relative to vehicle

## Geometric Assumptions

### Current Assumptions (Require Confirmation)

1. **Coplanarity**: A, B, C may be coplanar
   - Status: ASSUMPTION
   - Needs confirmation once mounting is defined

2. **Orthogonality**: A-B and A-C may be perpendicular
   - Status: ASSUMPTION
   - Depends on mounting configuration

3. **Symmetry**: Design may have bilateral symmetry
   - Status: ASSUMPTION
   - Depends on deployment mechanism

## Parametric Relationships

### Derived Calculations

When full geometry is defined, these will be calculated:

- **Triangle ABC**: If points are non-collinear
  - Side lengths: AB, BC, CA
  - Angles: ∠ABC, ∠BCA, ∠CAB
  - Area: Using Heron's formula or cross product

- **Rib lengths**: Function of deployment angle and spacing
  - Will be calculated once mechanism is defined

- **Canvas area**: Function of deployed geometry
  - Will be calculated once rib positions are known

## Validation Rules

### Geometric Validity

All geometry must satisfy:

1. **Non-degeneracy**
   - No coincident points (distance > tolerance)
   - No zero-length segments
   - No zero-volume solids

2. **Physical feasibility**
   - Positive dimensions
   - Reasonable proportions
   - No self-intersections

3. **Constraint satisfaction**
   - Known distances maintained
   - Angular limits respected
   - Clearance requirements met

## Tolerance Strategy

### Dimensional Tolerance

- **Tight tolerance**: ± 0.01 mm
  - Use for: Geometric validation in tests
  - Use for: Critical fit dimensions

- **Default tolerance**: ± 0.1 mm
  - Use for: General dimensions
  - Use for: Non-critical features

- **Loose tolerance**: ± 0.5 mm
  - Use for: Canvas, flexible components
  - Use for: Clearance dimensions

### Angular Tolerance

- **Tight**: ± 0.01°
- **Default**: ± 0.1°
- **Loose**: ± 1.0°

## Geometric Dependencies

### Dependency Chain

```
Point A (origin)
    ↓
Point B, C (defined by distances from A)
    ↓
Points D, E, ... (defined by mechanism geometry)
    ↓
Rib positions (function of points and deployment angle)
    ↓
Canvas shape (function of rib positions)
```

Changes propagate down the chain automatically via parametric recalculation.

## Future Geometric Definitions

### To Be Defined

1. **Deployment arc**
   - Center of rotation
   - Radius of deployment
   - Angular range

2. **Rib geometry**
   - Number of ribs
   - Rib spacing
   - Rib profile (straight, curved)
   - Rib endpoints

3. **Pivot locations**
   - Main pivot points
   - Secondary pivots
   - Hinge axes

4. **Canvas attachment**
   - Attachment point spacing
   - Edge geometry
   - Tension distribution

## Coordinate Calculations

### Point Definition Methods

Points can be defined by:

1. **Absolute coordinates**: (x, y, z)
2. **Relative to point**: point + offset
3. **Distance from points**: Trilateration
4. **On line/arc**: Parametric position
5. **Intersection**: Line-line, line-plane, etc.

### Example: Point on Line

```python
def point_on_line(start, end, parameter):
    """
    Point on line segment at parametric position.

    Args:
        start: Start point (x, y, z)
        end: End point (x, y, z)
        parameter: Position [0=start, 1=end]

    Returns:
        Point at parameter position
    """
    return interpolate(start, end, parameter)
```

## Change Management

When geometry changes:

1. **Update YAML**: Change parameters
2. **Run tests**: Validate constraints still satisfied
3. **Regenerate**: Build new CAD model
4. **Inspect**: Verify in FreeCAD
5. **Document**: Record reason for change

## Geometric Verification

### Automated Checks

Tests verify:
- Known distances (A-B, A-C)
- Non-coincident points
- Positive dimensions
- Volume calculations
- Export success

### Manual Checks

Engineer should verify:
- Visual appearance in FreeCAD
- Assembly fit
- Motion clearances (if applicable)
- Structural soundness

---

**Status**: Initial geometric framework
**Next Update**: When points D-H are defined
**Last Updated**: 2026-10-01
