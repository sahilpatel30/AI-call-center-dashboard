import streamlit as st
import pandas as pd
import json
from twilio_utils import fetch_call_logs, fetch_call_recordings
import plotly.express as px


# ------------------ Page Setup ------------------
st.set_page_config(page_title="AI Call Center Dashboard", layout="wide")

# ------------------ Custom CSS ------------------
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stApp {
        background-color: #0e1117;
    }
    h1, h2, h3, h4 {
        color: #F0F0F0;
        font-family: 'Segoe UI', sans-serif;
    }
    .block-container {
        padding: 2rem 3rem;
    }
    .card {
        background-color: #1c1f26;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 0 10px rgba(0,0,0,0.2);
    }
    .metric-title {
        font-size: 1rem;
        color: #A0A0A0;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #FFFFFF;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ Load Agents ------------------
try:
    with open("agents.json", "r") as f:
        agents = json.load(f)
except Exception as e:
    st.error(f"Error loading agents.json: {e}")
    agents = []

# ------------------ Fetch Twilio Data ------------------
try:
    calls = fetch_call_logs()
except Exception as e:
    st.error(f"Error fetching call logs: {e}")
    calls = []

try:
    recordings = fetch_call_recordings()
except Exception as e:
    st.error(f"Error fetching recordings: {e}")
    recordings = []

# ------------------ Metrics ------------------
total_calls = len(calls)
active_agents = len([a for a in agents if a["status"].lower() == "busy"])
available_agents = len([a for a in agents if a["status"].lower() == "available"])

# ------------------ Title ------------------
st.markdown("<h1 style='text-align:center;'>📞 AI Call Center Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Monitor agents, live calls, and recordings</p>", unsafe_allow_html=True)
st.markdown("<hr style='margin:1.5rem 0; border: 1px solid #333;'>", unsafe_allow_html=True)

# ------------------ Summary Cards ------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='card'><div class='metric-title'>Total Calls</div><div class='metric-value'>{}</div></div>".format(total_calls), unsafe_allow_html=True)
with col2:
    st.markdown("<div class='card'><div class='metric-title'>Active Agents</div><div class='metric-value'>{}</div></div>".format(active_agents), unsafe_allow_html=True)
with col3:
    st.markdown("<div class='card'><div class='metric-title'>Available Agents</div><div class='metric-value'>{}</div></div>".format(available_agents), unsafe_allow_html=True)

# ------------------ Agent Pool ------------------
st.markdown("<h3>👨‍💻 Agent Pool</h3>", unsafe_allow_html=True)
if agents:
    df_agents = pd.DataFrame(agents)
    df_agents = df_agents.rename(columns={"name": "Agent", "phone": "Phone", "status": "Status"})
    st.dataframe(df_agents.style.set_properties(**{
        'background-color': '#1c1f26',
        'color': '#ffffff',
        'border-color': '#444'
    }), use_container_width=True)
else:
    st.warning("No agent data available.")

# ------------------ Call Logs ------------------
st.markdown("<h3 style='margin-top:2rem;'>📞 Recent Call Logs</h3>", unsafe_allow_html=True)
if calls:
    df_calls = pd.DataFrame(calls)
    df_calls.columns = ["Caller", "Phone", "Date/Time", "Duration", "Status"]
    st.dataframe(df_calls.style.set_properties(**{
        'background-color': '#1c1f26',
        'color': '#ffffff',
        'border-color': '#444'
    }), use_container_width=True)
else:
    st.info("No recent call logs found.")





# ------------------ Recordings ------------------
st.markdown("<h3 style='margin-top:2rem;'>🎧 Call Recordings</h3>", unsafe_allow_html=True)
if recordings:
    for r in recordings:
        with st.container():
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"<div style='color:#ccc;'><b>{r['caller']}</b> — {r['date']} — ⏱️ {r['duration']}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<a href='{r['url']}' target='_blank' style='color:#4ecdc4;'>▶️ Play</a>", unsafe_allow_html=True)
else:
    st.info("No recent recordings found.")

# ------------------ Agent Status Bar Chart (Dark Styled) ------------------
st.markdown("<h3 style='margin-top:2rem;'>📊 Agent Availability</h3>", unsafe_allow_html=True)

try:
    if agents:
        df_status = pd.DataFrame(agents)
        status_count = df_status['status'].str.capitalize().value_counts().reset_index()
        status_count.columns = ['Status', 'Count']

        fig = px.bar(
            status_count,
            x='Status',
            y='Count',
            color='Status',
            color_discrete_map={
                'Available': '#4ecdc4',
                'Busy': '#ff6b6b'
            },
            text='Count',
            template='plotly_dark',
            title=None
        )
        fig.update_layout(
            showlegend=False,
            margin=dict(l=10, r=10, t=30, b=30),
            plot_bgcolor='#1c1f26',
            paper_bgcolor='#1c1f26'
        )
        fig.update_traces(marker_line_width=1.5, marker_line_color='rgba(255,255,255,0.2)', textposition='outside')

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No agent data available to plot.")
except Exception as e:
    st.warning(f"Agent bar chart error: {e}")

