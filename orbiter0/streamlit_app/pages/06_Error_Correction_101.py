"""
═══════════════════════════════════════════════════════════════════
CHAPTER 6: ERROR CORRECTION 101
Fixing errors without retransmission
═══════════════════════════════════════════════════════════════════
"""

import streamlit as st

st.set_page_config(page_title="Error Correction 101", page_icon="🔧", layout="wide")

st.title("🔧 Chapter 6: Error Correction 101")

st.markdown("""
---

### Not Just Detecting - FIXING! 🛠️

**Error Detection** (like CRC): Knows something is wrong
**Error Correction** (FEC): Actually FIXES what's wrong

**Forward Error Correction (FEC)** adds redundancy so we can
correct errors without asking for retransmission.

Example: "I s_nt you a m_ssage"
Even with missing letters, you can figure it out!

---

### 🎯 Learning Objectives

- ✅ Detection vs correction
- ✅ How redundancy enables correction
- ✅ Parity bits (simple detection)
- ✅ Hamming codes (single-bit correction)
- ✅ Trade-off: bandwidth vs reliability

---

### 🔬 Error Correction Techniques

**Parity Bit:**
- Simplest error detection
- Detects odd number of bit flips
- Cannot correct

**Hamming(7,4) Code:**
- 4 data bits → 7 total bits (3 parity)
- Can correct 1-bit errors
- Can detect 2-bit errors
- 43% overhead

---

---
""")

# Add path to import our modules
import sys
sys.path.append('../../src')

from comms.decoder import add_parity_bit, check_parity_bit, hamming_encode_4bit, hamming_decode_4bit
import numpy as np

# ═══════════════════════════════════════════════════════════════════
# DEMO 1: PARITY BIT
# ═══════════════════════════════════════════════════════════════════

st.header("🔬 Demo 1: Parity Bit (Detection Only)")

st.markdown("""
The simplest error detection: add 1 extra bit that makes the total number of 1s even (or odd).
**Cannot correct** errors - only detect them!
""")

col1, col2 = st.columns(2)

with col1:
    data_bits_str = st.text_input(
        "Data Bits (4 bits)",
        value="1010",
        max_chars=4,
        help="Enter 4 binary digits"
    )

with col2:
    flip_parity_bit = st.checkbox("Flip a bit (simulate error)", value=False)

if len(data_bits_str) == 4 and all(b in '01' for b in data_bits_str):
    data_bits = [int(b) for b in data_bits_str]

    # Encode with parity
    encoded = add_parity_bit(data_bits)

    st.markdown(f"""
    ### Encoding:
    - **Data bits:** `{data_bits}` → `{''.join(map(str, data_bits))}`
    - **Parity bit:** `{encoded[-1]}` (makes total 1s even)
    - **Encoded:** `{''.join(map(str, encoded))}` (5 bits total)
    """)

    # Simulate error
    test_bits = encoded.copy()
    if flip_parity_bit:
        test_bits[2] = 1 - test_bits[2]  # Flip middle bit
        st.warning(f"⚠️ **Flipped bit at index 2:** `{''.join(map(str, test_bits))}`")

    # Check parity
    parity_valid = check_parity_bit(test_bits)

    if parity_valid:
        st.success(f"✅ **Parity Check PASSED** - No errors detected")
    else:
        st.error(f"❌ **Parity Check FAILED** - Error detected (but cannot fix it!)")

    st.info("""
    **Limitation:** Parity can only **detect** errors, not fix them.
    If 2 bits flip, parity won't detect it!
    """)
else:
    st.warning("👆 Enter exactly 4 binary digits (0 or 1)")

st.markdown("""
---
""")

# ═══════════════════════════════════════════════════════════════════
# DEMO 2: HAMMING CODE
# ═══════════════════════════════════════════════════════════════════

st.header("🔬 Demo 2: Hamming(7,4) Code (Can Correct!)")

st.markdown("""
**Hamming codes** add redundancy strategically so we can:
- **Detect** 2-bit errors
- **Correct** 1-bit errors automatically!

**Hamming(7,4):** 4 data bits → 7 total bits (3 parity bits)
""")

col_a, col_b = st.columns([2, 1])

with col_a:
    hamming_data_str = st.text_input(
        "Data Bits (4 bits)",
        value="1101",
        max_chars=4,
        key="hamming_input",
        help="Enter 4 binary digits"
    )

with col_b:
    error_mode = st.selectbox(
        "Error Injection",
        ["No Error", "1-Bit Error (correctable)", "2-Bit Error (detectable only)"],
        help="Simulate transmission errors"
    )

if len(hamming_data_str) == 4 and all(b in '01' for b in hamming_data_str):
    hamming_data = [int(b) for b in hamming_data_str]

    # Encode with Hamming
    hamming_encoded = hamming_encode_4bit(hamming_data)

    st.markdown(f"""
    ### 📤 Encoding Process:
    - **Original data:** `{hamming_data}` → `{''.join(map(str, hamming_data))}`
    - **Hamming(7,4) encoded:** `{''.join(map(str, hamming_encoded))}` (7 bits)
    - **Overhead:** 3 parity bits (43% overhead)
    """)

    # Show bit positions
    st.code(f"""
    Position: 1   2   3   4   5   6   7
    Bit:      {hamming_encoded[0]}   {hamming_encoded[1]}   {hamming_encoded[2]}   {hamming_encoded[3]}   {hamming_encoded[4]}   {hamming_encoded[5]}   {hamming_encoded[6]}
    Type:     P   P   D   P   D   D   D
              ^   ^   ^   ^   ^   ^   ^
           (Parity bits at positions 1, 2, 4)
    """, language="")

    # Simulate errors
    received_bits = hamming_encoded.copy()
    error_positions = []

    if error_mode == "1-Bit Error (correctable)":
        error_positions = [3]  # Flip bit at position 3 (index 3)
        received_bits[3] = 1 - received_bits[3]
        st.warning(f"⚠️ **Injected 1-bit error at position 4:** `{''.join(map(str, received_bits))}`")

    elif error_mode == "2-Bit Error (detectable only)":
        error_positions = [2, 5]
        received_bits[2] = 1 - received_bits[2]
        received_bits[5] = 1 - received_bits[5]
        st.warning(f"⚠️ **Injected 2-bit errors at positions 3, 6:** `{''.join(map(str, received_bits))}`")

    # Decode
    decoded_data = hamming_decode_4bit(received_bits)

    st.markdown(f"""
    ### 📥 Decoding & Correction:
    - **Received bits:** `{''.join(map(str, received_bits))}`
    - **Decoded data:** `{''.join(map(str, decoded_data))}`
    - **Original data:** `{''.join(map(str, hamming_data))}`
    """)

    # Check if correction worked
    if decoded_data == hamming_data:
        if error_mode == "No Error":
            st.success("✅ **Perfect transmission** - No errors")
        elif error_mode == "1-Bit Error (correctable)":
            st.success("🎉 **Error CORRECTED!** Hamming code automatically fixed the flipped bit!")
            st.info(f"The error at position {error_positions[0]+1} was detected and corrected.")
        else:
            st.error("❌ This shouldn't happen with 2-bit errors")
    else:
        st.error(f"❌ **Decoding failed** - Too many errors for Hamming(7,4) to correct")
        st.warning("Hamming(7,4) can only **correct 1 bit** or **detect 2 bits**. With 2-bit errors, it detects but cannot fix.")

    st.markdown("""
    ---

    ### 🎓 How Hamming Codes Work

    **Parity Bit Placement:**
    - Parity bits go at positions that are powers of 2: 1, 2, 4, 8, ...
    - Each parity bit checks specific bit positions
    - When we decode, we check all parity bits
    - The pattern of failures tells us **exactly which bit is wrong**!

    **Example:**
    ```
    If parity checks fail at positions 1 and 2:
    → Error is at position 1+2 = 3
    → Flip bit 3 to correct it!
    ```

    **Try This:**
    1. Send clean data → see encoding
    2. Inject 1-bit error → watch it get corrected!
    3. Inject 2-bit error → see detection without correction
    4. Try different data patterns

    """)

else:
    st.warning("👆 Enter exactly 4 binary digits (0 or 1)")

st.markdown("""
---
""")

# ═══════════════════════════════════════════════════════════════════
# DEMO 3: COMPARISON
# ═══════════════════════════════════════════════════════════════════

st.header("🔬 Demo 3: FEC Comparison")

st.markdown("""
Let's compare different error correction strategies!
""")

# Simulate transmission with various BER
ber_values = [0, 0.01, 0.05, 0.1, 0.2]
strategies = ["No FEC", "Parity (detect only)", "Hamming(7,4)"]

# Create comparison table
st.markdown("### 📊 Error Correction Performance")

# Sample data
sample_data = [1, 1, 0, 1]

results_data = []

for ber in ber_values:
    row = {"BER": f"{ber:.0%}"}

    # No FEC
    errors_no_fec = int(4 * ber)  # Average number of bit errors
    row["No FEC"] = "❌ Failed" if errors_no_fec > 0 else "✅ OK"

    # Parity
    row["Parity"] = "⚠️ Detected" if errors_no_fec > 0 else "✅ OK"

    # Hamming
    if errors_no_fec == 0:
        row["Hamming(7,4)"] = "✅ OK"
    elif errors_no_fec == 1:
        row["Hamming(7,4)"] = "✅ Corrected"
    else:
        row["Hamming(7,4)"] = "❌ Too many errors"

    results_data.append(row)

import pandas as pd
df = pd.DataFrame(results_data)
st.table(df)

st.markdown("""
**Analysis:**
- **No FEC:** Fast but unreliable - any error breaks the data
- **Parity:** Can detect errors but needs retransmission
- **Hamming(7,4):** Can fix 1-bit errors without retransmission!

**Trade-offs:**
- **Bandwidth:** Hamming uses 43% more bandwidth (3 extra bits per 4 data bits)
- **Latency:** No retransmission needed = faster overall
- **Complexity:** More complex encoding/decoding logic

**Real Satellites:**
- Use advanced codes: Reed-Solomon, Turbo codes, LDPC
- Can correct many errors with less overhead
- Critical for deep space missions (Mars rovers, Voyager, etc.)

---

**➡️ Next:** Try the **Satellite Pass Simulator** for timeline views

""")

st.success("✅ **Interactive Demo Active:** Toggle FEC and watch error correction in action!")

st.divider()
st.caption("Chapter 6: Error Correction 101 | Phase 4: Fully Interactive Learning Console")
