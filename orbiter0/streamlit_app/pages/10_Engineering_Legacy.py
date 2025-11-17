"""
═══════════════════════════════════════════════════════════════════
CHAPTER 10: ENGINEERING LEGACY
Complete system reference and documentation
═══════════════════════════════════════════════════════════════════
"""

import streamlit as st

st.set_page_config(page_title="Engineering Legacy", page_icon="📘", layout="wide")

st.title("📘 Chapter 10: Engineering Legacy")

# Create tabs for organized content
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📐 Equations", "📊 Parameters", "🔧 Troubleshooting", "🎓 Resources", "🚀 Future"
])

# ═══════════════════════════════════════════════════════════════
# TAB 1: EQUATIONS AND FORMULAS
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.header("📐 Mathematical Reference")

    st.markdown("""
    ### Signal Generation

    **Sine Wave:**
    ```
    s(t) = A × sin(2π × f × t)

    Where:
      A = amplitude
      f = frequency (Hz)
      t = time (seconds)
    ```

    **Sampling:**
    ```
    Nyquist Theorem: f_sample ≥ 2 × f_max

    Where:
      f_sample = sampling rate
      f_max = highest frequency in signal
    ```

    ---

    ### Noise and SNR

    **Signal-to-Noise Ratio (Linear):**
    ```
    SNR = P_signal / P_noise

    Where:
      P_signal = signal power = mean(signal²)
      P_noise = noise power = mean(noise²)
    ```

    **SNR in Decibels:**
    ```
    SNR_dB = 10 × log₁₀(SNR)

    Example:
      SNR = 100  →  SNR_dB = 20 dB
      SNR = 10   →  SNR_dB = 10 dB
      SNR = 1    →  SNR_dB = 0 dB
    ```

    **Adding AWGN Noise:**
    ```
    noise_power = signal_power / (10^(SNR_dB/10))
    noise = normal(0, √noise_power)
    noisy_signal = signal + noise
    ```

    ---

    ### Modulation (BPSK)

    **Bit to Symbol Mapping:**
    ```
    bit = 0  →  symbol = -1  (phase = 180°)
    bit = 1  →  symbol = +1  (phase = 0°)

    Formula: symbol = 2×bit - 1
    ```

    **Modulated Signal:**
    ```
    s(t) = symbol × cos(2π × f_c × t)

    Where:
      f_c = carrier frequency
    ```

    **Demodulation (Coherent Detection):**
    ```
    1. Mix with carrier: r(t) × cos(2π × f_c × t)
    2. Integrate over symbol period
    3. Decision: value > 0 → bit=1, else bit=0
    ```

    ---

    ### Channel Effects

    **Free Space Path Loss (Simplified):**
    ```
    Attenuation = (d_ref / d)²

    Where:
      d = actual distance (km)
      d_ref = reference distance (km)
    ```

    **Path Loss in dB (Full Formula):**
    ```
    FSPL_dB = 20×log₁₀(d) + 20×log₁₀(f) - 147.55

    Where:
      d = distance (km)
      f = frequency (MHz)
    ```

    ---

    ### Error Metrics

    **Bit Error Rate (BER):**
    ```
    BER = (number of bit errors) / (total bits transmitted)

    Example:
      Sent:     10000 bits
      Errors:   100 bits
      BER = 100/10000 = 0.01 = 1%
    ```

    **Theoretical BPSK BER in AWGN:**
    ```
    BER = 0.5 × erfc(√SNR)

    Where:
      erfc = complementary error function
      SNR = signal-to-noise ratio (linear, not dB!)
    ```

    ---

    ### Error Correction

    **CRC-16 Polynomial:**
    ```
    CRC-16-CCITT: x¹⁶ + x¹² + x⁵ + 1
    Hex: 0x1021
    ```

    **Hamming(7,4) Parity Bits:**
    ```
    Position:  1  2  3  4  5  6  7
    Type:      P₁ P₂ D₁ P₄ D₂ D₃ D₄

    P₁ = D₁ ⊕ D₂ ⊕ D₄  (covers positions 1,3,5,7)
    P₂ = D₁ ⊕ D₃ ⊕ D₄  (covers positions 2,3,6,7)
    P₄ = D₂ ⊕ D₃ ⊕ D₄  (covers positions 4,5,6,7)

    Where ⊕ = XOR operation
    ```

    **Hamming Code Efficiency:**
    ```
    Efficiency = data_bits / total_bits
              = 4 / 7
              = 57%

    Overhead = 43%
    ```
    """)

# ═══════════════════════════════════════════════════════════════
# TAB 2: PARAMETER TABLES
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.header("📊 Parameter Reference Tables")

    st.subheader("Signal Parameters")
    st.table({
        "Parameter": ["Sample Rate", "Carrier Frequency", "Symbol Rate", "Amplitude"],
        "Default": ["44100 Hz", "1000 Hz", "100 Hz", "1.0"],
        "Range": ["1000-100000 Hz", "100-10000 Hz", "10-1000 Hz", "0.1-10.0"],
        "Notes": [
            "Must be ≥2× carrier freq",
            "Real satellites use GHz",
            "Lower = easier to visualize",
            "Normalized to 1.0"
        ]
    })

    st.subheader("Channel Parameters")
    st.table({
        "Parameter": ["SNR", "Distance", "Atmospheric Loss", "Fade Duration"],
        "Default": ["15 dB", "1000 km", "2 dB", "0.5 sec"],
        "Range": ["0-30 dB", "100-5000 km", "0-10 dB", "0.1-2.0 sec"],
        "Effect": [
            "Higher = fewer errors",
            "Farther = weaker signal",
            "Fixed additional loss",
            "Length of dropout"
        ]
    })

    st.subheader("SNR Quality Guide")
    st.table({
        "SNR (dB)": ["30", "20", "15", "10", "5", "0"],
        "Quality": ["Excellent", "Good", "Moderate", "Marginal", "Poor", "Unusable"],
        "Typical BER": ["~0.0001", "~0.001", "~0.01", "~0.05", "~0.15", "~0.4"],
        "Use Case": [
            "Ideal demos",
            "Near-perfect quality",
            "**DEFAULT - visible errors**",
            "FEC demonstration",
            "Challenging scenario",
            "Failure demonstration"
        ]
    })

    st.subheader("Packet Structure")
    st.table({
        "Section": ["Preamble", "Header", "Payload", "CRC"],
        "Size": ["4 bytes", "8 bytes", "Variable", "2 bytes"],
        "Content": [
            "0xAAAAAAAA (sync)",
            "ID + Length + Time",
            "Your message data",
            "CRC-16 checksum"
        ],
        "Purpose": [
            "Packet detection",
            "Metadata",
            "Actual data",
            "Error detection"
        ]
    })

# ═══════════════════════════════════════════════════════════════
# TAB 3: TROUBLESHOOTING
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.header("🔧 Troubleshooting Guide")

    st.subheader("Common Issues")

    with st.expander("❌ BER is always 0% (no errors)"):
        st.markdown("""
        **Causes:**
        - SNR too high (>25 dB)
        - No noise being added
        - Short messages (not enough bits to show errors)

        **Solutions:**
        - Lower SNR to 10-15 dB
        - Check noise generation code
        - Use longer messages (>100 bits)
        """)

    with st.expander("❌ BER is always 50% (random guessing)"):
        st.markdown("""
        **Causes:**
        - Demodulation not working
        - Carrier frequency mismatch
        - Symbol timing issues

        **Solutions:**
        - Verify carrier freq same for TX and RX
        - Check samples_per_symbol calculation
        - Inspect demodulated symbols (should be near ±1)
        """)

    with st.expander("❌ Message completely unrecoverable"):
        st.markdown("""
        **Causes:**
        - SNR too low (<3 dB)
        - Excessive fading
        - FEC disabled

        **Solutions:**
        - Increase SNR to ≥8 dB
        - Reduce fade severity
        - Enable FEC
        """)

    with st.expander("❌ CRC check always fails"):
        st.markdown("""
        **Causes:**
        - Packet format mismatch
        - Bit errors in header/CRC
        - Incorrect packet parsing

        **Solutions:**
        - Verify packet structure matches
        - Check that header is protected
        - Increase SNR to reduce errors
        """)

    with st.expander("❌ Plots look wrong"):
        st.markdown("""
        **Causes:**
        - Axis scaling issues
        - Too many/few samples displayed
        - Time axis doesn't match signal

        **Solutions:**
        - Check time_axis length == signal length
        - Limit displayed samples to 1000-2000
        - Verify sample rate used consistently
        """)

    st.subheader("Validation Tests")

    st.code("""
# Test 1: Perfect transmission (should work!)
result = simulate_transmission(
    message="Hello",
    snr_db=40,  # Very high SNR
    distance_km=100,  # Close
    use_fec=False
)
assert result['ber'] < 0.001, "Perfect case should have BER < 0.1%"

# Test 2: Noise effect visible
result_clean = simulate_transmission(snr_db=30, ...)
result_noisy = simulate_transmission(snr_db=10, ...)
assert result_noisy['ber'] > result_clean['ber'], "More noise → higher BER"

# Test 3: FEC helps
result_no_fec = simulate_transmission(snr_db=12, use_fec=False, ...)
result_with_fec = simulate_transmission(snr_db=12, use_fec=True, ...)
assert result_with_fec['ber'] < result_no_fec['ber'], "FEC should reduce BER"
""", language='python')

# ═══════════════════════════════════════════════════════════════
# TAB 4: LEARNING RESOURCES
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.header("🎓 Learning Resources")

    st.subheader("📚 Recommended Reading")

    st.markdown("""
    **Beginner Level:**
    - *"Digital Communications: Fundamentals and Applications"* by Bernard Sklar
    - *"Wireless Communications"* by Andrea Goldsmith (Chapters 1-5)
    - MIT OpenCourseWare: 6.450 Digital Communications

    **Intermediate Level:**
    - *"Software Defined Radio for Engineers"* (free from Analog Devices)
    - *"Communication Systems"* by Simon Haykin
    - IEEE Communications Society tutorials

    **Advanced Level:**
    - *"Digital Communications"* by John Proakis
    - *"Turbo Coding and Turbo Equalization"* by Claude Berrou
    - IEEE/ACM journals on wireless communications
    """)

    st.subheader("🌐 Online Tutorials")

    st.markdown("""
    - **DSP Guide**: dspguide.com (excellent free book)
    - **GNU Radio Tutorials**: wiki.gnuradio.org/index.php/Tutorials
    - **MATLAB Communications Toolbox**: mathworks.com/help/comm
    - **3GPP Specifications**: For real cellular standards
    - **AMSAT**: For amateur satellite communications
    """)

    st.subheader("🛠️ Hands-On Projects")

    st.markdown("""
    **Next Steps from ORBITER-0:**

    1. **Add QPSK Modulation** (Medium)
       - 2 bits per symbol instead of 1
       - I/Q representation
       - Constellation diagram

    2. **Implement Reed-Solomon FEC** (Medium-Hard)
       - Better for burst errors
       - Used in real satellites
       - More complex math

    3. **Real Orbital Mechanics** (Hard)
       - Keplerian elements
       - SGP4/SDP4 propagators
       - Real satellite tracking

    4. **Build an SDR Receiver** (Hard)
       - Use RTL-SDR dongle ($25)
       - Receive real signals
       - Decode FM radio, weather sats

    5. **Deep Space Simulation** (Very Hard)
       - 10M+ km distances
       - Doppler shift tracking
       - Hour-long propagation delays
    """)

# ═══════════════════════════════════════════════════════════════
# TAB 5: FUTURE DIRECTIONS
# ═══════════════════════════════════════════════════════════════
with tab5:
    st.header("🚀 Future Directions")

    st.subheader("ORBITER-1: Intermediate Version")

    st.markdown("""
    **Goals:**
    - More realistic orbital mechanics
    - Multiple modulation schemes
    - Advanced error correction
    - Real satellite frequencies

    **New Features:**
    - QPSK, 8PSK, 16QAM modulation
    - Reed-Solomon + Convolutional codes
    - Multiple ground stations
    - Doppler shift compensation
    - Actual satellite TLEs (Two-Line Elements)
    - Real antenna patterns

    **Technical Depth:**
    - Keplerian orbital elements
    - Pass prediction algorithms
    - Frequency planning
    - Link budget calculations
    """)

    st.subheader("ORBITER-DEEP-SPACE: Advanced Version")

    st.markdown("""
    **Scenario:**
    Communicate with a spacecraft at Mars distance (10M+ km)

    **Challenges:**
    - Extremely low SNR (<-10 dB signal below noise!)
    - 5-20 minute one-way light time
    - Doppler shift from orbital motion
    - Solar conjunction blackouts

    **Advanced Techniques:**
    - Turbo codes / LDPC codes
    - Concatenated coding
    - Interleaving for burst errors
    - Radiometric tracking
    - Arraying (combine multiple antennas)

    **Real Examples:**
    - Mars rovers (NASA/ESA)
    - Voyager probes (at edge of solar system!)
    - New Horizons (Pluto mission)
    """)

    st.success("""
    ### 🎓 You've Completed ORBITER-0!

    **What You Now Understand:**
    - ✅ How signals work (time & frequency domain)
    - ✅ Noise and its effects
    - ✅ Digital modulation (BPSK)
    - ✅ Channel impairments
    - ✅ Packet structure and framing
    - ✅ Error detection & correction
    - ✅ End-to-end system design

    **You're Ready For:**
    - Real wireless projects
    - SDR experimentation
    - Communications courses
    - Amateur radio
    - Satellite ground station operation

    **Keep Learning!** 🚀📡
    """)

st.divider()
st.caption("Chapter 10: Engineering Legacy | Phase 1 Structure Complete | Mission Success!")
