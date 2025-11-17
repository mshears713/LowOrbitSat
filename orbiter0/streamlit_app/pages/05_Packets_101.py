"""
═══════════════════════════════════════════════════════════════════
CHAPTER 5: PACKETS 101
Structuring data for reliable transmission
═══════════════════════════════════════════════════════════════════
"""

import streamlit as st

st.set_page_config(page_title="Packets 101", page_icon="📦", layout="wide")

st.title("📦 Chapter 5: Packets 101")

st.markdown("""
---

### Organizing the Data 📬

You can't just throw random bits into space! Real systems organize
data into **PACKETS** - structured bundles with headers and checksums.

**Packet = Header + Payload + Checksum**

Think of it like mailing a letter:
- 📮 Header = address and return address
- 📄 Payload = the letter itself
- ✅ Checksum = delivery confirmation

---

### 🎯 Learning Objectives

- ✅ Why we need packet structure
- ✅ Header fields (ID, length, timestamp)
- ✅ Checksums for error detection (CRC)
- ✅ Packet overhead trade-offs
- ✅ Framing and synchronization

---

### 📋 Packet Structure

```
┌──────────────────────────────────────────┐
│ PREAMBLE (sync)      │ 4 bytes           │
├──────────────────────────────────────────┤
│ HEADER               │ 8 bytes           │
│   - Packet ID        │ (2 bytes)         │
│   - Length           │ (2 bytes)         │
│   - Timestamp        │ (4 bytes)         │
├──────────────────────────────────────────┤
│ PAYLOAD              │ N bytes           │
├──────────────────────────────────────────┤
│ CRC-16 Checksum      │ 2 bytes           │
└──────────────────────────────────────────┘
```

---

### 🔬 Interactive Demo

**Status:** 🔜 Coming in Phase 3

- Create packets from text
- View hex dump
- Inject errors
- Test CRC validation

---

**➡️ Next:** Learn error correction in **Error Correction 101**

""")

st.info("📋 **Implementation Status:** Packet system coming in Phase 3")

st.divider()
st.caption("Chapter 5: Packets 101 | Phase 1 Structure Complete")
