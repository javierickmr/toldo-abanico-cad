# Structural Analysis Framework

## Important Disclaimer

**CAD GEOMETRY ≠ STRUCTURAL SAFETY**

The CAD model can render perfectly and still be structurally inadequate. This document outlines the separate structural analysis that MUST be performed.

## Analysis Required

### 1. Load Cases

#### Static Loads
- **Self-weight**: Mass of frame, canvas, hardware
- **Snow load**: If applicable to region
- **Personnel load**: If accessible during deployment

#### Dynamic Loads
- **Wind load**: Primary design driver
  - Operating wind speed (deployed)
  - Survival wind speed (stowed)
  - Gust factors
- **Impact**: Deployment shock, road vibrations
- **Vehicle motion**: Acceleration, braking, cornering

#### Combined Loads
- Worst-case combinations per applicable codes
- Factor of safety per load type

### 2. Stress Analysis

For each structural member:

- **Axial stress**: Tension, compression
- **Bending stress**: Moment-induced
- **Shear stress**: Transverse and torsional
- **Combined stress**: Von Mises equivalent
- **Buckling**: Critical for slender members
- **Fatigue**: Cyclic loading considerations

### 3. Connection Analysis

- **Welds**: Size, length, type
- **Bolts**: Diameter, grade, preload
- **Pins/Pivots**: Bearing stress, shear
- **Anchors**: Vehicle mounting points

### 4. Deflection Limits

- **Serviceability**: Maximum acceptable deflection
- **Aesthetics**: Visible sag under load
- **Function**: Interference with operation

## Analysis Methods

### Hand Calculations

For preliminary design:
- Simple beam equations
- Basic stress formulas
- Conservative assumptions

**Location**: `calculations/hand_calcs.md`

### Finite Element Method (FEM)

For detailed verification:
- FreeCAD FEM workbench
- Mesh quality requirements
- Boundary conditions
- Load application
- Result interpretation

**Location**: `calculations/fem/`

## Material Properties

### Required Data

For each material:
- Elastic modulus (E)
- Yield strength (σ_y)
- Ultimate strength (σ_u)
- Density (ρ)
- Poisson's ratio (ν)

**Source**: `config/materials.yaml`

**Note**: All material properties in YAML are ASSUMPTIONS until confirmed.

## Safety Factors

### Recommended Minimums

- **Static loads**: FS ≥ 3.0
- **Dynamic loads**: FS ≥ 5.0
- **Fatigue**: FS ≥ 2.0 on fatigue limit

**Actual factors**: Must be determined by qualified engineer based on:
- Consequence of failure
- Load uncertainty
- Material variability
- Fabrication quality

## Design Constraints

### Geometric Constraints

From CAD model:
- Member lengths
- Cross-sections
- Joint locations
- Clearances

### Performance Constraints

User requirements:
- Maximum deployed wind speed
- Maximum deflection
- Minimum service life
- Weight limit

## Analysis Workflow

```
1. Define Load Cases
   ↓
2. Extract Geometry from CAD
   ↓
3. Apply Material Properties
   ↓
4. Perform Hand Calculations
   ↓
5. Check Against Limits
   ↓
6. If OK: Verify with FEM
   ↓
7. If Not OK: Revise Design → Update CAD → Repeat
   ↓
8. Document Results
```

## Wind Load Calculation

### Simplified Approach

```
F_wind = 0.5 * ρ_air * V² * A * C_d

Where:
  ρ_air = 1.225 kg/m³ (sea level, 15°C)
  V = wind speed (m/s)
  A = projected area (m²)
  C_d = drag coefficient (depends on shape)
```

### Detailed Approach

- Use local wind code (ASCE 7, EN 1991, etc.)
- Account for exposure category
- Include gust effects
- Consider dynamic response

**Location**: `calculations/wind_loads.py`

## Critical Failure Modes

To be analyzed:

1. **Tube buckling**: Compression members
2. **Pivot shear**: Pins/hinge bolts
3. **Canvas tearing**: Fabric stress
4. **Weld failure**: Joint strength
5. **Mounting failure**: Anchor pullout
6. **Fatigue cracking**: Cyclic stress points

## Analysis Documentation

Each analysis must include:

1. **Assumptions**: Clearly stated
2. **Loads**: Magnitude, direction, application point
3. **Boundary conditions**: Supports, constraints
4. **Material data**: Source, uncertainty
5. **Calculations**: Step-by-step or FEM setup
6. **Results**: Stress, deflection, safety factor
7. **Conclusion**: Pass/fail, recommendations

## FEM Guidelines

### Mesh Requirements

- **Element type**: Appropriate for geometry
- **Element size**: Convergence study
- **Aspect ratio**: < 10 typically
- **Mesh refinement**: At stress concentrations

### Boundary Conditions

- **Supports**: Realistic constraint
- **Loads**: Correct direction and magnitude
- **Contacts**: Appropriate for joints

### Result Validation

- **Check equilibrium**: Sum forces = 0
- **Check units**: Consistent throughout
- **Sanity check**: Order of magnitude reasonable
- **Compare to hand calc**: Should be similar

## Iteration Loop

```
Design (CAD) → Analysis → Results
      ↑                      ↓
      └──── Fail: Revise ────┘
                 ↓
              Pass: Document
```

## Responsibility

**CRITICAL**: Structural analysis must be performed by or reviewed by a qualified engineer.

This software generates geometry. It does NOT validate structural adequacy.

## Future Work

### Not Yet Implemented

- [ ] Automated load case generation
- [ ] FEM automation via FreeCAD macros
- [ ] Optimization routines
- [ ] Fatigue life prediction
- [ ] Cost vs. weight optimization

### Planned

- [ ] Integration with structural codes
- [ ] Parametric stress maps
- [ ] Automated factor of safety checks
- [ ] Design iteration automation

## References

### Codes and Standards

**TBD**: Determine applicable codes based on:
- Location (country, region)
- Application (vehicle-mounted structure)
- Loads (wind, snow, etc.)

Possible references:
- ASCE 7: Minimum Design Loads
- EN 1991: Eurocode - Actions on structures
- AISC Steel Construction Manual
- AWS D1.1: Structural Welding Code

### Analysis Software

- FreeCAD FEM (free, open-source)
- Frame3DD (open-source frame analysis)
- Hand calculations (spreadsheet)

### Material References

- ASM Metals Handbook
- ASTM Standards
- Material manufacturer datasheets

## Checklist Before Fabrication

**DO NOT fabricate until**:

- [ ] All load cases defined
- [ ] All materials specified
- [ ] Hand calculations complete
- [ ] FEM analysis complete (if required)
- [ ] All safety factors ≥ minimum
- [ ] All deflections < limits
- [ ] All failure modes checked
- [ ] Engineer review complete
- [ ] Documentation complete

## Contact

For structural analysis questions:
**Consult a licensed professional engineer**

---

**Status**: Framework defined, analysis pending
**Last Updated**: 2026-10-01
