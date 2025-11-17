"""
═══════════════════════════════════════════════════════════════════
MODULE: runtime/__init__.py
PURPOSE: Runtime orchestration package for ORBITER-0
THEME: Bringing all the pieces together
═══════════════════════════════════════════════════════════════════

This package contains the high-level runtime orchestration that ties
together all components of the ORBITER-0 system:
  - Signal generation
  - Channel modeling
  - Packet transmission
  - Error correction
  - Mission archival

It's the conductor of our satellite communications orchestra!

═══════════════════════════════════════════════════════════════════
"""

from .pipeline import simulate_transmission, simulate_satellite_pass

__all__ = ['simulate_transmission', 'simulate_satellite_pass']
