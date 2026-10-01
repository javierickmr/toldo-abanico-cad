# AI CONTEXT - Toldo Abanico CAD Project

**CRITICAL**: Read this document COMPLETELY before making any modifications to this project.

## Project Summary

**Objective**: Design a parametric, deployable, fan-style folding awning for a Chevrolet S10 pickup truck.

**Approach**: Mathematical CAD modeling using Python and CadQuery, with all geometry derived from parameters and calculations.

**Status**: Initial infrastructure complete. Awaiting detailed dimensional specifications to build full model.

## What We're Building

A folding awning that mounts to a Chevrolet S10 and deploys to provide shade/weather protection. The design uses a fan-fold mechanism similar to Japanese fans.

## Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| CAD Engine | CadQuery | 2.8.0 | Parametric 3D modeling |
| Language | Python | 3.12.10 | Programming |
| Testing | pytest | Latest | Validation |
| Config | PyYAML | Latest | Parameter management |
| Export | STEP/STL/DXF | - | CAD interchange |
| Future | FreeCAD | TBD | Drawings, FEM |

## Project Location

**ABSOLUTE PATH**: `D:\Descargas\02_Proyectos\Toldo Abanico\Cad`

**Virtual Environment**: `D:\Descargas\02_Proyectos\Toldo Abanico\Cad\.venv`

**NEVER** work outside this directory.
**NEVER** install packages globally.
**ALWAYS** activate `.venv` before running Python.

## Architecture

```
PARAMETERS (YAML)
      ↓
GEOMETRY (Mathematical)
      ↓
COMPONENTS (CadQuery)
      ↓
ASSEMBLY
      ↓
VALIDATION (pytest)
      ↓
EXPORTS (STEP/STL/DXF)
```

**Separate concerns**:
- CAD geometry ≠ Structural analysis
- 3D modeling ≠ 2D drawings
- Design ≠ Fabrication instructions

## Coordinate System

**Convention**: Right-handed Cartesian

- **X**: Longitudinal (along vehicle length, forward = +X)
- **Y**: Lateral (across vehicle width, right = +Y when facing forward)
- **Z**: Vertical (up = +Z)
- **Origin**: Point A (primary structural mounting point)
- **Units**: Millimeters (mm)

**CRITICAL**: All code must use this convention consistently.

## Known Dimensions (CONFIRMED)

These values are KNOWN and must NOT be changed without authorization:

```yaml
Vehicle: Chevrolet S10
- Total length: 5365 mm
- Height: 1828 mm

Awning:
- Distance A to B: 2600 mm
- Distance A to C: 2600 mm
```

## Unknown Dimensions (TBD)

The following are NOT yet specified:

- Tube diameters and wall thicknesses
- Pivot/pin dimensions
- Number of folding ribs
- Deployment angle
- Material specifications
- Mounting bracket details
- Canvas/fabric specifications

**DO NOT INVENT THESE VALUES**. Mark as `null` in YAML until confirmed.

## Structural Points

Current known points:
- **Point A**: Primary anchor (origin: 0, 0, 0)
- **Point B**: 2600mm from A (lateral direction)
- **Point C**: 2600mm from A (longitudinal direction)

Future points D, E, F, G, H will define additional structure.

## Data Classification

Every parameter must be tagged:

- **KNOWN**: Measured or confirmed by user
- **CALCULATED**: Derived mathematically from KNOWN values
- **ASSUMPTION**: Estimated, needs confirmation
- **TBD**: Not yet determined

**NEVER** change KNOWN → ASSUMPTION without explicit approval.

## File Structure

### Source Files (EDIT THESE)
- `config/*.yaml` - All parameters
- `src/awning/*.py` - Python source code
- `tests/*.py` - Test suite
- `docs/*.md` - Documentation

### Generated Files (DO NOT EDIT)
- `exports/step/*.step` - Generated STEP files
- `exports/stl/*.stl` - Generated STL files
- `exports/dxf/*.dxf` - Generated DXF files

**IMPORTANT**: Never manually edit generated CAD files. Regenerate from source.

## How to Activate Environment

### PowerShell
```powershell
cd "D:\Descargas\02_Proyectos\Toldo Abanico\Cad"
.\.venv\Scripts\Activate.ps1
```

### Bash (Git Bash on Windows)
```bash
cd "/d/Descargas/02_Proyectos/Toldo Abanico/Cad"
source .venv/Scripts/activate
```

### Verify
```bash
python -c "import cadquery; print('CadQuery OK')"
```

## How to Run Tests

```bash
# All tests
pytest

# Verbose
pytest -v

# Specific test
pytest tests/test_geometry.py -v

# With coverage
pytest --cov=src/awning
```

**ALWAYS** run tests after modifying code.

## How to Generate Model

```bash
# Demo model
python src/awning/demo.py

# Or via script
python scripts/build_model.py
```

## How to Validate Configuration

```bash
python scripts/validate_model.py
```

## Critical Rules

### Geometry Rules
1. **No magic numbers** - All dimensions from config or calculations
2. **No hardcoded coordinates** - Derive from parameters
3. **Maintain coordinate system** - X=longitudinal, Y=lateral, Z=vertical
4. **Validate everything** - Distance, angles, volumes, non-degeneracy

### Parameter Rules
1. **Never invent dimensions** - Use `null` for unknown
2. **Never change KNOWN without approval** - These are confirmed
3. **Document ASSUMPTIONS** - Mark clearly in YAML comments
4. **Separate CALCULATED from KNOWN** - Don't mix sources

### Code Rules
1. **Type hints** - Use typing module
2. **Docstrings** - All functions must have docstrings
3. **Units in docstrings** - State units explicitly (mm, degrees, etc.)
4. **Validation** - Use `validation.py` functions
5. **No silent failures** - Raise exceptions with clear messages

### Testing Rules
1. **Test after changes** - Always run pytest
2. **Test known values** - Validate A-B = 2600mm, A-C = 2600mm
3. **Test edge cases** - Zero vectors, coincident points, etc.
4. **Test exports** - Verify files exist and non-empty

### Git Rules
1. **Commit source, not artifacts** - Don't commit generated STEP/STL
2. **Descriptive messages** - Explain WHY, not just WHAT
3. **Small commits** - Logical, atomic changes
4. **Test before commit** - Ensure tests pass

## Common Tasks

### Add New Parameter
1. Edit `config/dimensions.yaml`
2. Add with appropriate tag (KNOWN/CALCULATED/ASSUMPTION/TBD)
3. Document units and meaning
4. Add validation in tests
5. Run `pytest`

### Add New Component
1. Create function in appropriate module (e.g., `tubes.py`)
2. Use parameters from `Parameters` class
3. Add docstring with units
4. Add validation
5. Write tests
6. Export to STEP/STL

### Modify Geometry
1. Read current implementation
2. Understand coordinate system
3. Modify calculations
4. Run tests - **THEY MUST PASS**
5. Regenerate model
6. Inspect in FreeCAD

## Validation Checklist

Before considering any work complete:

- [ ] All parameters documented in YAML
- [ ] All dimensions have units specified
- [ ] pytest runs without failures
- [ ] STEP file generates successfully
- [ ] STEP file is non-empty (>1KB typically)
- [ ] STL file generates successfully
- [ ] Known dimensions validated (A-B=2600, A-C=2600)
- [ ] No magic numbers in code
- [ ] Coordinate system followed
- [ ] Git commit with meaningful message

## What NOT To Do

### ❌ NEVER
- Invent dimensions without marking as ASSUMPTION
- Edit STEP/STL/DXF files manually
- Use images as geometric source of truth
- Install Python packages globally
- Work outside the project directory
- Change known dimensions without approval
- Skip pytest after changes
- Use inconsistent coordinate system
- Hardcode values in Python
- Commit broken tests

### ✅ ALWAYS
- Load dimensions from YAML
- Derive geometry mathematically
- Run pytest after changes
- Use `.venv` virtual environment
- Document assumptions clearly
- Validate calculations
- Export from code, never manually
- Follow coordinate conventions
- Tag data status (KNOWN/CALCULATED/ASSUMPTION/TBD)
- Ask for clarification when uncertain

## Images Are NOT Source of Truth

**CRITICAL PRINCIPLE**: This is a CAD project, not an illustration project.

Images can be used for:
- Visual reference
- Design inspiration
- Documentation
- Communication

Images CANNOT be used for:
- Extracting dimensions (unreliable)
- Replacing mathematical geometry
- Source of truth for design

**Always**: Parameters → Geometry → CAD Model → Drawings
**Never**: Image → Dimensions → CAD Model

## Design Philosophy

1. **Parametric**: Change one parameter, entire model updates
2. **Traceable**: Every dimension has a source
3. **Validated**: Automated tests prevent errors
4. **Reproducible**: Anyone can rebuild from source
5. **Professional**: Engineering standards, not quick hacks

## Structural Analysis (Future)

CAD geometry does NOT prove structural safety.

Separate structural analysis will include:
- Load calculations (self-weight, wind, snow)
- Stress analysis (bending, shear, torsion)
- Factor of safety verification
- Fatigue considerations
- FEM validation

**Never** claim a design is "safe" just because it renders in CAD.

## Next Steps for This Project

1. Obtain missing dimensions (tube sizes, pivots, etc.)
2. Define complete structural point cloud (D, E, F, G, H)
3. Implement full awning geometry
4. Create assembly with all components
5. Generate technical drawings in FreeCAD
6. Perform structural calculations
7. Run FEM analysis
8. Create fabrication drawings
9. Build prototype

## When Resuming This Project

1. **Read this file** (you're doing it now ✓)
2. Read `CONTRIBUTING_AI.md` for detailed rules
3. Read `ARCHITECTURE.md` for system design
4. Activate `.venv`
5. Run `pytest` to ensure environment works
6. Run `python src/awning/demo.py` to verify CAD pipeline
7. Review `config/dimensions.yaml` for current parameters
8. Check Git status: `git status`

## Getting Help

If you encounter:
- **Import errors**: Check `.venv` is activated
- **Test failures**: Read error message, check coordinate system
- **Export failures**: Verify output directories exist
- **Parameter errors**: Check YAML syntax, required values

## Questions to Ask User Before Proceeding

When uncertain, ask:
- "Is this dimension KNOWN or should I mark it as TBD?"
- "Should I use ASSUMPTION or wait for confirmation?"
- "Is this structural point confirmed?"
- "Do you want me to implement this now or mark as future work?"

## Success Criteria

This project is successful when:
1. All dimensions are defined (no TBD)
2. Full parametric model generates
3. All tests pass
4. Exports work correctly
5. Model can be opened in FreeCAD
6. Technical drawings can be created
7. Structural analysis confirms safety
8. Fabrication drawings are complete

## Current Status

**Phase**: Initial infrastructure ✓
**Next Phase**: Detailed dimensional specification
**Blocking**: Need tube sizes, pivot dimensions, deployment geometry

**What Works**:
- Python environment ✓
- CadQuery installation ✓
- Parameter loading ✓
- Geometric calculations ✓
- Validation system ✓
- Export pipeline ✓
- Demo model generation ✓
- Test suite ✓

**What Needs Work**:
- Full awning geometry (awaiting dimensions)
- Complete structural point definitions
- Material selection
- Structural analysis
- Technical drawings

---

**Last Updated**: 2026-10-01
**Project Version**: 0.1.0
**Python Version**: 3.12.10
**CadQuery Version**: 2.8.0
