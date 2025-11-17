"""
═══════════════════════════════════════════════════════════════════
CHAPTER 1: SIGNALS 101
The foundation of all communication
═══════════════════════════════════════════════════════════════════
"""

import streamlit as st

st.set_page_config(page_title="Signals 101", page_icon="📡", layout="wide")

# ═══════════════════════════════════════════════════════════════════
# CHAPTER INTRODUCTION
# ═══════════════════════════════════════════════════════════════════

st.title("📡 Chapter 1: Signals 101")

st.markdown("""
---

### Welcome, Cadet! 🚀

Before our satellite can talk to Earth, it needs to create **SIGNALS**.

**What is a signal?**
A signal is just a pattern of energy changing over time. Think of it like:
- 🎵 Sound waves when you talk
- 🌊 Ripples spreading across a pond
- 💡 A flashlight blinking a message in Morse code

In wireless communications, signals are **electromagnetic waves** that
carry information through space.

---

### 🎯 Learning Objectives

By the end of this chapter, you'll understand:
- ✅ What a signal is (samples over time)
- ✅ How frequency and amplitude work
- ✅ The difference between sine and square waves
- ✅ How to visualize waveforms
- ✅ The concept of sampling rate

---

### 📚 Key Concepts

**Amplitude:** How "tall" the wave is (signal strength)

**Frequency:** How many cycles happen per second (measured in Hertz)
- 1 Hz = 1 cycle per second
- 1000 Hz = 1000 cycles per second

**Sample Rate:** How many measurements we take per second
- Must be at least 2× the highest frequency (Nyquist theorem)

**Waveforms:**
- **Sine wave:** Smooth, fundamental oscillation
- **Square wave:** Digital-like, abrupt transitions

---

### 🔬 Interactive Demo

**Status:** 🔜 Coming in Phase 2

The interactive signal generator will let you:
- Adjust frequency with a slider
- Change amplitude
- Switch between sine and square waves
- See the waveform plotted in real-time

**Preview:**
```
Frequency (Hz):  [slider 1-100]
Amplitude:       [slider 0.1-2.0]
Wave Type:       [Sine | Square]

[Real-time plot will appear here]
```

---

### 💡 Why This Matters

Understanding signals is the **foundation** of everything in wireless communications:
- Without signals, there's no way to transmit information
- Every other concept (noise, modulation, errors) builds on this
- Real satellite systems use complex signals, but the basics are the same

---

### 🎓 Try This Next

Once Phase 2 is implemented, experiment with:
1. Generate a 10 Hz sine wave - count the cycles
2. Increase frequency to 50 Hz - notice how it oscillates faster
3. Switch to square wave - see the digital-like transitions
4. Lower the sample rate - see what happens (spoiler: aliasing!)

---

### ➡️ Next Chapter

When you're ready, move on to **Noise 101** to see how signals
get corrupted during transmission.

---

""")

st.info("📋 **Implementation Status:** This page will be fully interactive in Phase 2")

# Footer
st.divider()
st.caption("Chapter 1: Signals 101 | Phase 1 Structure Complete")
