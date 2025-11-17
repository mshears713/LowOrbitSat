"""
═══════════════════════════════════════════════════════════════════
MODULE: signal/modulation.py
PURPOSE: BPSK modulation and demodulation for beginners
THEME: Encoding bits into signals and back again
═══════════════════════════════════════════════════════════════════

📡 STORY:
Our satellite needs to send BITS (0s and 1s) through space.
But space only understands WAVES (electromagnetic radiation).

We need a way to convert bits → waves (modulation)
And waves → bits (demodulation)

This module implements BPSK (Binary Phase Shift Keying):
  - Bit 0 → Symbol -1 → Wave with 180° phase
  - Bit 1 → Symbol +1 → Wave with 0° phase

LEARNING GOALS:
  • What modulation is and why we need it
  • How BPSK encodes one bit per symbol
  • How to convert text → bits → symbols → signal
  • How noise affects symbol detection
  • How to demodulate (decode) a signal back to bits

SIMPLIFICATIONS:
  - Only BPSK (simplest modulation)
  - No carrier recovery or synchronization
  - Perfect symbol timing
  - Ignoring I/Q representation for now

═══════════════════════════════════════════════════════════════════
"""

# ┌────────────────────────────────────────────────────────┐
# │              BPSK MODULATION PIPELINE                  │
# ├────────────────────────────────────────────────────────┤
# │                                                        │
# │  Text ──► Bits ──► Symbols ──► Signal                 │
# │  "Hi"     [0,1]    [-1,+1]      waveform              │
# │                                                        │
# │  Mapping:                                              │
# │    Bit 0  →  Symbol -1  →  Phase 180°                 │
# │    Bit 1  →  Symbol +1  →  Phase 0°                   │
# │                                                        │
# └────────────────────────────────────────────────────────┘

# ┌────────────────────────────────────────────────────────┐
# │              BPSK DEMODULATION PIPELINE                │
# ├────────────────────────────────────────────────────────┤
# │                                                        │
# │  Noisy Signal ──► Symbols ──► Bits ──► Text           │
# │  waveform         [-1,+1]     [0,1]     "Hi"          │
# │                                                        │
# │  Detection:                                            │
# │    Sample > 0  →  Symbol +1  →  Bit 1                 │
# │    Sample < 0  →  Symbol -1  →  Bit 0                 │
# │    (Errors happen when noise flips the sign!)         │
# │                                                        │
# └────────────────────────────────────────────────────────┘


def text_to_bits(text):
    """
    Convert text string to list of bits.

    🎓 TEACHING NOTE:
    Computers store text as numbers (ASCII/UTF-8).
    Each character is a byte (8 bits).

    Example:
      'H' → ASCII 72 → Binary 01001000 → [0,1,0,0,1,0,0,0]

    Parameters
    ----------
    text : str
        Message to convert

    Returns
    -------
    bits : list of int
        List of 0s and 1s
    """
    # Implementation coming in Phase 2
    pass


def bits_to_text(bits):
    """
    Convert list of bits back to text string.

    🎓 TEACHING NOTE:
    Reverse of text_to_bits().
    Groups bits into bytes, then decodes to characters.

    Parameters
    ----------
    bits : list of int
        List of 0s and 1s (must be multiple of 8)

    Returns
    -------
    text : str
        Decoded message
    """
    # Implementation coming in Phase 2
    pass


def bits_to_bpsk_symbols(bits):
    """
    Convert bits to BPSK symbols.

    🎓 TEACHING NOTE:
    BPSK mapping is simple:
      0 → -1
      1 → +1

    These symbols will be multiplied by the carrier wave.

    Parameters
    ----------
    bits : list of int
        List of 0s and 1s

    Returns
    -------
    symbols : ndarray
        Array of -1s and +1s
    """
    # Implementation coming in Phase 2
    pass


def bpsk_symbols_to_bits(symbols):
    """
    Convert BPSK symbols back to bits (demodulation).

    🎓 TEACHING NOTE:
    Decision rule:
      If symbol > 0 → bit 1
      If symbol < 0 → bit 0
      If symbol == 0 → guess (coin flip)

    NOISE CAUSES ERRORS:
    If noise is strong enough, it can flip the sign,
    causing a bit error!

    Parameters
    ----------
    symbols : ndarray
        Array of numbers (ideally close to -1 or +1)

    Returns
    -------
    bits : list of int
        Decoded bits
    """
    # Implementation coming in Phase 2
    pass


def modulate_bpsk(symbols, carrier_freq_hz, sample_rate_hz):
    """
    Modulate BPSK symbols onto a carrier wave.

    🎓 TEACHING NOTE:
    We multiply our symbols by a sine wave (carrier).
    Symbol +1 → normal sine
    Symbol -1 → inverted sine (180° phase shift)

    This creates the actual signal that travels through space.

    Parameters
    ----------
    symbols : ndarray
        BPSK symbols (-1 or +1)
    carrier_freq_hz : float
        Frequency of carrier wave
    sample_rate_hz : int
        Sampling rate

    Returns
    -------
    signal : ndarray
        Modulated waveform
    """
    # Implementation coming in Phase 2
    pass


def demodulate_bpsk(signal, carrier_freq_hz, sample_rate_hz, symbols_count):
    """
    Demodulate BPSK signal back to symbols.

    🎓 TEACHING NOTE:
    Simplified demodulation:
    1. Multiply signal by carrier (removes carrier)
    2. Integrate (sum) over each symbol period
    3. Check sign to recover symbol

    Real systems use matched filters, but this works for teaching!

    Parameters
    ----------
    signal : ndarray
        Received signal (noisy)
    carrier_freq_hz : float
        Known carrier frequency
    sample_rate_hz : int
        Sampling rate
    symbols_count : int
        How many symbols to expect

    Returns
    -------
    symbols : ndarray
        Recovered symbols (may have errors due to noise)
    """
    # Implementation coming in Phase 2
    pass


# ═══ DEBUGGING NOTES ═══
#
# Common Issues:
#   1. Getting gibberish text? Check bit alignment (must be multiple of 8)
#   2. All bits wrong? Carrier frequency might be inverted
#   3. Random errors? That's normal with noise! Check SNR
#
# Testing Tips:
#   - Start with no noise to verify modulation works
#   - Test with simple messages like "Hi" or "Test"
#   - Plot symbols to see +1/-1 pattern clearly
#   - Count bit errors vs expected (BER calculation)
#
# Gotchas:
#   - Symbol timing must be exact (samples per symbol)
#   - Carrier frequency must match exactly for demodulation
#   - Phase offset can invert all bits (not handled in basic version)


# ═══ FUTURE IMPROVEMENTS ═══
#
# For Advanced Version (ORBITER-1):
#   [ ] Add QPSK modulation (2 bits per symbol)
#   [ ] Implement carrier recovery (PLL)
#   [ ] Add symbol timing recovery
#   [ ] Support I/Q constellation diagrams
#   [ ] Add soft-decision decoding
#   [ ] Implement matched filtering
#
# For Deep Space Version:
#   [ ] Higher-order modulation (8PSK, 16QAM)
#   [ ] Coherent vs non-coherent detection
#   [ ] Doppler compensation
