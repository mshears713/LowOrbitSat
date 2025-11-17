"""
═══════════════════════════════════════════════════════════════════
CHAPTER 3: MODULATION 101
Encoding bits into signals - BPSK fundamentals
═══════════════════════════════════════════════════════════════════
"""

import streamlit as st

st.set_page_config(page_title="Modulation 101", page_icon="🔀", layout="wide")

st.title("🔀 Chapter 3: Modulation 101")

st.markdown("""
---

### From Bits to Waves 🌊

Our satellite needs to send **BITS** (0s and 1s) through space.
But space only understands **WAVES** (electromagnetic radiation).

**The Solution: MODULATION**
- Encoding: Bits → Waves (modulation)
- Decoding: Waves → Bits (demodulation)

---

### 🎯 Learning Objectives

- ✅ What modulation is and why we need it
- ✅ BPSK (Binary Phase Shift Keying) basics
- ✅ Converting text → bits → symbols → signal
- ✅ How to demodulate signals back to bits
- ✅ How noise affects symbol detection

---

### 🔬 BPSK Mapping

**Binary Phase Shift Keying** is the simplest modulation:

```
Bit 0  →  Symbol -1  →  Wave with 180° phase
Bit 1  →  Symbol +1  →  Wave with 0° phase
```

**Demodulation:**
```
Sample > 0  →  Symbol +1  →  Bit 1
Sample < 0  →  Symbol -1  →  Bit 0
```

(Errors happen when noise flips the sign!)

---
""")

# ═══════════════════════════════════════════════════════════════════
# INTERACTIVE DEMO
# ═══════════════════════════════════════════════════════════════════

st.header("🔬 Interactive BPSK Modulator & Demodulator")

st.markdown("""
Send a message through the BPSK communication system!
Watch as your text is converted to bits, modulated, transmitted through a noisy channel, and decoded back.
""")

# Add path to import our modules
import sys
sys.path.append('../../src')

from signals.modulation import (
    text_to_bits, bits_to_text, bits_to_bpsk_symbols,
    bpsk_symbols_to_bits, modulate_bpsk, demodulate_bpsk
)
from channel.noise import add_awgn
from utils.math_helpers import calculate_ber, ber_to_quality_string
import matplotlib.pyplot as plt
import numpy as np

# User input
col1, col2 = st.columns([2, 1])

with col1:
    message = st.text_input(
        "Your Message",
        value="Hi",
        max_chars=20,
        help="Keep it short (max 20 chars) for clear visualization"
    )

with col2:
    snr_db = st.slider(
        "Channel SNR (dB)",
        min_value=0,
        max_value=25,
        value=15,
        help="Signal quality: Higher = less errors"
    )

if message:
    # Step 1: Text to bits
    bits = text_to_bits(message)

    st.markdown(f"""
    ### 📝 Step 1: Text → Bits
    **Message:** `"{message}"`
    **Bits:** `{bits[:32]}{'...' if len(bits) > 32 else ''}`
    **Total bits:** {len(bits)} ({len(bits)//8} characters × 8 bits/char)
    """)

    # Step 2: Bits to BPSK symbols
    symbols = bits_to_bpsk_symbols(bits)

    st.markdown(f"""
    ### 🔀 Step 2: Bits → BPSK Symbols
    **BPSK Mapping:** Bit 0 → Symbol -1, Bit 1 → Symbol +1
    **Symbols:** `{list(symbols[:16])}{'...' if len(symbols) > 16 else ''}`
    """)

    # Step 3: Modulate
    carrier_freq = 100  # Hz
    sample_rate = 10000  # Hz
    signal, time_axis = modulate_bpsk(symbols, carrier_freq, sample_rate)

    # Step 4: Add noise
    noisy_signal, noise = add_awgn(signal, snr_db)

    # Step 5: Demodulate
    demod_symbols = demodulate_bpsk(noisy_signal, carrier_freq, sample_rate, len(symbols))
    demod_bits = bpsk_symbols_to_bits(demod_symbols)
    decoded_message = bits_to_text(demod_bits)

    # Calculate BER
    ber, num_errors, total_bits = calculate_ber(bits, demod_bits)
    quality = ber_to_quality_string(ber)

    # Visualization
    st.markdown("### 📊 Step 3: Modulation & Transmission")

    # Show a portion of the modulated signal
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))

    # Plot 1: Clean modulated signal (zoomed to show a few symbols)
    samples_per_symbol = len(signal) // len(symbols)
    show_symbols = min(8, len(symbols))  # Show up to 8 symbols
    show_samples = show_symbols * samples_per_symbol

    ax1.plot(time_axis[:show_samples], signal[:show_samples],
             linewidth=1.5, color='blue', label='Clean Signal')
    ax1.set_xlabel('Time (seconds)', fontsize=10)
    ax1.set_ylabel('Amplitude', fontsize=10)
    ax1.set_title(f'BPSK Modulated Signal (First {show_symbols} symbols)', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # Highlight symbol boundaries
    for i in range(show_symbols + 1):
        ax1.axvline(x=time_axis[i * samples_per_symbol] if i * samples_per_symbol < len(time_axis) else time_axis[-1],
                   color='red', linestyle='--', alpha=0.3, linewidth=1)

    # Add symbol labels
    for i in range(min(show_symbols, len(symbols))):
        mid_sample = i * samples_per_symbol + samples_per_symbol // 2
        if mid_sample < len(time_axis):
            symbol_val = symbols[i]
            bit_val = bits[i]
            ax1.text(time_axis[mid_sample], 1.3, f'Bit:{bit_val}\nSym:{symbol_val}',
                    ha='center', fontsize=8, color='darkred', fontweight='bold')

    # Plot 2: Noisy signal
    ax2.plot(time_axis[:show_samples], noisy_signal[:show_samples],
             linewidth=1, color='red', alpha=0.7, label='Noisy Signal')
    ax2.set_xlabel('Time (seconds)', fontsize=10)
    ax2.set_ylabel('Amplitude', fontsize=10)
    ax2.set_title(f'After Channel (SNR = {snr_db} dB)', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # Results
    st.markdown("### 📥 Step 4: Demodulation & Decoding")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown(f"""
        **Original Message:**
        `"{message}"`

        **Received Message:**
        `"{decoded_message}"`

        **Match:** {'✅ Yes!' if message == decoded_message else '❌ No (errors occurred)'}
        """)

    with col_b:
        st.markdown(f"""
        **Bit Error Rate:**
        {ber:.6f} ({ber*100:.4f}%)

        **Errors:** {num_errors} / {total_bits} bits

        **Quality:** {quality}
        """)

    # Show quality indicator
    if ber == 0:
        st.success("🎉 **Perfect transmission!** No bit errors detected.")
    elif ber < 0.01:
        st.info("📶 **Good quality:** Minor errors, message likely intact")
    elif ber < 0.1:
        st.warning("⚠️ **Degraded:** Significant errors, message may be corrupted")
    else:
        st.error("❌ **Poor quality:** Heavy corruption, message likely unreadable")

    # Teaching notes
    st.markdown(f"""
    ---

    ### 🎓 What You're Seeing

    **Top Plot:** BPSK modulated signal showing phase shifts
    - Symbol +1 (bit 1) → normal sine wave (0° phase)
    - Symbol -1 (bit 0) → inverted sine wave (180° phase)
    - Red dashed lines show symbol boundaries

    **Bottom Plot:** Same signal after passing through noisy channel
    - Noise makes it harder to detect the correct symbol
    - Demodulator checks: "Is this sample positive or negative?"
    - If noise flips the sign → **bit error!**

    **Try This:**
    1. High SNR (20+ dB) → Should get perfect message
    2. Low SNR (< 5 dB) → Lots of errors
    3. Try messages with different characters → see bit patterns
    4. Note: Even 1% BER can corrupt text significantly!

    ---

**➡️ Next:** Learn how distance affects signals in **Channel 101**

""")

else:
    st.warning("👆 Enter a message above to see BPSK modulation in action!")

st.markdown("""
---
""")

st.success("✅ **Interactive Demo Active:** Type a message and watch it travel through the communication system!")

st.divider()
st.caption("Chapter 3: Modulation 101 | Phase 4: Fully Interactive Learning Console")
