"""
═══════════════════════════════════════════════════════════════════
MODULE: channel/fades.py
PURPOSE: Simulate temporary signal dropouts and burst errors
THEME: Sometimes the signal just... disappears for a moment
═══════════════════════════════════════════════════════════════════

📡 STORY:
Ever listen to FM radio while driving under a bridge?
The signal cuts out momentarily. That's a FADE!

Fades are temporary drops in signal strength caused by:
  - Obstacles (buildings, mountains, the Earth itself)
  - Atmospheric scintillation (turbulence)
  - Multipath interference
  - Weather (rain, clouds)

FADE TYPES:
┌──────────────────────────────────────────────────────────────┐
│ SHALLOW FADE: Signal weakens but doesn't disappear          │
│   Normal: ████████████████                                  │
│   Faded:  ████▓▓▓▓████████  (50% strength)                  │
├──────────────────────────────────────────────────────────────┤
│ DEEP FADE: Signal nearly vanishes                           │
│   Normal: ████████████████                                  │
│   Faded:  ████░░░░████████  (10% strength)                  │
├──────────────────────────────────────────────────────────────┤
│ BURST FADE: Multiple rapid fades                            │
│   ████▓░▓░▓░░░▓▓████  (choppy, intermittent)                │
└──────────────────────────────────────────────────────────────┘

LEARNING GOALS:
  • Understanding burst errors vs random errors
  • Time-varying channel effects
  • Why error correction is crucial
  • Modeling realistic impairments

SIMPLIFICATIONS:
  - Fades are simple rectangular dropouts
  - No multipath modeling
  - Predetermined fade events (not random processes)

═══════════════════════════════════════════════════════════════════
"""

import numpy as np
from dataclasses import dataclass
from typing import List


# ┌────────────────────────────────────────────────────────┐
# │              FADE EVENT TIMELINE                       │
# ├────────────────────────────────────────────────────────┤
# │                                                        │
# │  Signal Strength                                       │
# │    100% ▓▓▓▓▓▓╌╌╌╌▓▓▓▓▓▓▓▓▓▓╌╌╌▓▓▓▓▓▓                 │
# │     50% ┊     ┊░░░┊    ┊       ░┊                     │
# │      0% ┊     ┊   ┊    ┊       ░┊                     │
# │         └─────┴───┴────┴───────┴┴─────> Time          │
# │               ▲        ▲        ▲                      │
# │              Fade    Normal   Burst                    │
# │              event            fade                     │
# │                                                        │
# └────────────────────────────────────────────────────────┘


@dataclass
class FadeEvent:
    """
    Represents a signal fade event.

    🎓 TEACHING NOTE:
    A fade is defined by WHEN it happens, HOW LONG it lasts,
    and HOW SEVERE it is.

    Attributes
    ----------
    start_time : float
        When the fade begins (seconds)
    duration : float
        How long the fade lasts (seconds)
    attenuation : float
        Signal reduction factor (0.0 = total loss, 1.0 = no fade)
        - 1.0 = normal (100% strength)
        - 0.5 = shallow fade (50% strength)
        - 0.1 = deep fade (10% strength)
        - 0.0 = complete dropout
    """
    start_time: float
    duration: float
    attenuation: float

    def __post_init__(self):
        """Validate fade parameters."""
        # 🎓 SANITY CHECKS
        if self.start_time < 0:
            raise ValueError("start_time must be >= 0")
        if self.duration <= 0:
            raise ValueError("duration must be > 0")
        if not 0.0 <= self.attenuation <= 1.0:
            raise ValueError("attenuation must be between 0.0 and 1.0")

    @property
    def end_time(self):
        """When the fade ends."""
        return self.start_time + self.duration

    def is_active_at(self, time):
        """Check if fade is active at given time."""
        return self.start_time <= time < self.end_time

    def __repr__(self):
        return (f"FadeEvent(t={self.start_time:.2f}s, "
                f"dur={self.duration:.2f}s, "
                f"atten={self.attenuation:.2f})")


def apply_fades_to_signal(signal, time_axis, fade_events: List[FadeEvent]):
    """
    Apply fade events to a time-domain signal.

    🎓 TEACHING NOTE:
    This function looks at each signal sample and checks:
    "Is there a fade happening right now?"
    If yes, multiply the signal by the attenuation factor.

    WHY MULTIPLY?
    Attenuation is a REDUCTION in signal amplitude.
    - attenuation = 1.0 → signal × 1.0 = unchanged
    - attenuation = 0.5 → signal × 0.5 = half strength
    - attenuation = 0.0 → signal × 0.0 = complete loss

    Parameters
    ----------
    signal : np.ndarray
        Original signal samples
    time_axis : np.ndarray
        Time values for each sample (seconds)
    fade_events : List[FadeEvent]
        List of fades to apply

    Returns
    -------
    faded_signal : np.ndarray
        Signal with fades applied
    """
    # Start with original signal
    faded_signal = signal.copy()

    # 🎓 PROCESS EACH SAMPLE
    for i, t in enumerate(time_axis):
        # Check all fade events
        for fade in fade_events:
            if fade.is_active_at(t):
                # 🎓 APPLY ATTENUATION
                # Multiple fades multiply together (worst case)
                faded_signal[i] *= fade.attenuation

    return faded_signal


def generate_random_fades(duration_sec, num_fades=3, fade_severity='mixed'):
    """
    Generate random fade events for testing.

    🎓 TEACHING NOTE:
    Real fades happen randomly based on environment.
    This function creates realistic fade patterns for simulation.

    Parameters
    ----------
    duration_sec : float
        Total duration to generate fades over (seconds)
    num_fades : int
        Number of fade events to create
    fade_severity : str
        Type of fades: 'shallow', 'deep', 'mixed'

    Returns
    -------
    fade_events : List[FadeEvent]
        Generated fade events
    """
    import random

    fade_events = []

    # 🎓 SEVERITY PROFILES
    severity_profiles = {
        'shallow': (0.5, 0.8),   # 50-80% signal remains
        'deep': (0.05, 0.3),     # 5-30% signal remains
        'mixed': (0.1, 0.9)      # Wide range
    }

    min_atten, max_atten = severity_profiles.get(fade_severity, (0.1, 0.9))

    for _ in range(num_fades):
        # Random timing
        start_time = random.uniform(0, duration_sec)

        # Random duration (0.1 to 2.0 seconds)
        fade_duration = random.uniform(0.1, 2.0)

        # Random severity
        attenuation = random.uniform(min_atten, max_atten)

        fade_events.append(FadeEvent(
            start_time=start_time,
            duration=fade_duration,
            attenuation=attenuation
        ))

    # Sort by start time for easier debugging
    fade_events.sort(key=lambda f: f.start_time)

    return fade_events


def create_fade_mask(time_axis, fade_events: List[FadeEvent]):
    """
    Create a time-domain mask showing fade attenuation.

    🎓 TEACHING NOTE:
    A "mask" is an array that shows how much signal survives at each time.
    Useful for visualizing fades!

    Output:
    - 1.0 = no fade (full signal)
    - 0.5 = 50% fade
    - 0.0 = complete dropout

    Parameters
    ----------
    time_axis : np.ndarray
        Time values (seconds)
    fade_events : List[FadeEvent]
        Fades to include

    Returns
    -------
    mask : np.ndarray
        Attenuation factor at each time point
    """
    # Start with no fading (all 1.0)
    mask = np.ones_like(time_axis)

    # Apply each fade
    for i, t in enumerate(time_axis):
        for fade in fade_events:
            if fade.is_active_at(t):
                mask[i] *= fade.attenuation

    return mask


def estimate_fade_impact(fade_events: List[FadeEvent], total_duration):
    """
    Estimate how much communication is affected by fades.

    🎓 TEACHING NOTE:
    This calculates statistics about fading:
    - What percentage of time has fades?
    - What's the average signal loss?
    - How severe are the worst fades?

    Useful for understanding channel quality!

    Parameters
    ----------
    fade_events : List[FadeEvent]
        Fades to analyze
    total_duration : float
        Total time period (seconds)

    Returns
    -------
    stats : dict
        Statistics about fades
    """
    if total_duration <= 0:
        return {}

    # Calculate total faded time
    total_fade_time = sum(f.duration for f in fade_events)
    fade_percentage = (total_fade_time / total_duration) * 100

    # Find worst fade
    if fade_events:
        worst_fade = min(fade_events, key=lambda f: f.attenuation)
        avg_attenuation = np.mean([f.attenuation for f in fade_events])
    else:
        worst_fade = None
        avg_attenuation = 1.0

    return {
        'total_fades': len(fade_events),
        'total_fade_time_sec': total_fade_time,
        'fade_percentage': fade_percentage,
        'worst_attenuation': worst_fade.attenuation if worst_fade else 1.0,
        'average_attenuation': avg_attenuation
    }


# ═══ DEBUGGING NOTES ═══
#
# Common Issues:
#   1. Fades not visible? Check attenuation < 1.0
#   2. Signal completely gone? Attenuation might be too low
#   3. Overlapping fades? They multiply together (can be very severe)
#   4. Fade timing wrong? Check time_axis matches signal length
#
# Testing Tips:
#   - Plot signal before and after fades
#   - Use create_fade_mask() to visualize fade timeline
#   - Start with single fade event, then add more
#   - Check estimate_fade_impact() for statistics
#   - Test with various severities (shallow, deep, mixed)
#
# Gotchas:
#   - Multiple fades at same time MULTIPLY (0.5 × 0.5 = 0.25)
#   - Zero attenuation = complete signal loss
#   - Fade duration must match time units (seconds)
#   - Random fades differ each run (use random.seed() for repeatability)


# ═══ FUTURE IMPROVEMENTS ═══
#
# For Advanced Version (ORBITER-1):
#   [ ] Rayleigh fading model (statistical mobile fading)
#   [ ] Rician fading model (LOS + scattered components)
#   [ ] Frequency-selective fading (different freqs fade differently)
#   [ ] Doppler spread effects
#   [ ] Nakagami-m fading
#   [ ] Log-normal shadowing
#
# For Deep Space Version:
#   [ ] Ionospheric scintillation
#   [ ] Plasma irregularities
#   [ ] Solar corona effects
#   [ ] Interplanetary scintillation
