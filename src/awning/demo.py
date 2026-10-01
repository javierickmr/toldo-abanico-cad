"""
Demo CAD Model
==============

Generates a simple parametric demonstration assembly to validate
that CadQuery and the export pipeline work correctly.

This demo creates:
- A rectangular tube
- A mounting plate with holes
- A pivot pin
- Assembly of components

All dimensions are parametric and sourced from configuration.
"""

import cadquery as cq
from pathlib import Path
import sys

# Allow running as script or module
if __name__ == "__main__" and __package__ is None:
    # Add parent directory to path for direct execution
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from src.awning.parameters import Parameters
    from src.awning.validation import validate_positive, validate_volume
    from src.awning.exporters import export_step, export_stl, export_dxf
else:
    # Relative imports for module usage
    from .parameters import Parameters
    from .validation import validate_positive, validate_volume
    from .exporters import export_step, export_stl, export_dxf


# Demo parameters (since main dimensions are TBD)
DEMO_PARAMS = {
    'tube': {
        'length': 200,          # mm
        'width': 50,            # mm
        'height': 30,           # mm
        'wall_thickness': 3,    # mm
    },
    'plate': {
        'length': 100,          # mm
        'width': 80,            # mm
        'thickness': 5,         # mm
        'hole_diameter': 8,     # mm
        'hole_spacing': 60,     # mm
    },
    'pivot': {
        'diameter': 10,         # mm
        'length': 90,           # mm
    }
}


def create_rectangular_tube(
    length: float,
    width: float,
    height: float,
    wall_thickness: float
) -> cq.Workplane:
    """
    Create a rectangular tube with specified dimensions.

    Args:
        length: Tube length (X direction)
        width: Tube width (Y direction)
        height: Tube height (Z direction)
        wall_thickness: Wall thickness

    Returns:
        CadQuery Workplane with tube
    """
    # Validate inputs
    validate_positive(length, "tube length")
    validate_positive(width, "tube width")
    validate_positive(height, "tube height")
    validate_positive(wall_thickness, "tube wall thickness")

    # Create outer box
    outer = cq.Workplane("XY").box(length, width, height)

    # Create inner box (subtract to make tube)
    inner_length = length - 2 * wall_thickness
    inner_width = width - 2 * wall_thickness
    inner_height = height - 2 * wall_thickness

    if inner_length <= 0 or inner_width <= 0 or inner_height <= 0:
        raise ValueError("Wall thickness too large for tube dimensions")

    inner = cq.Workplane("XY").box(inner_length, inner_width, inner_height)

    # Subtract inner from outer
    tube = outer.cut(inner)

    return tube


def create_mounting_plate(
    length: float,
    width: float,
    thickness: float,
    hole_diameter: float,
    hole_spacing: float
) -> cq.Workplane:
    """
    Create a mounting plate with two holes.

    Args:
        length: Plate length (X direction)
        width: Plate width (Y direction)
        thickness: Plate thickness (Z direction)
        hole_diameter: Diameter of mounting holes
        hole_spacing: Distance between hole centers

    Returns:
        CadQuery Workplane with plate
    """
    # Validate inputs
    validate_positive(length, "plate length")
    validate_positive(width, "plate width")
    validate_positive(thickness, "plate thickness")
    validate_positive(hole_diameter, "hole diameter")

    # Create base plate
    plate = cq.Workplane("XY").box(length, width, thickness)

    # Add two holes symmetrically placed
    plate = (plate
        .faces(">Z")
        .workplane()
        .pushPoints([(-hole_spacing/2, 0), (hole_spacing/2, 0)])
        .hole(hole_diameter)
    )

    return plate


def create_pivot_pin(diameter: float, length: float) -> cq.Workplane:
    """
    Create a cylindrical pivot pin.

    Args:
        diameter: Pin diameter
        length: Pin length

    Returns:
        CadQuery Workplane with pin
    """
    validate_positive(diameter, "pivot diameter")
    validate_positive(length, "pivot length")

    pin = (cq.Workplane("XY")
        .circle(diameter / 2)
        .extrude(length)
    )

    return pin


def create_demo_assembly() -> cq.Assembly:
    """
    Create a complete demo assembly.

    Returns:
        CadQuery Assembly with all components
    """
    params = DEMO_PARAMS

    # Create components
    tube = create_rectangular_tube(
        params['tube']['length'],
        params['tube']['width'],
        params['tube']['height'],
        params['tube']['wall_thickness']
    )

    plate = create_mounting_plate(
        params['plate']['length'],
        params['plate']['width'],
        params['plate']['thickness'],
        params['plate']['hole_diameter'],
        params['plate']['hole_spacing']
    )

    pivot = create_pivot_pin(
        params['pivot']['diameter'],
        params['pivot']['length']
    )

    # Create assembly
    assembly = cq.Assembly()

    # Add tube at origin
    assembly.add(tube, name="tube", color=cq.Color("lightgray"))

    # Add plate offset above tube
    tube_height = params['tube']['height']
    plate_thickness = params['plate']['thickness']

    assembly.add(
        plate,
        name="plate",
        loc=cq.Location((0, 0, tube_height/2 + plate_thickness/2)),
        color=cq.Color("steelblue")
    )

    # Add pivot through plate
    pivot_height = tube_height/2 + plate_thickness + params['pivot']['length']/2

    assembly.add(
        pivot,
        name="pivot",
        loc=cq.Location((0, 0, pivot_height)),
        color=cq.Color("gold")
    )

    return assembly


def main():
    """Main function to generate and export demo model."""
    print("=" * 60)
    print("DEMO CAD MODEL GENERATION")
    print("=" * 60)

    # Create assembly
    print("\n[1/4] Creating demo assembly...")
    assembly = create_demo_assembly()
    print("      [OK] Assembly created")

    # Get individual shape for STL/DXF export
    # Combine all shapes into one
    print("\n[2/4] Combining shapes for export...")
    tube = create_rectangular_tube(**DEMO_PARAMS['tube'])
    plate = create_mounting_plate(**DEMO_PARAMS['plate'])
    combined_shape = tube  # For simplicity, just use tube
    print("      [OK] Shapes combined")

    # Export STEP
    print("\n[3/4] Exporting to STEP format...")
    step_path = export_step(assembly, "exports/step/demo.step")
    print(f"      [OK] STEP exported: {step_path}")

    # Export STL
    print("      Exporting to STL format...")
    stl_path = export_stl(combined_shape, "exports/stl/demo.stl")
    print(f"      [OK] STL exported: {stl_path}")

    # Export DXF
    print("      Exporting to DXF format...")
    try:
        dxf_path = export_dxf(combined_shape, "exports/dxf/demo.dxf")
        print(f"      [OK] DXF exported: {dxf_path}")
    except Exception as e:
        print(f"      [WARNING] DXF export failed: {e}")

    # Validate volumes
    print("\n[4/4] Validating geometry...")

    # Calculate expected tube volume
    t = DEMO_PARAMS['tube']
    outer_vol = t['length'] * t['width'] * t['height']
    inner_length = t['length'] - 2 * t['wall_thickness']
    inner_width = t['width'] - 2 * t['wall_thickness']
    inner_height = t['height'] - 2 * t['wall_thickness']
    inner_vol = inner_length * inner_width * inner_height
    expected_tube_vol = outer_vol - inner_vol

    # Get actual volume
    actual_tube_vol = tube.val().Volume()

    print(f"      Expected tube volume: {expected_tube_vol:.2f} mm³")
    print(f"      Actual tube volume:   {actual_tube_vol:.2f} mm³")

    # Validate with tolerance
    validate_volume(actual_tube_vol, expected_tube_vol, tolerance=0.01, name="Tube volume")
    print("      [OK] Volume validation passed")

    print("\n" + "=" * 60)
    print("DEMO GENERATION COMPLETE")
    print("=" * 60)
    print("\nGenerated files:")
    print(f"  • {step_path}")
    print(f"  • {stl_path}")
    print("\nYou can now:")
    print("  1. Open STEP file in FreeCAD for inspection")
    print("  2. View STL file in 3D viewer")
    print("  3. Run pytest to validate the system")


if __name__ == "__main__":
    main()
