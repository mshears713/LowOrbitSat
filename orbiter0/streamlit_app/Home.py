"""
═══════════════════════════════════════════════════════════════════
ORBITER-0 HOME PAGE
Welcome to your satellite communications learning journey!
═══════════════════════════════════════════════════════════════════
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="ORBITER-0: Satellite Communications Simulator",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════
# MISSION BRIEFING
# ═══════════════════════════════════════════════════════════════════

st.title("🛰️ ORBITER-0: Beginner Satellite Communications")

st.markdown("""
---

### 📡 Welcome, Cadet!

You've been assigned to **Mission ORBITER-0**, a teaching-oriented simulation
of a tiny CubeSat drifting over Earth, sending curious little packets to ground stations.

**Your Mission:**
Learn the fundamentals of wireless communications through hands-on experimentation
with signals, noise, modulation, and error correction.

---

### 🎯 What You'll Learn

This system teaches wireless communications through **10 interactive chapters**:

1. **Signals 101** - What signals are and how to generate them
2. **Noise 101** - Understanding interference and SNR
3. **Modulation 101** - Encoding bits into waves (BPSK)
4. **Channel 101** - How signals degrade over distance
5. **Packets 101** - Structuring data for transmission
6. **Error Correction 101** - Detecting and fixing bit errors
7. **Downlink Console** - Live satellite communications simulator
8. **Satellite Pass Simulator** - Timeline-based visibility windows
9. **Mission Archive** - Historical data browser
10. **Engineering Legacy** - Complete reference documentation

---

### 🏗️ System Architecture

```
                 ┌────────────────────┐
                 │   Signal Generator │
                 │ (sine, square, BPSK)
                 └──────────┬─────────┘
                            │ samples
                  ┌─────────▼──────────┐
                  │     Noise Engine    │
                  │ (Gaussian, bursts)  │
                  └──────────┬─────────┘
                            │ noisy signal
                  ┌─────────▼──────────┐
                  │   Channel Model     │
                  │ (range loss, fades) │
                  └──────────┬─────────┘
                            │ degraded signal
         ┌──────────────────▼───────────────────┐
         │           Packetizer                 │
         │ (bits → frames → packets)            │
         └──────────────────┬───────────────────┘
                            │ packets
                ┌───────────▼────────────┐
                │  Cleaner & Decoder     │
                │ (CRC, simple FEC)      │
                └───────────┬────────────┘
                            │ clean message
                   ┌────────▼────────┐
                   │  Mission Archive│
                   └─────────────────┘
```

---

### 🚀 Getting Started

**Choose a chapter from the sidebar →**

We recommend starting with **Signals 101** and working through in order.
Each chapter builds on concepts from previous ones.

**Teaching Philosophy:**
- 📊 Visuals first - every concept has interactive demos
- 🎓 Gentle math - simplified for accessibility
- 🔧 Hands-on - adjust sliders and see immediate results
- 💡 Intuition over equations - understand the "why"

---

### 🌟 Project Status

**Phase 1: FOUNDATIONS** ✅ Complete
- Directory structure established
- Teaching-oriented stubs created
- Documentation framework in place

**Phase 2: SIMPLE SIGNAL CHAIN** ✅ Complete
- Waveform generation (sine, square)
- Noise engine (Gaussian, bursts)
- BPSK modulation & demodulation
- Simple channel model with range loss
- Spectrograms and bit error counting

**Phase 3: PACKETS & ERROR HANDLING** ✅ Complete
- Packet structure with headers & checksums
- CRC validation
- Forward Error Correction (Hamming codes)
- Atmospheric loss modeling
- Satellite pass timeline simulation
- Mission archival to SQLite
- Debugging tools

**Phase 4: STREAMLIT LEARNING CONSOLE** 🚀 In Progress
- Interactive teaching pages for all concepts
- Live visualization and experimentation
- Real-time parameter adjustment
- Mission control interfaces

**Phase 5:** Future full integration

---

### ⚠️ Important Notes

This is a **teaching system**, not production software:
- Physics is simplified
- Math is gentle
- Focus is on intuition and learning
- Real satellite systems are far more complex!

---

**Ready to begin your mission?**
👈 Select **Signals 101** from the sidebar to start learning!

""")

# Footer
st.divider()
st.caption("ORBITER-0 | Teaching-Oriented Satellite Communications Simulator | Phase 4: Learning Console Active")
