"""
═══════════════════════════════════════════════════════════════════
MODULE: signal/spectrograms.py
PURPOSE: Time-frequency analysis and visualization
THEME: Seeing how signal frequency content changes over time
═══════════════════════════════════════════════════════════════════

📡 STORY:
Sometimes we want to see not just the signal over TIME,
but also what FREQUENCIES are present and when.

A spectrogram is like a musical score - it shows:
  - Time on the x-axis (when)
  - Frequency on the y-axis (what pitch)
  - Color/brightness shows strength (how loud)

LEARNING GOALS:
  • Understanding frequency domain vs time domain
  • Visualizing modulation in frequency space
  • Seeing how signals occupy bandwidth
  • Intro to Fourier analysis concepts

SIMPLIFICATIONS:
  - Using matplotlib's built-in spectrogram
  - No windowing function explanations
  - Fixed time-frequency resolution

═══════════════════════════════════════════════════════════════════
"""

# ┌────────────────────────────────────────────────────────┐
# │              SPECTROGRAM VISUALIZATION                 │
# ├────────────────────────────────────────────────────────┤
# │                                                        │
# │              Frequency →                               │
# │                ▲                                       │
# │                │  🟦🟦🟨🟨🟧🟧🟥🟥                       │
# │            1000 Hz │  🟦🟨🟧🟥🟧🟨🟦🟦                   │
# │                │  🟦🟦🟦🟦🟦🟦🟦🟦                       │
# │              0 Hz │────────────────►                   │
# │                    Time (seconds)                      │
# │                                                        │
# │  Color = Signal strength at that frequency/time        │
# │  Bright = Strong, Dark = Weak                          │
# │                                                        │
# └────────────────────────────────────────────────────────┘

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab


def generate_spectrogram(signal, sample_rate_hz, title="Spectrogram"):
    """
    Generate and plot a spectrogram (time-frequency representation).

    🎓 TEACHING NOTE:
    A spectrogram shows how the frequency content of a signal
    changes over time. Think of it like sheet music for signals!

    How it works:
    1. Divide signal into short time windows
    2. Compute frequency spectrum for each window (FFT)
    3. Stack the spectra side-by-side to show time evolution

    WHY THIS MATTERS:
    - See modulation patterns visually
    - Identify interference or noise bursts
    - Understand bandwidth usage
    - Detect frequency changes over time

    Parameters
    ----------
    signal : ndarray
        Time-domain signal to analyze
    sample_rate_hz : int
        Sampling rate of the signal
    title : str
        Title for the plot

    Returns
    -------
    fig : matplotlib Figure
        Figure object containing the spectrogram
    ax : matplotlib Axes
        Axes object with the plot
    """
    # Create figure with good size
    fig, ax = plt.subplots(figsize=(10, 6))

    # Generate spectrogram using matplotlib's built-in function
    # 🎓 NFFT = number of points for FFT (affects frequency resolution)
    # noverlap = overlap between windows (affects time resolution)
    # More points = better frequency resolution but worse time resolution
    NFFT = 256  # Good balance for teaching
    noverlap = 128  # 50% overlap

    # Compute and plot spectrogram
    # 🎓 Returns:
    #   spectrum: 2D array of power values
    #   freqs: frequency bins
    #   t: time bins
    #   im: the image plotted
    spectrum, freqs, t, im = ax.specgram(
        signal,
        NFFT=NFFT,
        Fs=sample_rate_hz,
        noverlap=noverlap,
        cmap='viridis'  # Color map (purple-green-yellow)
    )

    # Add teaching-oriented labels
    ax.set_xlabel('Time (seconds)', fontsize=12)
    ax.set_ylabel('Frequency (Hz)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')

    # Add colorbar to show what colors mean
    # 🎓 Color indicates signal strength (power) at that time/frequency
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Power/Frequency (dB/Hz)', fontsize=10)

    plt.tight_layout()

    return fig, ax


def plot_frequency_spectrum(signal, sample_rate_hz, title="Frequency Spectrum"):
    """
    Plot the frequency spectrum of a signal (single-sided).

    🎓 TEACHING NOTE:
    This shows "what frequencies are present" in the signal.
    Unlike a spectrogram, this averages over all time.

    Useful for:
    - Seeing the carrier frequency
    - Checking signal bandwidth
    - Identifying noise components

    Parameters
    ----------
    signal : ndarray
        Time-domain signal
    sample_rate_hz : int
        Sampling rate
    title : str
        Plot title

    Returns
    -------
    fig, ax : matplotlib Figure and Axes
    freqs : ndarray
        Frequency values
    magnitude : ndarray
        Magnitude at each frequency
    """
    # Compute FFT (Fast Fourier Transform)
    # 🎓 FFT converts time-domain signal → frequency-domain
    N = len(signal)
    fft_output = np.fft.fft(signal)

    # Compute magnitude (we only care about strength, not phase)
    magnitude = np.abs(fft_output)

    # Compute frequency bins
    # 🎓 FFT output spans from 0 to sample_rate
    freqs = np.fft.fftfreq(N, 1/sample_rate_hz)

    # Take only positive frequencies (single-sided spectrum)
    # 🎓 Negative frequencies are mirror images for real signals
    positive_freqs = freqs[:N//2]
    positive_magnitude = magnitude[:N//2]

    # Normalize for better visualization
    positive_magnitude = positive_magnitude / N

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 4))

    # Plot as line (frequency spectrum)
    ax.plot(positive_freqs, positive_magnitude, linewidth=1.5, color='#E63946')

    # Add labels
    ax.set_xlabel('Frequency (Hz)', fontsize=12)
    ax.set_ylabel('Magnitude', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')

    plt.tight_layout()

    return fig, ax, positive_freqs, positive_magnitude


# ═══ DEBUGGING NOTES ═══
#
# Common Issues:
#   1. Spectrogram too dark? Signal might be very weak - check amplitude
#   2. Vertical lines everywhere? That's normal for abrupt signal changes
#   3. Frequency axis too large? Zoom into region of interest
#   4. Blurry in time? Increase NFFT for better frequency resolution
#
# Testing Tips:
#   - Test with sine wave → should see single horizontal line
#   - Test with chirp → should see diagonal line (frequency sweep)
#   - Test with BPSK → should see bandwidth around carrier
#   - Compare before/after modulation
#
# Gotchas:
#   - Time-frequency resolution trade-off (Heisenberg uncertainty!)
#   - Colormap choice affects perception
#   - FFT assumes periodic signals


# ═══ FUTURE IMPROVEMENTS ═══
#
# For Advanced Version (ORBITER-1):
#   [ ] Custom STFT implementation
#   [ ] Adjustable window functions
#   [ ] Waterfall displays
#   [ ] 3D spectrograms
