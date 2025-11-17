"""
═══════════════════════════════════════════════════════════════════
COMMUNICATIONS MODULE
═══════════════════════════════════════════════════════════════════

Handles packet framing, error detection, correction, and storage.

Modules:
  • packetizer:  Create structured packets with headers and checksums
  • corruptor:   Inject bit errors for testing
  • cleaner:     Error detection (CRC validation)
  • decoder:     Forward Error Correction (FEC)
  • anomalies:   Track and log communication issues
  • storage:     SQLite database persistence

Teaching Focus: How data is packaged and protected in real systems
"""
