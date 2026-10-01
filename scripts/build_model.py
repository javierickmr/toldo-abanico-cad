#!/usr/bin/env python
"""
Build Model Script
==================

Convenience script to build the CAD model and export to all formats.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from awning.demo import main

if __name__ == "__main__":
    main()
