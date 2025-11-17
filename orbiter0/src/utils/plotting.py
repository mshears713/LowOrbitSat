"""
═══════════════════════════════════════════════════════════════════
MODULE: utils/plotting.py
PURPOSE: Standardized matplotlib visualization functions
THEME: Making signals visible - plots tell the story
═══════════════════════════════════════════════════════════════════

📡 STORY:
Visualizations are CRITICAL for learning wireless communications.
You need to SEE:
  • Waveforms in time domain
  • Spectra in frequency domain
  • Noise effects
  • Modulation patterns
  • Error patterns

This module provides consistent, teaching-oriented plotting
functions used throughout the system.

ALL PLOTS include:
  • Clear titles and labels
  • Grid lines for readability
  • Teaching annotations
  • Consistent styling
  • Colorblind-friendly colors

LEARNING GOALS:
  • Effective data visualization
  • Time vs frequency domain
  • Interpreting signal plots
  • Visual debugging techniques

═══════════════════════════════════════════════════════════════════
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
from typing import Optional, Tuple, List


# ═══════════════════════════════════════════════════════════════
# PLOTTING STYLE CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# Teaching-friendly color palette (colorblind-safe)
COLORS = {
    'signal': '#2E86AB',      # Blue - clean signal
    'noise': '#A23B72',       # Purple - noise
    'corrupted': '#F18F01',   # Orange - corrupted
    'corrected': '#06A77D',   # Green - corrected/success
    'error': '#C73E1D',       # Red - errors
    'reference': '#666666',   # Gray - reference lines
}

# Standard figure size
DEFAULT_FIGSIZE = (10, 4)
WIDE_FIGSIZE = (12, 4)
TALL_FIGSIZE = (8, 6)
LARGE_FIGSIZE = (12, 8)


def apply_teaching_style(ax):
    """
    Apply consistent teaching-oriented style to axes.

    🎓 TEACHING NOTE:
    This makes plots more readable for learners:
    - Grid for easier value reading
    - Thicker lines for visibility
    - Larger fonts for clarity
    - Spines only on left and bottom

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes to style
    """
    # Grid with low opacity
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.8)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Thicker axis lines
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)

    # Larger tick labels
    ax.tick_params(labelsize=10)


# ═══════════════════════════════════════════════════════════════
# TIME-DOMAIN PLOTTING
# ═══════════════════════════════════════════════════════════════

def plot_signal(
    time_axis: np.ndarray,
    signal: np.ndarray,
    title: str = "Signal",
    xlabel: str = "Time (seconds)",
    ylabel: str = "Amplitude",
    color: str = None,
    figsize: Tuple = DEFAULT_FIGSIZE,
    show_teaching_notes: bool = True
) -> Figure:
    """
    Plot a time-domain signal.

    🎓 TEACHING NOTE:
    Time-domain plots show how signal amplitude changes over time.
    This is the most fundamental view of any signal!

    Parameters
    ----------
    time_axis : np.ndarray
        Time values
    signal : np.ndarray
        Signal values
    title : str
        Plot title
    xlabel, ylabel : str
        Axis labels
    color : str, optional
        Line color (default: signal blue)
    figsize : tuple
        Figure size
    show_teaching_notes : bool
        Whether to add teaching annotations

    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure object
    """
    if color is None:
        color = COLORS['signal']

    fig, ax = plt.subplots(figsize=figsize)

    # Plot signal
    ax.plot(time_axis, signal, color=color, linewidth=2, label='Signal')

    # Labels
    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)

    # Teaching annotations
    if show_teaching_notes:
        # Mark peak amplitude
        max_idx = np.argmax(np.abs(signal))
        ax.plot(time_axis[max_idx], signal[max_idx], 'ro', markersize=8)
        ax.annotate(
            f'Peak: {signal[max_idx]:.3f}',
            xy=(time_axis[max_idx], signal[max_idx]),
            xytext=(10, 10),
            textcoords='offset points',
            fontsize=9,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7)
        )

    apply_teaching_style(ax)
    ax.legend(fontsize=10)
    plt.tight_layout()

    return fig


def plot_signal_comparison(
    time_axis: np.ndarray,
    signal1: np.ndarray,
    signal2: np.ndarray,
    label1: str = "Original",
    label2: str = "Modified",
    title: str = "Signal Comparison",
    figsize: Tuple = DEFAULT_FIGSIZE
) -> Figure:
    """
    Plot two signals for comparison.

    🎓 TEACHING NOTE:
    Comparing signals helps visualize the effects of:
    - Noise addition
    - Channel effects
    - Filtering

    Parameters
    ----------
    time_axis : np.ndarray
        Time values
    signal1, signal2 : np.ndarray
        Signals to compare
    label1, label2 : str
        Signal labels
    title : str
        Plot title
    figsize : tuple
        Figure size

    Returns
    -------
    fig : Figure
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Plot both signals
    ax.plot(time_axis, signal1, color=COLORS['signal'],
            linewidth=2, alpha=0.8, label=label1)
    ax.plot(time_axis, signal2, color=COLORS['corrupted'],
            linewidth=1.5, alpha=0.7, label=label2)

    # Zero line
    ax.axhline(y=0, color=COLORS['reference'], linestyle='--',
               linewidth=1, alpha=0.5)

    ax.set_xlabel("Time (seconds)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Amplitude", fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)

    apply_teaching_style(ax)
    ax.legend(fontsize=10, loc='best')
    plt.tight_layout()

    return fig


# ═══════════════════════════════════════════════════════════════
# FREQUENCY-DOMAIN PLOTTING
# ═══════════════════════════════════════════════════════════════

def plot_spectrum(
    signal: np.ndarray,
    sample_rate_hz: int,
    title: str = "Frequency Spectrum",
    figsize: Tuple = DEFAULT_FIGSIZE
) -> Figure:
    """
    Plot frequency spectrum using FFT.

    🎓 TEACHING NOTE:
    Frequency domain shows WHICH frequencies are present in a signal.
    - High peak at frequency F → signal contains F Hz component
    - Spread across frequencies → noise or complex signal

    Parameters
    ----------
    signal : np.ndarray
        Time-domain signal
    sample_rate_hz : int
        Sampling rate
    title : str
        Plot title
    figsize : tuple
        Figure size

    Returns
    -------
    fig : Figure
    """
    # Compute FFT
    n = len(signal)
    fft_vals = np.fft.fft(signal)
    fft_freqs = np.fft.fftfreq(n, 1/sample_rate_hz)

    # Only positive frequencies (spectrum is symmetric)
    pos_mask = fft_freqs >= 0
    freqs = fft_freqs[pos_mask]
    magnitude = np.abs(fft_vals[pos_mask]) / n

    fig, ax = plt.subplots(figsize=figsize)

    # Plot spectrum
    ax.plot(freqs, magnitude, color=COLORS['signal'], linewidth=2)

    # Mark dominant frequency
    dominant_idx = np.argmax(magnitude[1:]) + 1  # Skip DC component
    dominant_freq = freqs[dominant_idx]
    ax.plot(dominant_freq, magnitude[dominant_idx], 'ro', markersize=10)
    ax.annotate(
        f'Peak: {dominant_freq:.1f} Hz',
        xy=(dominant_freq, magnitude[dominant_idx]),
        xytext=(10, 10),
        textcoords='offset points',
        fontsize=9,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7)
    )

    ax.set_xlabel("Frequency (Hz)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Magnitude", fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)

    apply_teaching_style(ax)
    plt.tight_layout()

    return fig


# ═══════════════════════════════════════════════════════════════
# MODULATION VISUALIZATION
# ═══════════════════════════════════════════════════════════════

def plot_bpsk_constellation(
    symbols: np.ndarray,
    title: str = "BPSK Constellation Diagram",
    figsize: Tuple = (6, 6)
) -> Figure:
    """
    Plot BPSK constellation diagram.

    🎓 TEACHING NOTE:
    Constellation diagrams show symbol locations.
    For BPSK:
    - Clean signals → tight clusters at -1 and +1
    - Noisy signals → spread out clouds
    - Errors → symbols on wrong side of zero

    Parameters
    ----------
    symbols : np.ndarray
        BPSK symbols (+1 or -1)
    title : str
        Plot title
    figsize : tuple
        Figure size

    Returns
    -------
    fig : Figure
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Scatter plot of symbols
    ax.scatter(symbols, np.zeros_like(symbols), alpha=0.5,
               s=50, color=COLORS['signal'], edgecolors='black',
               linewidths=0.5)

    # Ideal symbol locations
    ax.axvline(x=-1, color=COLORS['corrected'], linestyle='--',
               linewidth=2, alpha=0.7, label='Ideal -1 (Bit 0)')
    ax.axvline(x=+1, color=COLORS['error'], linestyle='--',
               linewidth=2, alpha=0.7, label='Ideal +1 (Bit 1)')

    # Decision boundary
    ax.axvline(x=0, color='black', linestyle='-', linewidth=2,
               label='Decision Boundary')

    ax.set_xlabel("Symbol Value", fontsize=12, fontweight='bold')
    ax.set_ylabel("(Not used in BPSK)", fontsize=10, style='italic')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_ylim(-0.5, 0.5)
    ax.set_xlim(-2, 2)

    apply_teaching_style(ax)
    ax.legend(fontsize=10)
    plt.tight_layout()

    return fig


# ═══════════════════════════════════════════════════════════════
# ERROR VISUALIZATION
# ═══════════════════════════════════════════════════════════════

def plot_ber_vs_snr(
    snr_db_values: np.ndarray,
    ber_values: np.ndarray,
    title: str = "BER vs SNR",
    figsize: Tuple = DEFAULT_FIGSIZE,
    theoretical: bool = True
) -> Figure:
    """
    Plot Bit Error Rate vs Signal-to-Noise Ratio.

    🎓 TEACHING NOTE:
    This is the FUNDAMENTAL plot in communications!
    - Shows system performance
    - Higher SNR → Lower BER (better!)
    - Helps compare FEC schemes

    Parameters
    ----------
    snr_db_values : np.ndarray
        SNR values in dB
    ber_values : np.ndarray
        Corresponding BER values
    title : str
        Plot title
    figsize : tuple
        Figure size
    theoretical : bool
        Whether to plot theoretical BPSK curve

    Returns
    -------
    fig : Figure
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Plot measured BER
    ax.semilogy(snr_db_values, ber_values, 'o-',
                color=COLORS['signal'], linewidth=2,
                markersize=8, label='Measured')

    # Theoretical BPSK curve (if requested)
    if theoretical:
        from scipy.special import erfc
        snr_linear = 10**(snr_db_values / 10)
        theoretical_ber = 0.5 * erfc(np.sqrt(snr_linear))
        ax.semilogy(snr_db_values, theoretical_ber, '--',
                    color=COLORS['reference'], linewidth=2,
                    label='Theoretical BPSK')

    ax.set_xlabel("SNR (dB)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Bit Error Rate (BER)", fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)

    # Teaching annotation
    ax.text(0.05, 0.95,
            '📚 Lower BER = Better!\n   Higher SNR = Better!',
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

    apply_teaching_style(ax)
    ax.legend(fontsize=10)
    plt.tight_layout()

    return fig


def plot_bit_errors(
    original_bits: List[int],
    received_bits: List[int],
    title: str = "Bit Error Pattern",
    max_bits: int = 100,
    figsize: Tuple = WIDE_FIGSIZE
) -> Figure:
    """
    Visualize bit errors in transmission.

    🎓 TEACHING NOTE:
    Shows EXACTLY where errors occurred:
    - Green = correct bit
    - Red = error
    - Helps identify error patterns (random vs bursts)

    Parameters
    ----------
    original_bits : list
        Original transmitted bits
    received_bits : list
        Received bits (may have errors)
    title : str
        Plot title
    max_bits : int
        Maximum bits to display
    figsize : tuple
        Figure size

    Returns
    -------
    fig : Figure
    """
    # Limit to max_bits for readability
    orig = np.array(original_bits[:max_bits])
    recv = np.array(received_bits[:max_bits])

    # Identify errors
    errors = (orig != recv)

    fig, ax = plt.subplots(figsize=figsize)

    # Plot original bits
    ax.scatter(np.arange(len(orig))[~errors], orig[~errors],
               color=COLORS['corrected'], s=100, marker='o',
               label='Correct', alpha=0.7, edgecolors='black')

    # Plot errors
    if np.any(errors):
        ax.scatter(np.arange(len(orig))[errors], recv[errors],
                   color=COLORS['error'], s=150, marker='X',
                   label='Errors', edgecolors='black', linewidths=2)

    ax.set_xlabel("Bit Index", fontsize=12, fontweight='bold')
    ax.set_ylabel("Bit Value (0 or 1)", fontsize=12, fontweight='bold')
    ax.set_title(f"{title} ({np.sum(errors)}/{len(orig)} errors)",
                 fontsize=14, fontweight='bold', pad=15)
    ax.set_yticks([0, 1])
    ax.set_ylim(-0.5, 1.5)

    apply_teaching_style(ax)
    ax.legend(fontsize=10)
    plt.tight_layout()

    return fig


# ═══════════════════════════════════════════════════════════════
# SATELLITE PASS VISUALIZATION
# ═══════════════════════════════════════════════════════════════

def plot_satellite_pass_timeline(
    times: np.ndarray,
    elevations: np.ndarray,
    snrs: Optional[np.ndarray] = None,
    bers: Optional[np.ndarray] = None,
    title: str = "Satellite Pass Timeline",
    figsize: Tuple = LARGE_FIGSIZE
) -> Figure:
    """
    Plot satellite pass with elevation, SNR, and BER over time.

    🎓 TEACHING NOTE:
    Shows how signal quality changes as satellite moves:
    - Elevation: satellite height in sky
    - SNR: signal quality (higher = better)
    - BER: error rate (lower = better)

    Watch how they correlate!

    Parameters
    ----------
    times : np.ndarray
        Time points
    elevations : np.ndarray
        Elevation angles (degrees)
    snrs : np.ndarray, optional
        SNR values (dB)
    bers : np.ndarray, optional
        BER values
    title : str
        Plot title
    figsize : tuple
        Figure size

    Returns
    -------
    fig : Figure
    """
    # Determine number of subplots
    num_plots = 1 + (snrs is not None) + (bers is not None)

    fig, axes = plt.subplots(num_plots, 1, figsize=figsize, sharex=True)

    if num_plots == 1:
        axes = [axes]

    plot_idx = 0

    # Plot elevation
    axes[plot_idx].plot(times, elevations, color=COLORS['signal'],
                        linewidth=3, label='Elevation')
    axes[plot_idx].fill_between(times, 0, elevations,
                                 color=COLORS['signal'], alpha=0.2)
    axes[plot_idx].set_ylabel("Elevation (°)", fontsize=12, fontweight='bold')
    axes[plot_idx].set_title(title, fontsize=14, fontweight='bold', pad=15)
    apply_teaching_style(axes[plot_idx])
    axes[plot_idx].legend()
    plot_idx += 1

    # Plot SNR if provided
    if snrs is not None:
        axes[plot_idx].plot(times, snrs, color=COLORS['corrected'],
                            linewidth=2.5, label='SNR')
        axes[plot_idx].axhline(y=10, color=COLORS['reference'],
                               linestyle='--', label='Target SNR')
        axes[plot_idx].set_ylabel("SNR (dB)", fontsize=12, fontweight='bold')
        apply_teaching_style(axes[plot_idx])
        axes[plot_idx].legend()
        plot_idx += 1

    # Plot BER if provided
    if bers is not None:
        axes[plot_idx].semilogy(times, bers, color=COLORS['error'],
                                linewidth=2.5, label='BER')
        axes[plot_idx].set_ylabel("Bit Error Rate", fontsize=12, fontweight='bold')
        apply_teaching_style(axes[plot_idx])
        axes[plot_idx].legend()

    axes[-1].set_xlabel("Time (seconds)", fontsize=12, fontweight='bold')

    plt.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# PACKET VISUALIZATION
# ═══════════════════════════════════════════════════════════════

def plot_packet_structure(
    packet_bytes: bytes,
    title: str = "Packet Structure",
    figsize: Tuple = WIDE_FIGSIZE
) -> Figure:
    """
    Visualize packet structure with color-coded sections.

    🎓 TEACHING NOTE:
    Shows how data is organized in a packet:
    - Preamble (sync)
    - Header (metadata)
    - Payload (actual data)
    - CRC (checksum)

    Parameters
    ----------
    packet_bytes : bytes
        Packet data
    title : str
        Plot title
    figsize : tuple
        Figure size

    Returns
    -------
    fig : Figure
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Packet structure (from packetizer.py)
    preamble_len = 4
    header_len = 8
    crc_len = 2
    payload_len = len(packet_bytes) - preamble_len - header_len - crc_len

    sections = [
        ('Preamble', preamble_len, COLORS['signal']),
        ('Header', header_len, COLORS['corrected']),
        ('Payload', payload_len, COLORS['corrupted']),
        ('CRC', crc_len, COLORS['error'])
    ]

    x_pos = 0
    for name, length, color in sections:
        rect = mpatches.Rectangle((x_pos, 0), length, 1,
                                   facecolor=color, edgecolor='black',
                                   linewidth=2, alpha=0.7)
        ax.add_patch(rect)

        # Label
        ax.text(x_pos + length/2, 0.5, f"{name}\n{length}B",
                ha='center', va='center', fontsize=10, fontweight='bold')

        x_pos += length

    ax.set_xlim(0, len(packet_bytes))
    ax.set_ylim(0, 1)
    ax.set_xlabel("Byte Position", fontsize=12, fontweight='bold')
    ax.set_yticks([])
    ax.set_title(f"{title} ({len(packet_bytes)} bytes total)",
                 fontsize=14, fontweight='bold', pad=15)

    apply_teaching_style(ax)
    plt.tight_layout()

    return fig


# ═══════════════════════════════════════════════════════════════
# DEBUGGING NOTES
# ═══════════════════════════════════════════════════════════════
#
# Common Issues:
#   1. Plots look cluttered → Reduce max_bits or use larger figsize
#   2. Text overlaps → Adjust annotation positions
#   3. Colors hard to distinguish → Use COLORS dictionary
#   4. Plots not showing in Streamlit → Use st.pyplot(fig)
#
# Testing Tips:
#   - Test with different signal lengths
#   - Verify all plots have titles and labels
#   - Check colorblind friendliness
#   - Test with extreme values (very high/low SNR)
#
# ═══════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════
# FUTURE IMPROVEMENTS
# ═══════════════════════════════════════════════════════════════
#
# For ORBITER-1:
#   [ ] Interactive plots with plotly
#   [ ] 3D satellite trajectory visualization
#   [ ] Animated signal propagation
#   [ ] Waterfall spectrograms
#   [ ] Constellation diagram animations
#   [ ] Real-time updating plots
#   [ ] Export plots to PDF/PNG
#   [ ] Custom themes (dark mode, etc.)
#
# ═══════════════════════════════════════════════════════════════
