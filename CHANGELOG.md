# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-10-01

### Added
- Initial project structure and infrastructure
- Python virtual environment with CadQuery 2.8.0
- YAML-based parameter management system
  - `config/dimensions.yaml` with known vehicle and awning dimensions
  - `config/materials.yaml` with material property templates
  - `config/project.yaml` with project settings
- Core Python modules:
  - `parameters.py` for YAML configuration loading
  - `geometry.py` for mathematical calculations
  - `validation.py` for geometric validation
  - `exporters.py` for STEP/STL/DXF export
  - `demo.py` for demonstration model generation
- Comprehensive test suite with pytest:
  - Parameter loading tests
  - Geometric calculation tests
  - Export validation tests
  - Volume verification tests
- Complete documentation:
  - `README.md` for human users
  - `AI_CONTEXT.md` for AI collaborators (critical)
  - `CONTRIBUTING_AI.md` with strict rules for AI modifications
  - `ARCHITECTURE.md` describing system design
  - `docs/coordinate-system.md` defining coordinate conventions
  - `docs/geometry.md` documenting geometric relationships
  - `docs/structural-analysis.md` outlining future analysis requirements
- Git repository initialization
- `.gitignore` for Python, CAD, and IDE files
- `pyproject.toml` for project configuration

### Known Dimensions (CONFIRMED)
- Vehicle: Chevrolet S10
  - Length: 5365 mm
  - Height: 1828 mm
- Awning:
  - Distance A-B: 2600 mm
  - Distance A-C: 2600 mm

### To Be Determined (TBD)
- Tube dimensions (diameter, wall thickness)
- Pivot/pin specifications
- Number of folding ribs
- Deployment geometry
- Material selections
- Mounting bracket details
- Canvas/fabric specifications
- Points D, E, F, G, H coordinates

### Notes
- This release establishes the parametric CAD infrastructure
- Demo model successfully generates and exports to STEP/STL/DXF
- All tests pass
- Full model awaits dimensional specifications

## [Unreleased]

### Planned
- Complete dimensional specifications for all components
- Full awning geometry implementation
- Structural point cloud definition (Points D-H)
- Deployment mechanism design
- Canvas geometry
- Structural analysis integration
- FreeCAD technical drawings
- FEM analysis setup
- Fabrication documentation

---

## Version Number Scheme

- **Major** (X.0.0): Breaking changes to architecture or API
- **Minor** (0.X.0): New features, new components, significant additions
- **Patch** (0.0.X): Bug fixes, documentation updates, minor tweaks

## Change Categories

- **Added**: New features, files, or capabilities
- **Changed**: Changes to existing functionality
- **Deprecated**: Features marked for removal
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security-related changes

---

**Maintained by**: Awning CAD Project
**Format**: Keep a Changelog 1.0.0
**Versioning**: Semantic Versioning 2.0.0
