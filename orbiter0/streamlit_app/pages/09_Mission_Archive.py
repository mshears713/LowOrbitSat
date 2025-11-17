"""
═══════════════════════════════════════════════════════════════════
CHAPTER 9: MISSION ARCHIVE
Historical data browser and analysis
═══════════════════════════════════════════════════════════════════
"""

import streamlit as st

st.set_page_config(page_title="Mission Archive", page_icon="📚", layout="wide")

st.title("📚 Chapter 9: Mission Archive")

st.markdown("""
---

### The Mission Log 📖

Every satellite pass is saved to a **SQLite database** for
later analysis and learning.

**Archived Data:**
- 📝 Messages sent and received
- 📊 Signal quality metrics (SNR, BER)
- ⏱️ Timestamps
- ❌ Error statistics
- 📈 Pass parameters

---

### 🎯 Learning Objectives

- ✅ Database basics (SQLite)
- ✅ Data persistence
- ✅ Historical analysis
- ✅ Performance trending
- ✅ Query and filter operations

---

---
""")

# Add path to import our modules
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from comms.storage import init_database, save_mission, query_missions, get_mission_statistics, clear_database, get_default_db_path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ═══════════════════════════════════════════════════════════════════
# MISSION ARCHIVE BROWSER
# ═══════════════════════════════════════════════════════════════════

st.header("🔬 Mission Archive Browser")

# Initialize database
db_path = get_default_db_path()
init_database(db_path)

# Check if database exists and has data
if os.path.exists(db_path):
    try:
        missions = query_missions(limit=1000, db_path=db_path)
        stats = get_mission_statistics(db_path)
    except:
        missions = []
        stats = {'total_missions': 0, 'avg_ber': 0, 'avg_snr_db': 0, 'success_rate': 0}
else:
    missions = []
    stats = {'total_missions': 0, 'avg_ber': 0, 'avg_snr_db': 0, 'success_rate': 0}

if stats['total_missions'] > 0:
    # Display statistics
    st.markdown("### 📊 Archive Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Missions", stats['total_missions'])

    with col2:
        st.metric("Success Rate", f"{stats['success_rate']*100:.1f}%")

    with col3:
        st.metric("Avg BER", f"{stats['avg_ber']:.6f}")

    with col4:
        st.metric("Avg SNR", f"{stats['avg_snr_db']:.1f} dB")

    # Filter controls
    st.markdown("### 🔍 Filter Missions")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        min_snr_filter = st.number_input(
            "Min SNR (dB)",
            min_value=0,
            max_value=30,
            value=0,
            help="Show missions with SNR >= this value"
        )

    with col_b:
        max_ber_filter = st.number_input(
            "Max BER",
            min_value=0.0,
            max_value=1.0,
            value=1.0,
            step=0.01,
            format="%.4f",
            help="Show missions with BER <= this value"
        )

    with col_c:
        show_limit = st.number_input(
            "Max Results",
            min_value=10,
            max_value=1000,
            value=100,
            step=10,
            help="Maximum number of missions to display"
        )

    # Query with filters
    filtered_missions = query_missions(
        limit=show_limit,
        min_snr_db=min_snr_filter if min_snr_filter > 0 else None,
        max_ber=max_ber_filter if max_ber_filter < 1.0 else None,
        db_path=db_path
    )

    st.markdown(f"**Found {len(filtered_missions)} missions matching filters**")

    # Display missions
    if len(filtered_missions) > 0:
        st.markdown("### 📋 Mission List")

        # Convert to DataFrame for better display
        df_data = []
        for mission in filtered_missions:
            success = (mission[2] == mission[3])  # message_sent == message_received
            df_data.append({
                'ID': mission[0],
                'Timestamp': mission[7],
                'SNR (dB)': mission[5] if mission[5] else 'N/A',
                'BER': f"{mission[4]:.6f}" if mission[4] is not None else 'N/A',
                'Sent': mission[2][:30] + '...' if len(mission[2]) > 30 else mission[2],
                'Received': mission[3][:30] + '...' if len(mission[3]) > 30 else mission[3],
                'Success': '✅' if success else '❌'
            })

        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, height=400)

        # Visualizations
        st.markdown("### 📈 Performance Analysis")

        # Extract data for plotting
        snr_values = [m[5] for m in filtered_missions if m[5] is not None]
        ber_values = [m[4] for m in filtered_missions if m[4] is not None]
        success_values = [1 if m[2] == m[3] else 0 for m in filtered_missions]

        if len(snr_values) > 0 and len(ber_values) > 0:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

            # Plot 1: BER vs SNR scatter
            ax1.scatter(snr_values, ber_values, alpha=0.6, s=50, c='blue')
            ax1.set_xlabel('SNR (dB)', fontsize=11)
            ax1.set_ylabel('Bit Error Rate', fontsize=11)
            ax1.set_title('BER vs SNR', fontsize=13, fontweight='bold')
            ax1.grid(True, alpha=0.3)
            ax1.set_yscale('log')

            # Plot 2: Success rate by SNR bins
            snr_bins = np.arange(0, 31, 5)
            success_by_snr = []
            bin_centers = []

            for i in range(len(snr_bins) - 1):
                mask = [(snr_bins[i] <= s < snr_bins[i+1]) for s in snr_values]
                if sum(mask) > 0:
                    successes = [success_values[j] for j, m in enumerate(mask) if m]
                    success_rate = np.mean(successes)
                    success_by_snr.append(success_rate * 100)
                    bin_centers.append((snr_bins[i] + snr_bins[i+1]) / 2)

            if len(bin_centers) > 0:
                ax2.bar(bin_centers, success_by_snr, width=4, alpha=0.7, color='green')
                ax2.set_xlabel('SNR (dB)', fontsize=11)
                ax2.set_ylabel('Success Rate (%)', fontsize=11)
                ax2.set_title('Success Rate by SNR Range', fontsize=13, fontweight='bold')
                ax2.grid(True, alpha=0.3, axis='y')
                ax2.set_ylim([0, 105])

            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

        # Detailed mission viewer
        st.markdown("---")
        st.markdown("### 🔎 Mission Details")

        selected_id = st.selectbox(
            "Select Mission ID",
            options=[m[0] for m in filtered_missions],
            format_func=lambda x: f"Mission {x}"
        )

        if selected_id:
            # Find the selected mission
            selected_mission = next((m for m in filtered_missions if m[0] == selected_id), None)

            if selected_mission:
                mid, _, msg_sent, msg_received, ber, distance_km, snr_db, timestamp = selected_mission
                success = (msg_sent == msg_received)

                col_i, col_ii = st.columns(2)

                with col_i:
                    st.markdown(f"""
                    **Mission ID:** {mid}
                    **Timestamp:** {timestamp}
                    **Success:** {'✅ Yes' if success else '❌ No'}
                    """)

                with col_ii:
                    st.markdown(f"""
                    **SNR:** {snr_db if snr_db else 'N/A'} dB
                    **BER:** {ber:.6f if ber is not None else 'N/A'}
                    **Distance:** {distance_km if distance_km else 'N/A'} km
                    """)

                # Message comparison
                col_x, col_y = st.columns(2)

                with col_x:
                    st.markdown("**Message Sent:**")
                    st.code(msg_sent, language="")

                with col_y:
                    st.markdown("**Message Received:**")
                    st.code(msg_received, language="")

                # Character-level diff
                if msg_sent != msg_received:
                    st.markdown("**Character Differences:**")
                    max_len = max(len(msg_sent), len(msg_received))
                    diff_html = ""
                    for i in range(max_len):
                        c_sent = msg_sent[i] if i < len(msg_sent) else '∅'
                        c_recv = msg_received[i] if i < len(msg_received) else '∅'
                        if c_sent != c_recv:
                            diff_html += f"Position {i}: `{c_sent}` → `{c_recv}` ❌\n\n"
                    if diff_html:
                        st.markdown(diff_html)

        # Export option
        st.markdown("---")
        if st.button("📥 Export to CSV"):
            csv_data = pd.DataFrame([{
                'mission_id': m[0],
                'message_sent': m[2],
                'message_received': m[3],
                'ber': m[4],
                'distance_km': m[5],
                'snr_db': m[6],
                'timestamp': m[7]
            } for m in filtered_missions])

            csv_str = csv_data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv_str,
                file_name="mission_archive.csv",
                mime="text/csv"
            )

        # Clear database option
        st.markdown("---")
        st.warning("⚠️ **Danger Zone**")
        if st.button("🗑️ Clear All Mission Data", type="secondary"):
            if st.checkbox("I confirm I want to delete all missions"):
                clear_database(db_path)
                st.success("✅ Database cleared!")
                st.rerun()

    else:
        st.info("No missions match your filter criteria. Try adjusting the filters.")

else:
    st.info("""
    ### No Missions Yet!

    The mission archive is empty. To populate it:
    1. Use the **Downlink Console** to send messages
    2. Implement save_mission() calls in your communication pipeline
    3. Data will automatically be saved to SQLite

    **Database Location:** `{db_path}`
    """)

    # Demo: Add sample missions button
    if st.button("➕ Add Sample Missions", type="primary"):
        import random
        import time as pytime

        for i in range(10):
            snr = random.uniform(5, 25)
            ber = random.uniform(0.0001, 0.1)
            messages = ["Hello World", "Test Message", "Satellite Link", "Ground Control", "Mission Data"]
            msg = random.choice(messages)
            # Simulate errors based on BER
            corrupted = ""
            for c in msg:
                if random.random() < ber:
                    corrupted += chr(random.randint(65, 90))
                else:
                    corrupted += c

            save_mission(
                message_sent=msg,
                message_received=corrupted,
                ber=ber,
                snr_db=snr,
                distance_km=random.uniform(300, 1500),
                db_path=db_path
            )

        st.success("✅ Added 10 sample missions!")
        st.rerun()

st.markdown("""
---

### 🎓 Understanding Mission Archives

**Why Archive Data?**
- **Analysis:** Study performance trends over time
- **Debugging:** Investigate failures
- **Reporting:** Generate mission summaries
- **Learning:** Compare different scenarios
- **Research:** Build datasets for ML/analysis

**SQLite Database:**
- Lightweight, embedded database
- No server needed
- Perfect for small to medium datasets
- Easy to query with SQL

**Typical Queries:**
- "Show me all missions with BER > 5%"
- "Find the best SNR achieved"
- "List all failed transmissions"
- "Calculate average performance by month"

**Try This:**
1. Generate sample missions (button above if empty)
2. Filter by SNR or BER
3. View performance charts
4. Inspect individual mission details
5. Export data for external analysis

---

**➡️ Next:** Read the **Engineering Legacy** reference guide

""")

st.success("✅ **Interactive Demo Active:** Browse and analyze archived mission data!")

st.divider()
st.caption("Chapter 9: Mission Archive | Phase 4: Fully Interactive Learning Console")
