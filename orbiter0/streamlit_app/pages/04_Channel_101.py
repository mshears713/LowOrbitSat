"""
═══════════════════════════════════════════════════════════════════
CHAPTER 4: CHANNEL 101
How signals degrade over distance and through atmosphere
═══════════════════════════════════════════════════════════════════
"""

import streamlit as st

st.set_page_config(page_title="Channel 101", page_icon="🛰️", layout="wide")

st.title("🛰️ Chapter 4: Channel 101")

st.markdown("""
---

### The Journey Through Space 🌌

Signals don't magically teleport from satellite to ground station.
They travel through the **CHANNEL** - space and atmosphere - where
they get weaker and corrupted.

**Channel Effects:**
- 📏 **Range Loss:** Signal spreads out (inverse-square law)
- 🌫️ **Atmospheric Absorption:** Air isn't transparent to radio
- ⚡ **Fading:** Temporary dropouts from obstructions

---

### 🎯 Learning Objectives

- ✅ Free-space path loss (1/distance²)
- ✅ How distance affects signal strength
- ✅ Atmospheric absorption basics
- ✅ Fading events and burst errors
- ✅ Combined channel effects

---

### 🔬 Interactive Demo

**Status:** 🔜 Coming in Phase 2-3

- Adjust satellite distance
- See range loss calculation
- Add fade events on timeline
- Visualize combined effects

---

**➡️ Next:** Learn how to structure data in **Packets 101**

""")

st.info("📋 **Implementation Status:** Range loss in Phase 2, fading in Phase 3")

st.divider()
st.caption("Chapter 4: Channel 101 | Phase 1 Structure Complete")
