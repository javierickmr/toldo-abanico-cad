#!/usr/bin/env python
"""
Validate Model Script
=====================

Runs validation checks on the CAD model without building it.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from awning.parameters import Parameters
from awning.validation import validate_positive, validate_non_null

def main():
    print("=" * 60)
    print("MODEL VALIDATION")
    print("=" * 60)

    # Load parameters
    print("\n[1/3] Loading parameters...")
    try:
        params = Parameters()
        print("      ✓ Parameters loaded successfully")
    except Exception as e:
        print(f"      ✗ Failed to load parameters: {e}")
        return 1

    # Validate known dimensions
    print("\n[2/3] Validating known dimensions...")
    try:
        span_AB = params.get("awning.span_AB")
        span_AC = params.get("awning.span_AC")

        if span_AB is not None:
            validate_positive(span_AB, "awning.span_AB")
            print(f"      ✓ span_AB = {span_AB} mm")

        if span_AC is not None:
            validate_positive(span_AC, "awning.span_AC")
            print(f"      ✓ span_AC = {span_AC} mm")

        print("      ✓ Dimension validation passed")

    except Exception as e:
        print(f"      ✗ Validation failed: {e}")
        return 1

    # Check for TBD parameters
    print("\n[3/3] Checking for undefined parameters...")
    tbd_params = []

    for param_path in [
        "tubes.main_frame.outer_diameter",
        "tubes.main_frame.wall_thickness",
        "pivots.main_pivot.diameter",
    ]:
        value = params.get(param_path)
        if value is None:
            tbd_params.append(param_path)

    if tbd_params:
        print("      ⚠ The following parameters are not yet defined:")
        for param in tbd_params:
            print(f"        - {param}")
        print("      Note: These must be defined for full model generation")
    else:
        print("      ✓ All critical parameters defined")

    print("\n" + "=" * 60)
    print("VALIDATION COMPLETE")
    print("=" * 60)

    return 0

if __name__ == "__main__":
    sys.exit(main())
