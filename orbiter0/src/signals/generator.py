"""
═══════════════════════════════════════════════════════════════════
MODULE: signal/generator.py
PURPOSE: Generate beginner-friendly waveforms for satellite downlink
THEME: Teaching how signals are born before they travel to Earth
═══════════════════════════════════════════════════════════════════

📡 STORY:
Before a satellite can talk to Earth, it needs to create a SIGNAL.
Think of signals as waves of energy rippling through space.

This module generates the simplest possible waveforms:
  - Sine waves (smooth and predictable)
  - Square waves (abrupt and digital-like)
  - BPSK modulated signals (bits encoded as phase flips)

LEARNING GOALS:
  • What a signal is (samples over time)
  • How frequency and amplitude work
  • How to visualize waveforms
  • Intro to digital vs analog signals

SIMPLIFICATIONS:
  - No complex propagation physics
  - Time is discrete (sampled)
  - Perfect signal generation (no hardware noise)

═══════════════════════════════════════════════════════════════════
"""

# ┌─────────────────────────────────────────────────┐
# │          SIGNAL GENERATION PIPELINE            │
# ├─────────────────────────────────────────────────┤
# │                                                 │
# │  Frequency   ──┐                               │
# │  Amplitude   ──┤─► Generator ─► Samples Array  │
# │  Duration    ──┘                               │
# │                                                 │
# │  Output: numpy array of time-domain samples    │
# └─────────────────────────────────────────────────┘

import numpy as np
import matplotlib.pyplot as plt


def generate_sine(frequency_hz, amplitude, duration_sec, sample_rate_hz):
    """
    Generate a pure sine wave.

    🎓 TEACHING NOTE:
    A sine wave is the most fundamental signal in nature.
    It's what you get when something oscillates smoothly.

    Formula: amplitude * sin(2π * frequency * time)

    WHY THIS MATTERS:
    Real satellite signals aren't pure sines, but understanding
    them is the foundation for understanding everything else.

    Parameters
    ----------
    frequency_hz : float
        How many cycles per second (e.g., 1000 Hz = 1000 cycles/sec)
    amplitude : float
        Peak signal strength (how "tall" the wave is)
    duration_sec : float
        How long to generate the signal for
    sample_rate_hz : int
        How many samples to take per second (must be ≥ 2× frequency)

    Returns
    -------
    time_axis : ndarray
        Array of time values (x-axis for plotting)
    signal : ndarray
        Array of signal values (y-axis for plotting)
    """
    # Create time axis (this is where our signal lives)
    # 🎓 We need enough samples to capture the signal accurately
    num_samples = int(duration_sec * sample_rate_hz)
    time_axis = np.linspace(0, duration_sec, num_samples)

    # Generate the wave (magic happens here!)
    # 🎓 2π converts frequency from cycles/sec to radians/sec
    # Radians are the natural unit for trigonometric functions
    angular_freq = 2 * np.pi * frequency_hz
    signal = amplitude * np.sin(angular_freq * time_axis)

    return time_axis, signal


def generate_square(frequency_hz, amplitude, duration_sec, sample_rate_hz):
    """
    Generate a square wave (digital-like signal).

    🎓 TEACHING NOTE:
    Square waves are closer to how digital systems work.
    They're either "high" or "low" with instant transitions.

    WHY THIS MATTERS:
    Digital data (like bits) is often represented as square waves
    in real hardware.

    Parameters
    ----------
    Same as generate_sine()

    Returns
    -------
    time_axis, signal : ndarrays
    """
    # Create time axis
    num_samples = int(duration_sec * sample_rate_hz)
    time_axis = np.linspace(0, duration_sec, num_samples)

    # Generate square wave using the sign of a sine wave
    # 🎓 A square wave is just a sine wave where we keep only the sign:
    #    - Positive part becomes +amplitude
    #    - Negative part becomes -amplitude
    angular_freq = 2 * np.pi * frequency_hz
    sine_wave = np.sin(angular_freq * time_axis)

    # np.sign() converts positive values to +1, negative to -1
    # Then we scale by amplitude
    signal = amplitude * np.sign(sine_wave)

    # 🎓 EDGE CASE: np.sign(0) = 0, but we want a clean square wave
    # Set zeros to +amplitude (convention: start high)
    signal[signal == 0] = amplitude

    return time_axis, signal


def plot_signal(time_axis, signal, title="Signal", xlabel="Time (seconds)", ylabel="Amplitude"):
    """
    Plot a signal in the time domain with teaching-oriented labels.

    🎓 TEACHING NOTE:
    Visualizing signals is crucial to understanding them!
    This helper function creates clear, labeled plots.

    Parameters
    ----------
    time_axis : ndarray
        Time values (x-axis)
    signal : ndarray
        Signal values (y-axis)
    title : str
        Plot title
    xlabel : str
        X-axis label
    ylabel : str
        Y-axis label

    Returns
    -------
    fig, ax : matplotlib Figure and Axes objects
    """
    # Create figure with good size for visibility
    fig, ax = plt.subplots(figsize=(10, 4))

    # Plot the signal with a clear, visible line
    ax.plot(time_axis, signal, linewidth=2, color='#2E86AB')

    # Add labels and title (teaching-oriented)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')

    # Add grid for easier reading
    ax.grid(True, alpha=0.3, linestyle='--')

    # Make plot tight and clean
    plt.tight_layout()

    return fig, ax


# ═══ DEBUGGING NOTES ═══
#
# Common Issues:
#   1. Signal all zeros? Check that amplitude > 0
#   2. Signal looks choppy? Increase sample_rate_hz
#   3. Wrong frequency? Verify units (Hz not MHz)
#
# Testing Tips:
#   - Plot first 100 samples to verify shape
#   - Check signal.max() == amplitude
#   - Count zero crossings to verify frequency
#
# Gotchas:
#   - NumPy uses radians, not degrees
#   - Sample rate must be ≥ 2× highest frequency (Nyquist theorem)


# ═══ FUTURE IMPROVEMENTS ═══
#
# For Advanced Version (ORBITER-1):
#   [ ] Add chirp signals (frequency sweeping)
#   [ ] Support I/Q complex signals
#   [ ] Add realistic carrier frequencies
#   [ ] Implement bandlimited signals
#   [ ] Add pulse shaping filters
#   [ ] Support multi-carrier signals
#
# For Deep Space Version:
#   [ ] Doppler shift simulation
#   [ ] Extremely low SNR scenarios
#   [ ] Long propagation delays
