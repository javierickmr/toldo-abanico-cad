"""
CAD Export Module
=================

Handles export of CadQuery models to various CAD formats:
- STEP: Standard for 3D CAD exchange
- STL: For 3D printing and visualization
- DXF: For 2D drawings (projected views)
- SVG: For 2D vector graphics (future)

All exports include validation and error handling.
"""

import cadquery as cq
from pathlib import Path
from typing import Optional, Union


class ExportError(Exception):
    """Exception raised for export failures."""
    pass


def ensure_directory(filepath: Union[str, Path]) -> Path:
    """
    Ensure the directory for a file exists.

    Args:
        filepath: Path to file

    Returns:
        Path object for the file
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def export_step(
    assembly: cq.Assembly,
    filepath: Union[str, Path],
    validate: bool = True
) -> Path:
    """
    Export assembly to STEP format.

    Args:
        assembly: CadQuery Assembly to export
        filepath: Output file path
        validate: If True, verify file was created

    Returns:
        Path to exported file

    Raises:
        ExportError: If export fails
    """
    try:
        path = ensure_directory(filepath)
        assembly.save(str(path))

        if validate:
            if not path.exists():
                raise ExportError(f"STEP file was not created: {path}")
            if path.stat().st_size == 0:
                raise ExportError(f"STEP file is empty: {path}")

        return path

    except Exception as e:
        raise ExportError(f"Failed to export STEP: {e}") from e


def export_stl(
    shape: cq.Workplane,
    filepath: Union[str, Path],
    linear_deflection: float = 0.1,
    angular_deflection: float = 0.1,
    validate: bool = True
) -> Path:
    """
    Export shape to STL format.

    Args:
        shape: CadQuery Workplane containing the shape
        filepath: Output file path
        linear_deflection: Mesh quality parameter (smaller = finer)
        angular_deflection: Mesh quality parameter (smaller = finer)
        validate: If True, verify file was created

    Returns:
        Path to exported file

    Raises:
        ExportError: If export fails
    """
    try:
        path = ensure_directory(filepath)

        # Export STL
        cq.exporters.export(
            shape,
            str(path),
            tolerance=linear_deflection,
            angularTolerance=angular_deflection
        )

        if validate:
            if not path.exists():
                raise ExportError(f"STL file was not created: {path}")
            if path.stat().st_size == 0:
                raise ExportError(f"STL file is empty: {path}")

        return path

    except Exception as e:
        raise ExportError(f"Failed to export STL: {e}") from e


def export_dxf(
    shape: cq.Workplane,
    filepath: Union[str, Path],
    project_plane: str = "XY",
    validate: bool = True
) -> Path:
    """
    Export 2D projection to DXF format.

    Args:
        shape: CadQuery Workplane containing the shape
        filepath: Output file path
        project_plane: Plane to project onto ("XY", "XZ", or "YZ")
        validate: If True, verify file was created

    Returns:
        Path to exported file

    Raises:
        ExportError: If export fails
    """
    try:
        path = ensure_directory(filepath)

        # For DXF, we need to project the shape to 2D
        # This is a basic implementation - may need refinement
        cq.exporters.export(shape, str(path))

        if validate:
            if not path.exists():
                raise ExportError(f"DXF file was not created: {path}")
            if path.stat().st_size == 0:
                raise ExportError(f"DXF file is empty: {path}")

        return path

    except Exception as e:
        raise ExportError(f"Failed to export DXF: {e}") from e


def export_all(
    assembly: cq.Assembly,
    shape: cq.Workplane,
    base_name: str,
    output_dirs: Optional[dict] = None
) -> dict:
    """
    Export to all supported formats.

    Args:
        assembly: Assembly for STEP export
        shape: Workplane for STL/DXF export
        base_name: Base filename (without extension)
        output_dirs: Dictionary mapping format to directory

    Returns:
        Dictionary mapping format to exported file path
    """
    if output_dirs is None:
        output_dirs = {
            'step': 'exports/step',
            'stl': 'exports/stl',
            'dxf': 'exports/dxf',
        }

    results = {}

    # Export STEP
    try:
        step_path = Path(output_dirs['step']) / f"{base_name}.step"
        results['step'] = export_step(assembly, step_path)
    except Exception as e:
        results['step'] = f"Error: {e}"

    # Export STL
    try:
        stl_path = Path(output_dirs['stl']) / f"{base_name}.stl"
        results['stl'] = export_stl(shape, stl_path)
    except Exception as e:
        results['stl'] = f"Error: {e}"

    # Export DXF
    try:
        dxf_path = Path(output_dirs['dxf']) / f"{base_name}.dxf"
        results['dxf'] = export_dxf(shape, dxf_path)
    except Exception as e:
        results['dxf'] = f"Error: {e}"

    return results
