# Toldo Abanico - Parametric CAD

Parametric CAD design for a folding fan-style awning structure for Chevrolet S10.

## Overview

This project uses **CadQuery** (Python-based parametric CAD) to design a deployable awning system. All geometry is mathematically defined and fully parametric, enabling easy modifications and optimization.

## Key Features

- **Parametric Design**: All dimensions controlled via YAML configuration
- **Mathematical Geometry**: No magic numbers, all calculations traceable
- **Automated Validation**: pytest ensures geometric correctness
- **Multiple Export Formats**: STEP, STL, DXF
- **Version Controlled**: Full design history in Git
- **Reproducible**: Any collaborator can rebuild from source

## Technology Stack

- **Python 3.12+**
- **CadQuery 2.8+**: Parametric CAD modeling
- **pytest**: Automated validation
- **PyYAML**: Configuration management
- **FreeCAD** (optional): For inspection, drawings, FEM

## Project Structure

```
Cad/
├── .venv/                  # Python virtual environment
├── config/                 # YAML configuration files
│   ├── dimensions.yaml     # All dimensional parameters
│   ├── materials.yaml      # Material properties
│   └── project.yaml        # Project settings
├── src/awning/            # Python source code
│   ├── parameters.py      # Parameter loading
│   ├── geometry.py        # Geometric calculations
│   ├── validation.py      # Validation functions
│   ├── exporters.py       # CAD export utilities
│   └── demo.py            # Demo model generator
├── scripts/               # Utility scripts
├── tests/                 # pytest test suite
├── exports/               # Generated CAD files
│   ├── step/
│   ├── stl/
│   └── dxf/
└── docs/                  # Documentation
```

## Installation

### Prerequisites

- Python 3.10 or higher
- Git (optional but recommended)

### Setup

1. Navigate to project directory:
```powershell
cd "D:\Descargas\02_Proyectos\Toldo Abanico\Cad"
```

2. Activate virtual environment:
```powershell
.\.venv\Scripts\Activate.ps1
```

If you get execution policy errors:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. Verify installation:
```powershell
python -c "import cadquery as cq; print(f'CadQuery {cq.__version__}')"
```

## Usage

### Generate Demo Model

```powershell
.\.venv\Scripts\Activate.ps1
python src/awning/demo.py
```

Or using the script:
```powershell
.\.venv\Scripts\Activate.ps1
python scripts/build_model.py
```

This will generate:
- `exports/step/demo.step` - STEP CAD file
- `exports/stl/demo.stl` - STL mesh file
- `exports/dxf/demo.dxf` - DXF 2D drawing

### Run Tests

```powershell
.\.venv\Scripts\Activate.ps1
pytest
```

Run with verbose output:
```powershell
pytest -v
```

Run specific test file:
```powershell
pytest tests/test_geometry.py
```

### Validate Configuration

```powershell
.\.venv\Scripts\Activate.ps1
python scripts/validate_model.py
```

## Configuration

All design parameters are in `config/dimensions.yaml`:

```yaml
awning:
  span_AB: 2600    # mm - lateral span
  span_AC: 2600    # mm - longitudinal span
```

Parameters marked as `null` are **TBD** (To Be Determined) and need to be defined before full model generation.

## Coordinate System

- **Origin**: Point A (primary structural anchor)
- **X-axis**: Longitudinal (along vehicle length)
- **Y-axis**: Lateral (across vehicle width)
- **Z-axis**: Vertical (height)
- **Units**: Millimeters (mm)
- **Convention**: Right-handed coordinate system

See `docs/coordinate-system.md` for details.

## Known Dimensions

From initial specifications:

- **Vehicle**: Chevrolet S10
  - Total length: 5365 mm
  - Height: 1828 mm

- **Awning**:
  - Distance A-B: 2600 mm (KNOWN)
  - Distance A-C: 2600 mm (KNOWN)

## FreeCAD Integration

To open generated models in FreeCAD:

1. Install FreeCAD (https://www.freecad.org/)
2. Open FreeCAD
3. File → Open → `exports/step/demo.step`

FreeCAD can be used for:
- Visual inspection
- Creating technical drawings (TechDraw workbench)
- Finite Element Analysis (FEM workbench)
- Assembly visualization

## Development Workflow

1. **Modify parameters**: Edit `config/dimensions.yaml`
2. **Run tests**: `pytest` to validate changes
3. **Generate model**: `python src/awning/demo.py`
4. **Inspect**: Open STEP file in FreeCAD
5. **Commit**: Git commit with descriptive message

## Important Notes

### For AI Collaborators

- **Read `AI_CONTEXT.md`** first - contains full project context
- **Read `CONTRIBUTING_AI.md`** - rules for AI modifications
- **Never invent dimensions** - mark as TBD if unknown
- **Run pytest after changes** - ensure nothing broke
- **Follow coordinate system** - defined in docs

### Design Philosophy

This is **NOT** an illustration project. All geometry derives from:

1. **Configuration** (YAML files)
2. **Mathematical calculations** (Python code)
3. **CAD operations** (CadQuery)

Images are for **reference only**, never the source of truth.

## Next Steps

1. Define remaining TBD parameters in `config/dimensions.yaml`
2. Implement actual awning geometry (ribs, pivots, etc.)
3. Add structural validation
4. Create technical drawings in FreeCAD
5. Perform FEM analysis
6. Generate fabrication drawings

## Documentation

- `AI_CONTEXT.md` - Complete context for AI collaborators
- `CONTRIBUTING_AI.md` - Rules for AI modifications
- `ARCHITECTURE.md` - System architecture
- `docs/coordinate-system.md` - Coordinate system definition
- `docs/geometry.md` - Geometric relationships
- `docs/structural-analysis.md` - Structural calculations (future)

## License

Internal project - not for public distribution without permission.

## Contact

Project: Toldo Abanico para Chevrolet S10
Location: D:\Descargas\02_Proyectos\Toldo Abanico\Cad
