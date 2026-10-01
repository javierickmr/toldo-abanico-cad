# AI Contribution Guidelines

**MANDATORY READING** for all AI agents working on this project.

## Core Principles

This document contains **strict rules** that must be followed. Violations compromise project integrity.

## Rule 1: Dimension Integrity

### ✅ ALLOWED
- Use dimensions marked as KNOWN
- Calculate dimensions from KNOWN values
- Mark unknown dimensions as `null` or TBD
- Request clarification for ambiguous dimensions
- Document ASSUMPTIONS with clear tags

### ❌ FORBIDDEN
- **Inventing dimensions** without user approval
- Changing KNOWN dimensions without explicit authorization
- Using "typical" or "standard" values without marking as ASSUMPTION
- Extracting dimensions from images (unreliable)
- Guessing structural dimensions
- Converting KNOWN → ASSUMPTION silently
- Converting TBD → ASSUMPTION without documentation

### Example Violation
```yaml
# WRONG - inventing value
tubes:
  main_frame:
    outer_diameter: 25.4  # ❌ Where did this come from?
```

### Correct Approach
```yaml
# CORRECT - marking as unknown
tubes:
  main_frame:
    outer_diameter: null  # TBD - awaiting specification
```

## Rule 2: No Magic Numbers

### ✅ ALLOWED
- All dimensions from YAML configuration
- Calculated values with clear derivation
- Mathematical constants (π, √2, etc.)
- Standard conversions with documentation

### ❌ FORBIDDEN
- Hardcoded dimensions in Python code
- Undocumented constants
- Dimensions in comments that aren't in YAML
- "Temporary" hardcoded values

### Example Violation
```python
# WRONG
def create_tube():
    return cq.Workplane("XY").circle(12.7).extrude(200)  # ❌ Magic numbers
```

### Correct Approach
```python
# CORRECT
def create_tube(diameter: float, length: float):
    return cq.Workplane("XY").circle(diameter/2).extrude(length)

# In caller:
params = Parameters()
diameter = params.validate_required('tubes.main_frame.outer_diameter')
length = params.validate_required('tubes.main_frame.length')
tube = create_tube(diameter, length)
```

## Rule 3: Images Are Not Geometric Source

### ✅ ALLOWED
- Using images for visual reference
- Using images for design inspiration
- Using images in documentation
- Discussing what images show

### ❌ FORBIDDEN
- Measuring dimensions from images
- Using image dimensions as KNOWN
- Replacing mathematical geometry with image-derived data
- Claiming image dimensions are accurate

### Rationale
Images have:
- Unknown scale
- Perspective distortion
- Measurement uncertainty
- No guarantees of accuracy

### If You Must Use Image Information
1. Mark as ASSUMPTION, not KNOWN
2. Document source: "Based on image, needs confirmation"
3. Add large uncertainty margin
4. Flag for user verification

## Rule 4: Units Must Be Explicit

### ✅ ALLOWED
- All dimensions in millimeters (mm)
- Angles in degrees (specify in docstring)
- Volumes in mm³
- Documenting units in docstrings
- Converting with clear documentation

### ❌ FORBIDDEN
- Mixing units without conversion
- Assuming units
- Using imperial without conversion
- Undocumented unit assumptions

### Example
```python
# CORRECT
def calculate_area(width: float, height: float) -> float:
    """
    Calculate rectangular area.

    Args:
        width: Width in millimeters
        height: Height in millimeters

    Returns:
        Area in square millimeters (mm²)
    """
    return width * height
```

## Rule 5: Coordinate System Consistency

### ✅ REQUIRED
- X = longitudinal (vehicle length)
- Y = lateral (vehicle width)
- Z = vertical (height)
- Origin at Point A
- Right-handed system
- Document any local coordinate systems

### ❌ FORBIDDEN
- Mixing coordinate conventions
- Undocumented coordinate transformations
- Assuming different axis meanings
- Inconsistent handedness

## Rule 6: Test After Every Change

### ✅ REQUIRED
- Run `pytest` after modifying code
- Add tests for new functionality
- Validate known dimensions (A-B=2600, A-C=2600)
- Verify exports generate successfully

### ❌ FORBIDDEN
- Committing code without running tests
- Disabling tests to make code "pass"
- Ignoring test failures
- Assuming code works without verification

### Test Command
```bash
pytest -v
```

**All tests must pass** before considering work complete.

## Rule 7: Validate Everything

### ✅ REQUIRED
- Validate positive dimensions
- Validate reasonable ranges
- Validate non-degenerate geometry
- Validate distance between points
- Validate volumes
- Validate file generation

### ❌ FORBIDDEN
- Skipping validation for "simple" cases
- Assuming inputs are valid
- Silent failures
- Continuing with invalid geometry

### Example
```python
# CORRECT
from awning.validation import validate_positive, validate_distance

validate_positive(diameter, "tube diameter")
validate_distance(point_A, point_B, expected=2600, tolerance=0.01)
```

## Rule 8: Never Edit Generated Files

### ✅ SOURCE FILES (Edit These)
- `config/*.yaml`
- `src/**/*.py`
- `tests/**/*.py`
- `docs/**/*.md`
- `scripts/**/*.py`

### ❌ GENERATED FILES (Never Edit)
- `exports/step/*.step`
- `exports/stl/*.stl`
- `exports/dxf/*.dxf`
- Any file generated by Python scripts

### To Modify Geometry
1. Edit Python source code
2. Run generation script
3. Verify output
4. **Never** edit STEP/STL/DXF manually

## Rule 9: Document Assumptions

### ✅ REQUIRED
When making assumptions:
- Mark clearly in YAML comments
- Tag with `status: ASSUMPTION`
- Document reasoning
- Flag for user review

### Example
```yaml
tubes:
  main_frame:
    outer_diameter: 25.4  # ASSUMPTION - typical structural tube size
    wall_thickness: 2.0   # ASSUMPTION - standard gauge
    material: "steel_a36" # ASSUMPTION - common structural steel

    # NOTE: All above values are ASSUMPTIONS pending user confirmation
    # Source: Typical structural tube specifications
    # Confidence: LOW - requires engineering review
```

## Rule 10: Separate CAD from Analysis

### ✅ UNDERSTAND
- CAD geometry ≠ Structural safety
- Rendering ≠ Proven strength
- Assembly fit ≠ Load capacity
- 3D model ≠ Fabrication plan

### ❌ FORBIDDEN
- Claiming design is "safe" because model generates
- Skipping structural calculations
- Assuming CAD validates design
- Replacing engineering analysis with visualization

### Correct Approach
1. Generate CAD geometry
2. **Separately** perform structural analysis
3. **Separately** calculate loads, stresses
4. **Separately** verify safety factors
5. Iterate if analysis shows problems

## Rule 11: Handle Contradictions

### ✅ REQUIRED
When encountering contradictions:
1. **STOP** - Don't proceed with conflicting data
2. **FLAG** - Clearly identify the contradiction
3. **REPORT** - Inform user of conflict
4. **WAIT** - Get clarification before continuing

### ❌ FORBIDDEN
- Silently choosing one value over another
- Averaging conflicting dimensions
- Assuming newer data is correct
- Proceeding with contradictory information

### Example Response
```
⚠️  CONTRADICTION DETECTED

Config file says: awning.span_AB = 2600 mm
User just said: "The span should be 2400 mm"

These conflict. Which is correct?
- Keep 2600 mm (current KNOWN value)
- Change to 2400 mm (requires update)
- Something else?

I cannot proceed until this is resolved.
```

## Rule 12: Git Discipline

### ✅ REQUIRED
- Commit source code changes
- Write descriptive commit messages
- Test before committing
- Small, logical commits

### ❌ FORBIDDEN
- Committing broken tests
- Committing generated files (unless specifically requested)
- Vague commit messages ("updated files")
- Massive commits mixing unrelated changes

### Good Commit Messages
```
Add tube diameter validation to prevent degenerate geometry

Implemented min/max diameter checks in validation.py to catch
unreasonable tube dimensions before CAD generation.

- Added validate_tube_dimensions() function
- Added tests in test_validation.py
- All tests pass
```

## Rule 13: Function Documentation

### ✅ REQUIRED
- Docstring for every function
- Document parameters with types and units
- Document return values with types and units
- Document exceptions raised

### Example
```python
def create_tube(
    outer_diameter: float,
    wall_thickness: float,
    length: float
) -> cq.Workplane:
    """
    Create a cylindrical tube.

    Args:
        outer_diameter: Outer diameter in millimeters
        wall_thickness: Wall thickness in millimeters
        length: Tube length in millimeters

    Returns:
        CadQuery Workplane containing the tube geometry

    Raises:
        ValueError: If dimensions are invalid (negative, zero, or
                   wall_thickness >= outer_diameter/2)
    """
    # Implementation...
```

## Rule 14: Error Messages

### ✅ REQUIRED
- Clear, descriptive error messages
- Include actual vs expected values
- Suggest how to fix
- Reference relevant configuration

### ❌ FORBIDDEN
- Generic errors ("Invalid value")
- Errors without context
- Swallowed exceptions
- Silent failures

### Example
```python
# GOOD
raise ValueError(
    f"Tube wall thickness ({wall_thickness} mm) must be less than "
    f"half the outer diameter ({outer_diameter/2} mm). "
    f"Check 'tubes.main_frame.wall_thickness' in config/dimensions.yaml"
)

# BAD
raise ValueError("Invalid thickness")  # ❌ Not helpful
```

## Rule 15: Type Hints

### ✅ REQUIRED
- Type hints on function parameters
- Type hints on return values
- Use `typing` module for complex types
- Use `Optional` for nullable values

### Example
```python
from typing import Optional, Tuple

def calculate_position(
    base_point: Tuple[float, float, float],
    offset: float,
    direction: Optional[str] = None
) -> Tuple[float, float, float]:
    # Implementation...
```

## Enforcement

These rules are **mandatory**. Violations will result in:
1. Test failures (automated enforcement)
2. Rejected contributions
3. Required rework
4. Loss of trust in AI-generated code

## When Uncertain

**ALWAYS** prefer to:
1. Ask the user
2. Mark as TBD
3. Document assumptions
4. Flag for review

**NEVER**:
1. Guess
2. Assume
3. Invent
4. Proceed with uncertainty

## Summary Checklist

Before completing any task:

- [ ] No invented dimensions
- [ ] No magic numbers
- [ ] All units documented
- [ ] Coordinate system consistent
- [ ] Tests added and passing
- [ ] Validations in place
- [ ] No manual edits of generated files
- [ ] Assumptions clearly documented
- [ ] No contradictions unresolved
- [ ] Git commit is clean and descriptive
- [ ] Documentation updated
- [ ] Error messages are helpful
- [ ] Type hints present
- [ ] CAD vs analysis separation maintained

## Emergency Contact

If you encounter:
- Contradictory requirements → **STOP and ask user**
- Missing critical dimensions → **Mark TBD and ask user**
- Conflicting coordinate systems → **STOP and ask user**
- Structural safety questions → **Flag for engineering review**
- Unexplained test failures → **Report and investigate**

---

**Remember**: Quality over speed. Correct over convenient. Safety over simplicity.

**Last Updated**: 2026-10-01
