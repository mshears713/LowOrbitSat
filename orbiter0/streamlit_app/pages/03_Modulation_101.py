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

### 🔬 Interactive Demo

**Status:** 🔜 Coming in Phase 2

- Type a message
- See it convert to bits
- Watch BPSK encoding visualization
- Add noise and see demodulation errors
- Decode back to text

---

**➡️ Next:** Learn how distance affects signals in **Channel 101**

""")

st.info("📋 **Implementation Status:** BPSK demo coming in Phase 2")

st.divider()
st.caption("Chapter 3: Modulation 101 | Phase 1 Structure Complete")
