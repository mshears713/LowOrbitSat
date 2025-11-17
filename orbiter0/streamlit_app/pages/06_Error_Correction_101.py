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

### 🔬 Interactive Demo

**Status:** 🔜 Coming in Phase 3-4

- Compare: No FEC vs Parity vs Hamming
- Inject bit errors
- Watch correction in action
- See BER improvement charts

---

**➡️ Next:** Try the **Downlink Console** for live simulation

""")

st.info("📋 **Implementation Status:** FEC implementation in Phase 3-4")

st.divider()
st.caption("Chapter 6: Error Correction 101 | Phase 1 Structure Complete")
