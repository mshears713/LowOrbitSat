"""
═══════════════════════════════════════════════════════════════════
MODULE: utils/timing.py
PURPOSE: Satellite pass timeline simulation
THEME: Satellites aren't always overhead - timing matters!
═══════════════════════════════════════════════════════════════════

📡 STORY:
Satellites orbit Earth. They're only visible (and in range)
for a few minutes during each "pass" overhead.

Signal strength follows a curve:
  - Weak when satellite rises above horizon
  - Strong when directly overhead (maximum elevation)
  - Weak again as it sets

This module simulates that timeline.

SATELLITE PASS VISUALIZATION:
┌──────────────────────────────────────────────────────────────┐
│                    SATELLITE PASS                             │
│                                                               │
│  Elevation                        📡 Satellite                │
│    90° │             ___/────\___                             │
│        │           _/            \_                           │
│    45° │        __/                \__                        │
│        │      _/                      \_                      │
│     0° ├─────/────────────────────────\─────                  │
│        │   Rise                       Set                     │
│        │   (AOS)                     (LOS)                    │
│        │                                                      │
│        └───────────────────────────────────►Time             │
│                                                               │
│  Signal Strength ∝ sin(elevation angle)                       │
│                                                               │
└──────────────────────────────────────────────────────────────┘

LEARNING GOALS:
  • Satellite passes and visibility windows
  • Signal strength variation over time
  • Time-based simulation
  • Simplified orbital mechanics

SIMPLIFICATIONS:
  - No real orbital mechanics (Keplerian elements)
  - Simplified elevation model (parabolic arc)
  - Fixed pass duration
  - Single ground station

═══════════════════════════════════════════════════════════════════
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional


@dataclass
class SatellitePass:
    """
    Represents a satellite pass over a ground station.

    🎓 TEACHING NOTE:
    A "pass" is when a satellite is visible from your location.
    It has a start time, end time, and peak (max elevation).

    Attributes
    ----------
    start_time : float
        When satellite rises above horizon (seconds)
    duration : float
        How long the pass lasts (seconds)
    max_elevation_deg : float
        Highest angle satellite reaches above horizon (degrees)
        - 90° = directly overhead (best)
        - 30° = good pass
        - 10° = low pass (marginal)
    """
    start_time: float  # seconds
    duration: float  # seconds
    max_elevation_deg: float  # degrees

    def __post_init__(self):
        """Validate pass parameters."""
        if self.start_time < 0:
            raise ValueError("start_time must be >= 0")
        if self.duration <= 0:
            raise ValueError("duration must be > 0")
        if not 0 <= self.max_elevation_deg <= 90:
            raise ValueError("max_elevation_deg must be between 0 and 90")

    @property
    def end_time(self):
        """When satellite sets below horizon."""
        return self.start_time + self.duration

    @property
    def peak_time(self):
        """When satellite reaches maximum elevation."""
        return self.start_time + (self.duration / 2)

    def __repr__(self):
        return (f"SatellitePass(start={self.start_time:.1f}s, "
                f"duration={self.duration:.1f}s, "
                f"max_elev={self.max_elevation_deg:.1f}°)")


def elevation_angle_curve(time_array, satellite_pass: SatellitePass):
    """
    Calculate elevation angle over time for a satellite pass.

    🎓 TEACHING NOTE:
    The satellite rises from horizon (0°), reaches peak elevation,
    then sets back to horizon.

    We model this as a parabolic curve (inverted parabola).

    Real Orbital Mechanics:
    Uses Keplerian elements, SGP4 propagation, etc.
    Our Model:
    Simple parabola - easy to understand!

    Parameters
    ----------
    time_array : np.ndarray
        Time points to evaluate (seconds)
    satellite_pass : SatellitePass
        Pass parameters

    Returns
    -------
    elevations : np.ndarray
        Elevation angle in degrees at each time point
    """
    elevations = np.zeros_like(time_array, dtype=float)

    # Find times during the pass
    in_pass = (time_array >= satellite_pass.start_time) & (time_array <= satellite_pass.end_time)

    if not np.any(in_pass):
        return elevations  # Satellite not visible

    # 🎓 PARABOLIC ELEVATION MODEL
    # Normalized time within pass (0 to 1)
    t_pass = time_array[in_pass] - satellite_pass.start_time
    t_normalized = t_pass / satellite_pass.duration

    # Parabolic curve: peaks at t=0.5, zero at t=0 and t=1
    # Formula: elevation = max_elev * 4 * t * (1 - t)
    # This gives a nice symmetric arc
    elevations[in_pass] = satellite_pass.max_elevation_deg * 4 * t_normalized * (1 - t_normalized)

    return elevations


def signal_strength_curve(time_array, satellite_pass: SatellitePass,
                         max_strength=1.0, min_strength=0.1):
    """
    Calculate signal strength over time during a satellite pass.

    🎓 TEACHING NOTE:
    Signal strength depends on elevation angle.
    Higher elevation = shorter path through atmosphere = stronger signal.

    We use a simplified model:
    strength ∝ sin(elevation)

    Why sine?
    - At 0° (horizon): sin(0°) = 0 (weak/no signal)
    - At 90° (overhead): sin(90°) = 1 (max signal)
    - Smooth transition in between

    Parameters
    ----------
    time_array : np.ndarray
        Time points (seconds)
    satellite_pass : SatellitePass
        Pass parameters
    max_strength : float
        Maximum signal strength (at peak elevation)
    min_strength : float
        Minimum signal strength (at horizon)

    Returns
    -------
    strengths : np.ndarray
        Signal strength at each time point (normalized 0-1)
    """
    # Get elevation angles
    elevations_deg = elevation_angle_curve(time_array, satellite_pass)

    # Convert to radians
    elevations_rad = np.radians(elevations_deg)

    # 🎓 SIGNAL STRENGTH = sin(elevation)
    # This gives realistic variation:
    # - Zero at horizon
    # - Maximum at zenith
    raw_strength = np.sin(elevations_rad)

    # Scale to desired range
    strengths = min_strength + (max_strength - min_strength) * raw_strength

    return strengths


def distance_curve(time_array, satellite_pass: SatellitePass,
                  altitude_km=500, min_distance_km=None):
    """
    Calculate satellite-to-ground-station distance over time.

    🎓 TEACHING NOTE:
    Distance affects signal strength (inverse square law).

    At horizon: distance = √(altitude² + (Earth_radius)²) ≈ very far
    Overhead: distance = altitude (minimum)

    We use simplified geometry:
    distance ≈ altitude / sin(elevation)

    Parameters
    ----------
    time_array : np.ndarray
        Time points (seconds)
    satellite_pass : SatellitePass
        Pass parameters
    altitude_km : float
        Satellite orbital altitude in km (default: 500 km for LEO)
    min_distance_km : float, optional
        Minimum distance (at peak). If None, uses altitude_km.

    Returns
    -------
    distances : np.ndarray
        Distance in km at each time point
    """
    if min_distance_km is None:
        min_distance_km = altitude_km

    # Get elevation angles
    elevations_deg = elevation_angle_curve(time_array, satellite_pass)
    elevations_rad = np.radians(elevations_deg)

    # 🎓 SIMPLIFIED DISTANCE MODEL
    # distance = altitude / sin(elevation)
    # At zenith (90°): distance = altitude
    # At horizon (0°): distance → infinity (we'll cap it)

    distances = np.full_like(time_array, min_distance_km * 10, dtype=float)

    # Only calculate for non-zero elevations
    nonzero = elevations_rad > np.radians(5)  # Avoid division by zero
    if np.any(nonzero):
        distances[nonzero] = min_distance_km / np.sin(elevations_rad[nonzero])

    return distances


def generate_pass_timeline(satellite_pass: SatellitePass, sample_rate_hz=10):
    """
    Generate complete timeline data for a satellite pass.

    🎓 TEACHING NOTE:
    This combines everything: elevation, signal strength, distance.
    It creates a full simulation of what happens during a pass.

    Useful for:
    - Visualizing passes
    - Planning communication windows
    - Understanding signal variations

    Parameters
    ----------
    satellite_pass : SatellitePass
        Pass to simulate
    sample_rate_hz : float
        How many samples per second (default: 10 Hz)

    Returns
    -------
    timeline : dict
        {
            'time': np.ndarray,
            'elevation_deg': np.ndarray,
            'signal_strength': np.ndarray,
            'distance_km': np.ndarray
        }
    """
    # Create time array covering the pass
    total_time = satellite_pass.duration + 10  # Add margin
    num_samples = int(total_time * sample_rate_hz)
    time_array = np.linspace(satellite_pass.start_time - 5,
                            satellite_pass.end_time + 5,
                            num_samples)

    # Calculate all metrics
    elevations = elevation_angle_curve(time_array, satellite_pass)
    strengths = signal_strength_curve(time_array, satellite_pass)
    distances = distance_curve(time_array, satellite_pass)

    return {
        'time': time_array,
        'elevation_deg': elevations,
        'signal_strength': strengths,
        'distance_km': distances,
        'pass': satellite_pass
    }


def find_communication_window(satellite_pass: SatellitePass,
                              min_elevation_deg=10):
    """
    Find the usable communication window within a pass.

    🎓 TEACHING NOTE:
    Not the entire pass is usable!
    - Very low elevations → poor signal
    - Usually need elevation > 10° for reliable comms

    This function finds when the satellite is "high enough"
    for good communication.

    Parameters
    ----------
    satellite_pass : SatellitePass
        Satellite pass
    min_elevation_deg : float
        Minimum usable elevation (default: 10°)

    Returns
    -------
    window : dict
        {
            'start_time': float,
            'end_time': float,
            'duration': float
        }
        or None if pass never reaches min elevation
    """
    # Can we reach the minimum elevation?
    if satellite_pass.max_elevation_deg < min_elevation_deg:
        return None  # Pass not high enough

    # 🎓 CALCULATE WINDOW
    # The elevation curve is parabolic.
    # We need to find when it crosses min_elevation threshold.

    # Sample the pass
    timeline = generate_pass_timeline(satellite_pass, sample_rate_hz=100)

    # Find where elevation >= threshold
    above_threshold = timeline['elevation_deg'] >= min_elevation_deg

    if not np.any(above_threshold):
        return None

    # Find start and end indices
    indices = np.where(above_threshold)[0]
    start_idx = indices[0]
    end_idx = indices[-1]

    start_time = timeline['time'][start_idx]
    end_time = timeline['time'][end_idx]

    return {
        'start_time': start_time,
        'end_time': end_time,
        'duration': end_time - start_time,
        'min_elevation': min_elevation_deg
    }


# ═══ DEBUGGING NOTES ═══
#
# Common Issues:
#   1. Elevation always zero? Check if time is within pass duration
#   2. Signal strength negative? Check min_strength parameter
#   3. Distance infinite? Elevation might be too low (< 5°)
#   4. Parabola asymmetric? Check start/end times are correct
#
# Testing Tips:
#   - Plot elevation vs time to verify parabolic shape
#   - Check peak occurs at midpoint of pass
#   - Verify elevation = 0 at start and end
#   - Test edge cases: very low passes, very high passes
#   - Compare signal strength to elevation curve
#
# Gotchas:
#   - Time is in seconds (not minutes or hours)
#   - Elevation in degrees (not radians) for user interface
#   - Distance model is simplified (not true orbital geometry)
#   - Parabolic model doesn't match real orbital paths exactly


# ═══ FUTURE IMPROVEMENTS ═══
#
# For Advanced Version (ORBITER-1):
#   [ ] Real SGP4/SDP4 orbital propagation
#   [ ] Two-Line Element (TLE) support
#   [ ] Multiple ground stations
#   [ ] Doppler shift calculation
#   [ ] Azimuth and elevation angles
#   [ ] Earth oblateness effects
#
# For Deep Space Version:
#   [ ] Planetary ephemerides
#   [ ] Light-time corrections
#   [ ] Relativistic effects
#   [ ] Multi-hour communication windows
