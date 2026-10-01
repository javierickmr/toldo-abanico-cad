# Coordinate System Definition

## Global Coordinate System

This project uses a **right-handed Cartesian coordinate system** with the following convention:

### Axis Definitions

- **X-axis (Longitudinal)**
  - Direction: Along vehicle length
  - Positive direction: Forward (toward front of vehicle)
  - Negative direction: Rearward (toward back of vehicle)

- **Y-axis (Lateral)**
  - Direction: Across vehicle width
  - Positive direction: Right (when facing forward)
  - Negative direction: Left (when facing forward)

- **Z-axis (Vertical)**
  - Direction: Height
  - Positive direction: Up (away from ground)
  - Negative direction: Down (toward ground)

### Origin

The origin (0, 0, 0) is located at **Point A**, the primary structural anchor point.

Point A will be defined relative to the vehicle once mounting position is determined.

## Handedness Verification

Right-handed system check:
- X × Y = Z ✓
- Y × Z = X ✓
- Z × X = Y ✓

## Visual Representation

```
         Z (up)
         |
         |
         |
         +-------→ Y (right)
        /
       /
      ↙
     X (forward)
```

## Structural Points

### Known Points

- **Point A**: Origin (0, 0, 0)
  - Primary anchor point
  - Reference for all other measurements

- **Point B**: (0, 2600, 0) - PRELIMINARY
  - 2600 mm lateral from Point A
  - Same longitudinal position
  - Same height

- **Point C**: (2600, 0, 0) - PRELIMINARY
  - 2600 mm forward from Point A
  - Same lateral position
  - Same height

**NOTE**: Above coordinates are preliminary assumptions assuming A, B, C are coplanar at Z=0. Actual coordinates will be refined when mounting geometry is defined.

### Future Points

Points D, E, F, G, H will be defined as the design develops.

## Units

- **Length**: Millimeters (mm)
- **Angles**: Degrees (°) unless otherwise specified
- **Volume**: Cubic millimeters (mm³)

## Transformations

### Local to Global

When components use local coordinate systems:
1. Define local origin in global coordinates
2. Define local axis orientations
3. Provide transformation matrix
4. Document clearly in component code

### Example

```python
# Component with local coordinates
local_origin_global = (100, 200, 50)  # mm in global system
local_rotation = (0, 0, 45)  # degrees around global Z

# Transform local point (10, 0, 0) to global
# ... transformation code ...
```

## Validation

All code must:
1. Use consistent axis definitions
2. Document coordinate system assumptions
3. Validate transformations
4. Test with known points

## Coordinate System Rules

### DO
✅ Always specify units in comments
✅ Use descriptive variable names (x_forward, y_lateral, z_up)
✅ Document local coordinate systems
✅ Validate against known points
✅ Use right-handed system

### DON'T
❌ Mix coordinate conventions
❌ Assume axis meanings
❌ Use undocumented transformations
❌ Change global convention
❌ Use left-handed systems

## Reference Checks

To verify coordinate system compliance:

```python
# Check 1: Known distance
A = (0, 0, 0)
B = (0, 2600, 0)
assert distance(A, B) == 2600

# Check 2: Right-handedness
X = (1, 0, 0)
Y = (0, 1, 0)
Z_expected = (0, 0, 1)
Z_calculated = cross_product(X, Y)
assert Z_calculated == Z_expected
```

## CadQuery Conventions

CadQuery uses:
- Right-handed coordinates ✓ (matches our system)
- Default workplane: XY plane at Z=0 ✓
- Extrusion: Positive Z direction by default ✓

Our system aligns with CadQuery defaults.

## FreeCAD Conventions

FreeCAD uses:
- Right-handed coordinates ✓
- X, Y, Z similar to our convention ✓
- Models will import correctly ✓

## Common Pitfalls

### Pitfall 1: Mixing Conventions
```python
# WRONG - inconsistent naming
front_distance = y_coordinate  # ❌ Y is lateral, not longitudinal
```

### Pitfall 2: Undocumented Rotations
```python
# WRONG - unclear transformation
rotated = component.rotate((0,0,0), (1,1,0), 45)  # ❌ What axis? What direction?

# CORRECT
# Rotate 45° around axis from origin toward (1,1,0) in global coords
rotated = component.rotate((0,0,0), (1,1,0), 45)
```

### Pitfall 3: Implicit Coordinates
```python
# WRONG - unclear which coordinate
position = 2600  # ❌ X, Y, or Z?

# CORRECT
y_lateral = 2600  # mm, lateral distance
```

## Vehicle Coordinate Context

When vehicle is positioned:
- **Front of vehicle**: +X direction
- **Driver's side**: -Y direction (left when facing forward)
- **Passenger side**: +Y direction (right when facing forward)
- **Roof**: +Z direction

## Awning Deployment Direction

**TBD**: Define deployment direction once mechanism is designed.

Likely options:
- Deploy in +Y direction (to passenger side)
- Deploy in ±Y direction (both sides)
- Deploy with rotation about X or Z axis

## Change Log

- 2026-10-01: Initial coordinate system definition
- Future: Update when Point A vehicle location is defined
- Future: Update when deployment mechanism is designed

---

**CRITICAL**: Any code that violates this coordinate system will fail geometric validation tests.
