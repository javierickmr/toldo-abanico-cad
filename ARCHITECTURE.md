# System Architecture

## Overview

This document describes the software architecture for the Toldo Abanico parametric CAD system.

## Architecture Layers

The system is organized into distinct layers with clear responsibilities:

```
┌─────────────────────────────────────────────┐
│         CONFIGURATION LAYER                 │
│  YAML files define all parameters          │
└─────────────────┬───────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────┐
│         PARAMETER LAYER                     │
│  Load and validate configuration           │
│  (parameters.py)                            │
└─────────────────┬───────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────┐
│         GEOMETRY LAYER                      │
│  Mathematical calculations                  │
│  Points, vectors, distances                 │
│  (geometry.py)                              │
└─────────────────┬───────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────┐
│         COMPONENT LAYER                     │
│  Create individual CAD components           │
│  Tubes, brackets, pivots, etc.              │
│  (tubes.py, brackets.py, etc.)              │
└─────────────────┬───────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────┐
│         ASSEMBLY LAYER                      │
│  Combine components into complete model     │
│  (assembly.py)                              │
└─────────────────┬───────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────┐
│         VALIDATION LAYER                    │
│  Verify geometric correctness               │
│  (validation.py + pytest)                   │
└─────────────────┬───────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────┐
│         EXPORT LAYER                        │
│  Generate STEP, STL, DXF files              │
│  (exporters.py)                             │
└─────────────────────────────────────────────┘
```

## Separate Concerns

### CAD Modeling
Handled by this system. Generates geometry.

### Structural Analysis
**Separate** from CAD. Includes:
- Load calculations
- Stress analysis
- Factor of safety verification
- Material selection validation

Located in: `calculations/`

### Technical Drawings
**Separate** from CAD. Created in FreeCAD:
- 2D projections
- Dimensioned drawings
- Bill of materials
- Assembly instructions

Located in: `drawings/`

## Data Flow

### Forward Flow (Design)
```
User Input → YAML Config → Parameters → Geometry → CAD → Exports
```

### Validation Flow (Checking)
```
CAD Model → pytest → Validations → Pass/Fail
```

### Analysis Flow (Engineering)
```
CAD Model → Extract Geometry → Structural Solver → Safety Check
```

## Layer Responsibilities

### Configuration Layer
**Files**: `config/*.yaml`

**Responsibilities**:
- Store all dimensional parameters
- Define material properties
- Set project preferences

**Rules**:
- Human-readable YAML
- Commented with units and status
- Version controlled

### Parameter Layer
**Files**: `src/awning/parameters.py`

**Responsibilities**:
- Load YAML configuration
- Provide typed access to parameters
- Validate required parameters exist
- Provide default values

**Rules**:
- No hardcoded dimensions
- Type-safe parameter access
- Clear error messages for missing parameters

### Geometry Layer
**Files**: `src/awning/geometry.py`

**Responsibilities**:
- Point and vector mathematics
- Distance, angle calculations
- Coordinate transformations
- Geometric queries (collinearity, etc.)

**Rules**:
- Pure functions (no side effects)
- Well-tested mathematical operations
- Unit-agnostic (assumes mm)
- No CAD operations here

### Component Layer
**Files**: `src/awning/tubes.py`, `brackets.py`, etc.

**Responsibilities**:
- Create individual CAD parts
- Apply parameters to CadQuery operations
- Return CadQuery Workplane objects

**Rules**:
- One component type per file
- Parametric (accept dimensions as arguments)
- Validated inputs
- Documented units

### Assembly Layer
**Files**: `src/awning/assembly.py`

**Responsibilities**:
- Combine components into complete model
- Position components in 3D space
- Define relationships between parts
- Create CadQuery Assembly

**Rules**:
- Use geometry layer for positioning
- Reference parameter layer for dimensions
- Validate assembly constraints

### Validation Layer
**Files**: `src/awning/validation.py`, `tests/*.py`

**Responsibilities**:
- Geometric validation functions
- Automated test suite (pytest)
- Known dimension checks
- Export verification

**Rules**:
- Test all critical dimensions
- Validate known values (A-B=2600, etc.)
- Check for degenerate geometry
- Verify export file generation

### Export Layer
**Files**: `src/awning/exporters.py`

**Responsibilities**:
- Export to STEP format
- Export to STL format
- Export to DXF format
- File system management

**Rules**:
- Validate exports succeed
- Check file size > 0
- Create output directories
- Handle export errors gracefully

## Module Dependencies

```
parameters.py       (no dependencies)
    ↓
geometry.py         (no dependencies)
    ↓
validation.py       (depends on: geometry)
    ↓
components/*.py     (depends on: parameters, geometry, validation, cadquery)
    ↓
assembly.py         (depends on: components, parameters, geometry)
    ↓
exporters.py        (depends on: cadquery)
```

## Coordinate System

**Global Convention**:
- Origin: Point A (primary mounting point)
- X-axis: Longitudinal (vehicle length)
- Y-axis: Lateral (vehicle width)
- Z-axis: Vertical (up)
- Right-handed system

**Local Coordinates**:
Components may use local coordinate systems, but must:
- Document the local system clearly
- Provide transformation to global
- Never assume global = local

## Error Handling Strategy

### Configuration Errors
- Missing files → Clear error with path
- Invalid YAML → Show line number
- Missing required param → Show parameter name

### Geometric Errors
- Invalid dimensions → Show actual vs. allowed
- Degenerate geometry → Show problematic values
- Validation failures → Show expected vs. actual

### Export Errors
- Failed export → Show format and reason
- Missing directory → Create automatically
- Empty file → Raise error immediately

## Testing Strategy

### Unit Tests
Test individual functions in isolation:
- `test_parameters.py`: Parameter loading
- `test_geometry.py`: Geometric calculations
- `test_validation.py`: Validation functions

### Integration Tests
Test complete workflows:
- `test_exports.py`: Full export pipeline
- `test_assembly.py`: Component integration

### Validation Tests
Test known values:
- A-B distance = 2600 mm
- A-C distance = 2600 mm
- Expected volumes

## Extension Points

### Adding New Components
1. Create `src/awning/component_name.py`
2. Define creation function with parameters
3. Add to `assembly.py`
4. Create tests in `tests/test_component_name.py`
5. Update documentation

### Adding New Parameters
1. Add to `config/dimensions.yaml`
2. Document units and status
3. Use in component creation
4. Add validation test
5. Update documentation

### Adding New Export Formats
1. Add function to `exporters.py`
2. Handle errors appropriately
3. Add test in `test_exports.py`
4. Update configuration

## Performance Considerations

### Current Approach
- Load all parameters once
- Calculate geometry on demand
- Generate CAD when requested
- Cache not implemented (not needed yet)

### Future Optimizations
If performance becomes an issue:
- Cache parameter loading
- Memoize expensive calculations
- Parallelize component generation
- Optimize CadQuery operations

## Security Considerations

### Not Applicable
This is a local CAD tool, not a web service.

### File System Safety
- Only write to project directory
- Create directories as needed
- Don't delete files automatically
- Warn before overwriting

## Deployment

### Current
- Local development only
- Manual execution
- Git version control

### Future
- CI/CD pipeline (optional)
- Automated testing on commit
- Release versioning
- Documentation generation

## Maintenance

### Documentation Updates
When changing architecture:
1. Update this file
2. Update `AI_CONTEXT.md`
3. Update relevant docstrings
4. Update tests

### Version Compatibility
- Python: 3.10+
- CadQuery: 2.4+
- pytest: 7.0+
- PyYAML: 6.0+

## Separation of Concerns

### What This System Does
✅ Parametric CAD modeling
✅ Geometric calculations
✅ Export to standard formats
✅ Validation of geometry

### What This System Does NOT Do
❌ Structural analysis (separate)
❌ Material stress calculations (separate)
❌ 2D drawing generation (FreeCAD)
❌ Bill of materials (FreeCAD)
❌ Fabrication instructions (separate docs)

## Design Principles

1. **Single Responsibility**: Each module has one clear purpose
2. **Dependency Inversion**: Depend on abstractions (parameters), not concrete values
3. **Open/Closed**: Open for extension, closed for modification
4. **Don't Repeat Yourself**: Parameters defined once, used many times
5. **Explicit is Better**: Clear naming, documented units, no magic

## Future Architecture Enhancements

### Planned
- Component library system
- Assembly constraint solver
- Parametric variation studies
- Integration with FreeCAD macros

### Under Consideration
- Web-based parameter editor
- Visual assembly viewer
- Automated drawing generation
- BOM generation from assembly

---

**Last Updated**: 2026-10-01
