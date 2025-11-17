⭐ ORBITER-0: Beginner Satellite Communications Simulation & Streamlit Learning Console
TYPE: Teaching-Oriented Full-System Project (5 Phases, 50 Steps)
THEME: A tiny CubeSat drifting over Earth, sending curious little packets to ground stations
LEVEL: Beginner-Friendly Wireless Comms (Earth-Only)
PROJECT PURPOSE

This project teaches wireless communications fundamentals using a playful satellite theme.
All physics is simplified. All math is gentle.
Programming clarity, visuals, and intuition are the priority.

The system builds:

A simple, modular wireless signal simulation

A beginner-friendly packet + corruption + decoding pipeline

A timeline-based "satellite pass" simulator

A persistent mission archive

A 10-chapter Streamlit learning console with waveform visualizations, sliders, and interactive demos

Rich narrative headers, ASCII diagrams, debugging notes, and extension hints in every file

Claude Code will implement this project strictly according to the PHASES and STEPS in this document.

Claude Code must not modify this README after Phase 1.

All generated files must include:

Narrative header docstrings

ASCII diagrams

Inline teaching commentary

Debugging notes

Future-improvements sections

TEACHING GOALS
Primary Goals

What a signal is and how to simulate one

What noise is and how it corrupts signals

Beginner modulation (BPSK conceptual model only)

Packets, headers, checksums, corruption

Simple error detection & correction

Basic “satellite pass” model

Streamlit UI engineering

Building a simple ground-station console

Secondary Goals

Intro to async event loops

Simple spectrograms and plots

Persistent state via SQLite + caches

Designing maintainable modular Python systems

Coding intuition for communications pipelines

HIGH-LEVEL ARCHITECTURE

(Beginner version — no heavy physics)

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
                            │ clean bits
                   ┌────────▼────────┐
                   │  Anomaly Notes  │
                   │ (dropouts etc.) │
                   └────────┬────────┘
                            │
           ┌────────────────▼──────────────────┐
           │   Ground Station & Archive        │
           └────────────────┬──────────────────┘
                            │
            ┌───────────────▼───────────────────┐
            │  Streamlit Learning Console        │
            └────────────────────────────────────┘

DIRECTORY STRUCTURE
orbiter0/
  streamlit_app/
    Home.py
    pages/
      01_Signals_101.py
      02_Noise_101.py
      03_Modulation_101.py
      04_Channel_101.py
      05_Packets_101.py
      06_Error_Correction_101.py
      07_Downlink_Console.py
      08_Satellite_Pass_Simulator.py
      09_Mission_Archive.py
      10_Engineering_Legacy.py
    assets/
  src/
    signal/
      generator.py
      modulation.py
      spectrograms.py
    channel/
      noise.py
      range_loss.py
      fades.py
    comms/
      packetizer.py
      corruptor.py
      cleaner.py
      decoder.py
      anomalies.py
      storage.py
    utils/
      timing.py
      math_helpers.py
      plotting.py
    config/
      default_params.yaml
    data/
      missions.sqlite
    caches/
  README.md

PROJECT PHASE PLAN (50 STEPS)

Claude Code will complete these phases only when explicitly instructed.
Do NOT execute future phases early.
Do NOT modify completed phases.
Do NOT alter this README after Phase 1.

Each file must contain:

Narrative header docstrings

ASCII diagrams

Teaching commentary

Debugging notes

Future-improvement ideas

────────────────────────────────────────────────────────────
PHASE 1 — FOUNDATIONS (10 STEPS)
────────────────────────────────────────────────────────────

Create directory structure exactly as specified.

Create empty module files in all subsystem folders.

Add header docstrings to every file explaining teaching purpose.

Add ASCII diagrams to major subsystem files.

Create generator.py stub for signal creation with commentary.

Create noise.py stub with basic noise concept notes.

Create modulation.py stub (BPSK placeholder + teaching notes).

Create packetizer.py stub explaining packets conceptually.

Initialize all Streamlit pages with narrative headers only.

Add default_params.yaml with annotated beginner placeholders.

────────────────────────────────────────────────────────────
PHASE 2 — SIMPLE SIGNAL CHAIN (10 STEPS)
────────────────────────────────────────────────────────────

Implement basic waveform generator (sine & square) with plots.

Implement NoiseEngine (Gaussian noise).

Implement cartoon range-loss model (just multiplies signal).

Implement simple BPSK modulation (+1/–1 flipping).

Add text→bits→BPSK converter.

Implement mini spectrogram generator.

Build simple Channel model combining modulation + loss + noise.

Implement BPSK demodulator (sign detection).

Add bit error counter + simple teaching metrics.

Update Streamlit Signals/Noise/Modulation pages to demo all parts.

────────────────────────────────────────────────────────────
PHASE 3 — PACKETS, FADING, & REAL-WORLD CONSTRAINTS (10 STEPS)
────────────────────────────────────────────────────────────

Implement packetizer with headers + checksums.

Create packet corruption functions (byte flips, random drops).

Implement fade events (noise bursts, short-duration loss).

Add CRC/checksum validator.

Implement tiny Forward Error Correction (simple parity or Hamming).

Add atmospheric absorption as another scalar loss.

Implement a simple “satellite pass” timeline (strength over time).

Update Streamlit page for Packet Visualization.

Add mission archival logic to SQLite.

Add debugging helpers for packet inspection.

────────────────────────────────────────────────────────────
PHASE 4 — STREAMLIT LEARNING CONSOLE (10 STEPS)
────────────────────────────────────────────────────────────

Implement Home page with mission intro + diagrams.

Implement Signals 101 with interactive waveform generator.

Implement Noise 101 with noise-level slider.

Implement Modulation 101 with bit-flip animations.

Implement Channel 101 showing range loss & fades.

Implement Packets 101 with real-time corruption display.

Implement Error Correction 101 with toggles for FEC.

Implement Satellite Pass Simulator with timeline scrubber.

Implement Downlink Console showing live decoded bits.

Implement Mission Archive Browser.

────────────────────────────────────────────────────────────
PHASE 5 — FULL INTEGRATION & POLISH (10 STEPS)
────────────────────────────────────────────────────────────

Integrate signal + channel + packet pipeline into orchestrated runtime.

Add async/await version of downlink loop.

Wire Streamlit session_state for cross-page data.

Add global plotting helpers with teaching commentary.

Add code snippet overlays explaining each computation.

Tune noise & fading for intuitive behavior.

Add pass import/export tools.

Add Engineering Legacy page (final reference).

Add full debugging suite (self-test functions).

Add future-extensions guide (Planetary Deep Space version).

IMPLEMENTATION RULES FOR CLAUDE CODE

Claude Code must:

Follow the phases sequentially

Not skip or merge steps

Not modify this README after Phase 1

Include narrative headers, ASCII diagrams, and teaching comments in every file

Keep math simple and explanations clear

Not introduce new directories unless required by a step

Keep code educational, not minimal

Add debugging and future-extension notes to all major modules

DEVELOPER SETUP
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app/Home.py

MISSION FLOW SUMMARY

Generate signal

Add noise

Apply modulation

Send through channel (range loss, fades)

Convert to packets

Corrupt and validate

Decode

Detect anomalies

Archive

Visualize in Streamlit
