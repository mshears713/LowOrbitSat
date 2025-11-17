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

import numpy as np


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
    # Convert text to bytes using UTF-8 encoding
    # 🎓 UTF-8 is the standard text encoding (supports all languages!)
    text_bytes = text.encode('utf-8')

    # Convert each byte to 8 bits
    bits = []
    for byte in text_bytes:
        # Convert byte to binary string, e.g., 72 → '01001000'
        # Format: {:08b} means "8 digits, binary, zero-padded"
        byte_bits = format(byte, '08b')

        # Convert each character '0' or '1' to integer 0 or 1
        for bit_char in byte_bits:
            bits.append(int(bit_char))

    return bits


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
    # Check that bits length is multiple of 8
    # 🎓 Each character is 8 bits (1 byte)
    if len(bits) % 8 != 0:
        # Pad with zeros if needed (or could raise error)
        bits = bits + [0] * (8 - len(bits) % 8)

    # Group bits into bytes
    bytes_list = []
    for i in range(0, len(bits), 8):
        # Get 8 bits
        byte_bits = bits[i:i+8]

        # Convert bit list to string like '01001000'
        bit_string = ''.join(str(b) for b in byte_bits)

        # Convert binary string to integer
        byte_value = int(bit_string, 2)

        bytes_list.append(byte_value)

    # Convert bytes to text
    # 🎓 Handle errors gracefully - replace invalid bytes with �
    try:
        text = bytes(bytes_list).decode('utf-8', errors='replace')
    except Exception:
        text = "<?>"  # Fallback for corrupted data

    return text


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
    # Convert bits to numpy array for vectorized operations
    bits_array = np.array(bits)

    # BPSK mapping: 0 → -1, 1 → +1
    # 🎓 Math trick: symbol = 2 * bit - 1
    #   When bit = 0: 2*0 - 1 = -1
    #   When bit = 1: 2*1 - 1 = +1
    symbols = 2 * bits_array - 1

    return symbols


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
    # Decision rule: Check sign of each symbol
    # 🎓 Simple threshold detector at zero
    #   symbol > 0 → bit 1
    #   symbol ≤ 0 → bit 0

    bits = []
    for symbol in symbols:
        if symbol > 0:
            bits.append(1)
        else:
            bits.append(0)

    # Alternative vectorized version (commented out for teaching clarity):
    # bits = (symbols > 0).astype(int).tolist()

    return bits


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
    time_axis : ndarray
        Time values for the signal
    """
    # Determine how many samples per symbol
    # 🎓 More samples = smoother wave, but more data
    # We'll use at least 10 samples per carrier cycle for smooth visualization
    samples_per_symbol = max(100, int(sample_rate_hz / carrier_freq_hz) * 10)

    # Calculate total duration
    num_symbols = len(symbols)
    duration_sec = num_symbols * samples_per_symbol / sample_rate_hz

    # Create time axis
    num_samples = num_symbols * samples_per_symbol
    time_axis = np.linspace(0, duration_sec, num_samples)

    # Create carrier wave
    # 🎓 Carrier is just a sine wave at the specified frequency
    angular_freq = 2 * np.pi * carrier_freq_hz
    carrier = np.sin(angular_freq * time_axis)

    # Upsample symbols to match carrier length
    # 🎓 Each symbol needs to be repeated for samples_per_symbol samples
    symbols_upsampled = np.repeat(symbols, samples_per_symbol)

    # Modulate: multiply carrier by symbols
    # 🎓 Symbol +1 → normal carrier
    #    Symbol -1 → inverted carrier (180° phase shift)
    signal = symbols_upsampled * carrier

    return signal, time_axis


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
    # Calculate samples per symbol
    samples_per_symbol = len(signal) // symbols_count
    if samples_per_symbol < 1:
        samples_per_symbol = 1

    # Create carrier for demodulation
    # 🎓 We need the same carrier to "unmix" the signal
    time_axis = np.linspace(0, len(signal) / sample_rate_hz, len(signal))
    angular_freq = 2 * np.pi * carrier_freq_hz
    carrier = np.sin(angular_freq * time_axis)

    # Demodulate: multiply by carrier
    # 🎓 This shifts the signal back to baseband
    demod_signal = signal * carrier

    # Integrate over each symbol period to recover symbols
    # 🎓 Integration helps reduce noise effects
    symbols = []
    for i in range(symbols_count):
        start_idx = i * samples_per_symbol
        end_idx = start_idx + samples_per_symbol

        # Sum (integrate) over the symbol period
        if end_idx <= len(demod_signal):
            symbol_sum = np.sum(demod_signal[start_idx:end_idx])
        else:
            symbol_sum = np.sum(demod_signal[start_idx:])

        # The sign of the sum tells us the symbol
        # 🎓 Positive sum → +1 symbol, Negative sum → -1 symbol
        if symbol_sum > 0:
            symbols.append(1)
        else:
            symbols.append(-1)

    return np.array(symbols)


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
