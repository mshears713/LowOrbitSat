"""
═══════════════════════════════════════════════════════════════════
CHAPTER 2: NOISE 101
Understanding interference and signal degradation
═══════════════════════════════════════════════════════════════════
"""

import streamlit as st

st.set_page_config(page_title="Noise 101", page_icon="📻", layout="wide")

st.title("📻 Chapter 2: Noise 101")

st.markdown("""
---

### The Imperfect Universe 🌌

Signals traveling through space don't stay perfect. They pick up **NOISE** -
random interference that corrupts the signal.

**What is noise?**
Think of noise like:
- 📺 Static on an old TV
- 📻 Hiss on a radio between stations
- ☎️ Background crackle on a bad phone call

**Where does noise come from?**
- ☀️ Thermal radiation from the sun
- 🌌 Cosmic background radiation
- ⚡ Electronics in the receiver
- 🌧️ Atmospheric interference

---

### 🎯 Learning Objectives

- ✅ What noise is and its sources
- ✅ Understanding AWGN (Additive White Gaussian Noise)
- ✅ Signal-to-Noise Ratio (SNR)
- ✅ How noise causes bit errors
- ✅ Converting to/from decibels (dB)

---

### 🔬 Interactive Demo

**Status:** 🔜 Coming in Phase 2

You'll be able to:
- Generate a clean signal
- Add adjustable noise (SNR slider)
- See clean vs noisy signals side-by-side
- Observe the Gaussian distribution of noise

---

### 📊 Understanding SNR

**SNR (Signal-to-Noise Ratio)** measures signal quality:

- **30 dB:** Excellent (signal 1000× stronger than noise)
- **20 dB:** Good (100× stronger)
- **10 dB:** Marginal (10× stronger)
- **0 dB:** Unusable (equal power)

---

**➡️ Next:** Learn how we encode bits into signals in **Modulation 101**

""")

st.info("📋 **Implementation Status:** Interactive demos coming in Phase 2")

st.divider()
st.caption("Chapter 2: Noise 101 | Phase 1 Structure Complete")
