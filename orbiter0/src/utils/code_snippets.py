"""
═══════════════════════════════════════════════════════════════════
MODULE: utils/code_snippets.py
PURPOSE: Reusable code snippets for teaching overlays in Streamlit
THEME: Show learners the code behind the magic
═══════════════════════════════════════════════════════════════════

📡 STORY:
Teaching-oriented projects should show HOW things work, not just
WHAT they do!

This module provides formatted code snippets that can be displayed
in Streamlit expanders to show students the actual implementation
behind each demo.

Each snippet includes:
  • The actual working code
  • Inline comments explaining each step
  • Teaching notes about why we do it this way
  • References to relevant concepts

LEARNING GOALS:
  • Transparency in how simulations work
  • Understanding implementation choices
  • Learning by example
  • Building confidence to modify code

═══════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════
# SIGNAL GENERATION SNIPPETS
# ═══════════════════════════════════════════════════════════════

SNIPPET_GENERATE_SINE = '''
def generate_sine(frequency_hz, amplitude, duration_sec, sample_rate_hz):
    """
    Generate a pure sine wave.

    🎓 TEACHING NOTE:
    A sine wave is the fundamental building block of all signals!
    Formula: y(t) = A * sin(2π * f * t)

    Where:
      A = amplitude (how tall the wave is)
      f = frequency (how fast it oscillates)
      t = time (when we sample it)
    """
    # Calculate how many samples we need
    # e.g., 1 second at 1000 Hz = 1000 samples
    num_samples = int(duration_sec * sample_rate_hz)

    # Create time axis: [0, 0.001, 0.002, ..., duration_sec]
    time_axis = np.linspace(0, duration_sec, num_samples)

    # Generate the sine wave
    # 2π converts frequency from Hz to radians/second
    angular_freq = 2 * np.pi * frequency_hz
    signal = amplitude * np.sin(angular_freq * time_axis)

    return time_axis, signal
'''

SNIPPET_ADD_NOISE = '''
def add_awgn(signal, snr_db):
    """
    Add Additive White Gaussian Noise (AWGN) to a signal.

    🎓 TEACHING NOTE:
    Real channels always have noise! This simulates it.

    "White" = all frequencies equally
    "Gaussian" = bell-curve distribution
    "Additive" = just add it to the signal
    """
    # Calculate signal power (average of squared values)
    signal_power = np.mean(signal ** 2)

    # Convert SNR from dB to linear scale
    # SNR_dB = 10 * log10(signal_power / noise_power)
    # Therefore: noise_power = signal_power / (10^(SNR_dB/10))
    snr_linear = 10 ** (snr_db / 10)
    noise_power = signal_power / snr_linear

    # Generate Gaussian noise with calculated power
    # np.random.normal(mean, std_dev, size)
    noise = np.random.normal(0, np.sqrt(noise_power), len(signal))

    # Add noise to signal
    noisy_signal = signal + noise

    return noisy_signal
'''

# ═══════════════════════════════════════════════════════════════
# MODULATION SNIPPETS
# ═══════════════════════════════════════════════════════════════

SNIPPET_TEXT_TO_BITS = '''
def text_to_bits(text):
    """
    Convert text to binary bits.

    🎓 TEACHING NOTE:
    Computers store text as numbers (UTF-8 encoding).
    Each character becomes 8 bits (1 byte).

    Example: "H" → ASCII 72 → 01001000
    """
    # Encode text to bytes using UTF-8
    text_bytes = text.encode('utf-8')

    # Convert each byte to 8 bits
    bits = []
    for byte in text_bytes:
        # Format as 8-digit binary: {:08b}
        byte_bits = format(byte, '08b')

        # Convert each '0'/'1' character to integer
        for bit_char in byte_bits:
            bits.append(int(bit_char))

    return bits
'''

SNIPPET_BPSK_MODULATION = '''
def bits_to_bpsk_symbols(bits):
    """
    Convert bits to BPSK symbols.

    🎓 TEACHING NOTE:
    BPSK (Binary Phase Shift Keying) maps:
      Bit 0 → Symbol -1 (phase = 180°)
      Bit 1 → Symbol +1 (phase = 0°)

    This is the simplest form of digital modulation!
    """
    # Map: 0→-1, 1→+1
    symbols = [2*bit - 1 for bit in bits]
    # Equivalent to: symbols = [-1 if bit==0 else +1 for bit in bits]

    return np.array(symbols, dtype=float)
'''

SNIPPET_BPSK_DEMODULATION = '''
def demodulate_bpsk(signal, carrier_freq_hz, sample_rate_hz, samples_per_symbol):
    """
    Demodulate BPSK signal back to symbols.

    🎓 TEACHING NOTE:
    Demodulation reverses modulation:
      1. Multiply by carrier (mixing)
      2. Integrate over symbol period
      3. Check sign: positive→+1, negative→-1

    Errors happen when noise flips the sign!
    """
    # Generate carrier wave (same as transmitter)
    num_samples = len(signal)
    time_axis = np.arange(num_samples) / sample_rate_hz
    carrier = np.cos(2 * np.pi * carrier_freq_hz * time_axis)

    # Mix signal with carrier (coherent detection)
    mixed = signal * carrier

    # Integrate over each symbol period
    num_symbols = len(mixed) // samples_per_symbol
    symbols = []

    for i in range(num_symbols):
        start = i * samples_per_symbol
        end = start + samples_per_symbol
        # Sum over symbol period (integration)
        symbol_value = np.sum(mixed[start:end])
        symbols.append(symbol_value)

    return np.array(symbols)
'''

# ═══════════════════════════════════════════════════════════════
# ERROR CORRECTION SNIPPETS
# ═══════════════════════════════════════════════════════════════

SNIPPET_CRC_CHECKSUM = '''
def compute_crc16(data_bytes):
    """
    Compute CRC-16 checksum for error detection.

    🎓 TEACHING NOTE:
    CRC (Cyclic Redundancy Check) is like a fingerprint for data.
    If even ONE bit changes, the CRC will be different!

    It can DETECT errors but not CORRECT them.
    """
    # CRC-16-CCITT polynomial: x^16 + x^12 + x^5 + 1
    polynomial = 0x1021  # Binary: 10001000000100001
    crc = 0xFFFF  # Initial value

    for byte in data_bytes:
        # XOR byte into CRC
        crc ^= (byte << 8)

        # Process each bit
        for _ in range(8):
            if crc & 0x8000:  # If leftmost bit is 1
                crc = (crc << 1) ^ polynomial
            else:
                crc = crc << 1
            crc &= 0xFFFF  # Keep only 16 bits

    return crc
'''

SNIPPET_HAMMING_ENCODE = '''
def hamming_encode_block(data_bits):
    """
    Encode 4 data bits into 7-bit Hamming code.

    🎓 TEACHING NOTE:
    Hamming(7,4) adds 3 parity bits to 4 data bits.
    This allows correcting 1-bit errors!

    Positions:  1  2  3  4  5  6  7
    Type:       P  P  D  P  D  D  D

    P = parity bit (calculated)
    D = data bit (your data)
    """
    if len(data_bits) != 4:
        raise ValueError("Hamming(7,4) requires exactly 4 data bits")

    d1, d2, d3, d4 = data_bits

    # Calculate parity bits
    # p1 covers positions 1,3,5,7
    p1 = d1 ^ d2 ^ d4

    # p2 covers positions 2,3,6,7
    p2 = d1 ^ d3 ^ d4

    # p4 covers positions 4,5,6,7
    p4 = d2 ^ d3 ^ d4

    # Arrange: P P D P D D D
    #          1 2 3 4 5 6 7
    encoded = [p1, p2, d1, p4, d2, d3, d4]

    return encoded
'''

# ═══════════════════════════════════════════════════════════════
# CHANNEL EFFECTS SNIPPETS
# ═══════════════════════════════════════════════════════════════

SNIPPET_RANGE_LOSS = '''
def apply_free_space_loss(signal, distance_km, frequency_hz):
    """
    Apply free-space path loss (signal weakens with distance).

    🎓 TEACHING NOTE:
    Signals spread out as they travel, like ripples on a pond.

    Power decreases as 1/distance²
    This is the "inverse square law" from physics!

    Real formula (simplified):
    Loss_dB = 20*log10(distance) + 20*log10(frequency) - 147.55
    """
    # For teaching, we use a simplified model
    # Loss increases with distance
    reference_distance_km = 400  # e.g., low Earth orbit

    # Attenuation factor (inverse square law)
    attenuation = (reference_distance_km / distance_km) ** 2

    # Apply to signal
    attenuated_signal = signal * np.sqrt(attenuation)

    return attenuated_signal
'''

SNIPPET_FADING = '''
def apply_fading_events(signal, fade_events, sample_rate_hz, time_axis):
    """
    Apply fading events (temporary signal dropouts).

    🎓 TEACHING NOTE:
    Fading happens when:
      • Satellite goes behind clouds
      • Atmospheric turbulence
      • Objects blocking line of sight

    Signal strength temporarily drops!
    """
    faded_signal = signal.copy()

    for fade in fade_events:
        # Convert time to sample indices
        start_idx = int(fade.start_time * sample_rate_hz)
        duration_samples = int(fade.duration * sample_rate_hz)
        end_idx = start_idx + duration_samples

        # Ensure indices are valid
        end_idx = min(end_idx, len(signal))

        # Apply attenuation during fade
        # fade.severity: 0=no effect, 1=complete loss
        attenuation = 1.0 - fade.severity
        faded_signal[start_idx:end_idx] *= attenuation

    return faded_signal
'''

# ═══════════════════════════════════════════════════════════════
# METRICS SNIPPETS
# ═══════════════════════════════════════════════════════════════

SNIPPET_CALCULATE_BER = '''
def calculate_ber(original_bits, received_bits):
    """
    Calculate Bit Error Rate (BER).

    🎓 TEACHING NOTE:
    BER is the most important metric in communications!

    BER = (number of bit errors) / (total bits)

    Example:
      Sent:     [1, 0, 1, 1, 0]
      Received: [1, 0, 0, 1, 0]
                           ↑ error!
      BER = 1/5 = 0.2 = 20%
    """
    # Ensure same length
    min_len = min(len(original_bits), len(received_bits))
    orig = original_bits[:min_len]
    recv = received_bits[:min_len]

    # Count errors (XOR gives 1 where bits differ)
    errors = sum(o != r for o, r in zip(orig, recv))

    # Calculate BER
    if min_len == 0:
        return 0.0
    ber = errors / min_len

    return ber
'''

SNIPPET_SNR_CALCULATION = '''
def calculate_snr_db(clean_signal, noise):
    """
    Calculate Signal-to-Noise Ratio in decibels.

    🎓 TEACHING NOTE:
    SNR measures signal quality:
      High SNR (>20 dB) = clean signal, few errors
      Low SNR (<5 dB) = noisy signal, many errors

    Formula: SNR_dB = 10 * log10(signal_power / noise_power)
    """
    # Calculate powers (mean of squared values)
    signal_power = np.mean(clean_signal ** 2)
    noise_power = np.mean(noise ** 2)

    # Avoid division by zero
    if noise_power == 0:
        return float('inf')

    # Convert to dB (decibels)
    snr_linear = signal_power / noise_power
    snr_db = 10 * np.log10(snr_linear)

    return snr_db
'''

# ═══════════════════════════════════════════════════════════════
# COMPLETE PIPELINE SNIPPET
# ═══════════════════════════════════════════════════════════════

SNIPPET_COMPLETE_PIPELINE = '''
def simulate_transmission(message, distance_km, snr_db, use_fec=True):
    """
    Complete satellite transmission simulation.

    🎓 TEACHING NOTE:
    This is the COMPLETE pipeline, end-to-end!
    Watch data flow through each stage.
    """
    # ═══ STEP 1: Text → Bits ═══
    bits = text_to_bits(message)
    print(f"Message: {len(bits)} bits")

    # ═══ STEP 2: Create Packet ═══
    packet = create_packet(message.encode('utf-8'))
    print(f"Packet: {len(packet)} bytes")

    # ═══ STEP 3: Error Correction Encoding ═══
    if use_fec:
        encoded_bits = hamming_encode_message(bits)
        print(f"FEC: {len(encoded_bits)} bits (added redundancy)")
    else:
        encoded_bits = bits

    # ═══ STEP 4: BPSK Modulation ═══
    symbols = bits_to_bpsk_symbols(encoded_bits)
    modulated_signal = modulate_bpsk(symbols, carrier_freq_hz, sample_rate_hz)
    print("Modulated to BPSK")

    # ═══ STEP 5: Channel Effects ═══
    # 5a. Range loss
    signal_after_range = apply_free_space_loss(modulated_signal, distance_km)

    # 5b. Add noise
    received_signal = add_awgn(signal_after_range, snr_db)
    print(f"Channel: {distance_km} km, {snr_db} dB SNR")

    # ═══ STEP 6: Demodulation ═══
    received_symbols = demodulate_bpsk(received_signal, ...)
    received_bits = bpsk_symbols_to_bits(received_symbols)
    print("Demodulated")

    # ═══ STEP 7: Error Correction Decoding ═══
    if use_fec:
        corrected_bits = hamming_decode_message(received_bits)
        print("FEC applied")
    else:
        corrected_bits = received_bits

    # ═══ STEP 8: Reconstruct Message ═══
    received_message = bits_to_text(corrected_bits)

    # ═══ STEP 9: Calculate Metrics ═══
    ber = calculate_ber(bits, received_bits)
    print(f"BER: {ber:.6f}")

    # ═══ STEP 10: Return Results ═══
    return {
        'message_sent': message,
        'message_received': received_message,
        'ber': ber,
        'perfect_match': message == received_message
    }
'''

# ═══════════════════════════════════════════════════════════════
# SNIPPET CATALOG
# ═══════════════════════════════════════════════════════════════

SNIPPETS = {
    # Signal processing
    'generate_sine': SNIPPET_GENERATE_SINE,
    'add_noise': SNIPPET_ADD_NOISE,

    # Modulation
    'text_to_bits': SNIPPET_TEXT_TO_BITS,
    'bpsk_modulation': SNIPPET_BPSK_MODULATION,
    'bpsk_demodulation': SNIPPET_BPSK_DEMODULATION,

    # Error correction
    'crc_checksum': SNIPPET_CRC_CHECKSUM,
    'hamming_encode': SNIPPET_HAMMING_ENCODE,

    # Channel effects
    'range_loss': SNIPPET_RANGE_LOSS,
    'fading': SNIPPET_FADING,

    # Metrics
    'calculate_ber': SNIPPET_CALCULATE_BER,
    'snr_calculation': SNIPPET_SNR_CALCULATION,

    # Complete pipeline
    'complete_pipeline': SNIPPET_COMPLETE_PIPELINE,
}


def get_snippet(name):
    """
    Get a code snippet by name.

    Parameters
    ----------
    name : str
        Snippet name (key from SNIPPETS dict)

    Returns
    -------
    snippet : str
        Formatted code snippet
    """
    return SNIPPETS.get(name, f"# Snippet '{name}' not found")


def list_snippets():
    """List all available snippet names."""
    return list(SNIPPETS.keys())


# ═══════════════════════════════════════════════════════════════
# STREAMLIT INTEGRATION HELPER
# ═══════════════════════════════════════════════════════════════

def show_code_snippet(snippet_name, streamlit_ref=None):
    """
    Display a code snippet in Streamlit (if st is available).

    🎓 TEACHING NOTE:
    This helper makes it easy to show code in Streamlit pages.

    Usage in Streamlit:
        from utils.code_snippets import show_code_snippet
        show_code_snippet('generate_sine', st)

    Parameters
    ----------
    snippet_name : str
        Name of snippet to display
    streamlit_ref : module, optional
        Streamlit module (pass 'st')

    Returns
    -------
    snippet : str
        The snippet text (for non-Streamlit use)
    """
    snippet = get_snippet(snippet_name)

    if streamlit_ref is not None:
        with streamlit_ref.expander(f"🔍 Show Code: {snippet_name}"):
            streamlit_ref.code(snippet, language='python')

    return snippet


# ═══════════════════════════════════════════════════════════════
# DEBUGGING NOTES
# ═══════════════════════════════════════════════════════════════
#
# Common Issues:
#   1. Snippet not found → Check list_snippets()
#   2. Formatting looks wrong → Check indentation in snippet strings
#   3. Code doesn't run → These are TEACHING examples, may be simplified
#
# Usage Tips:
#   - Use in Streamlit pages to show "how it works"
#   - Snippets are educational, not production code
#   - Encourage students to copy and experiment
#
# ═══════════════════════════════════════════════════════════════
