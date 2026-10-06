import streamlit as st
import requests
import pandas as pd
import json

API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI-231 Executive Dashboard", layout="wide", page_icon="🌐")

st.title("Enterprise Autonomous Infrastructure Intelligence")
st.markdown("### Critical Operations Platform (AI-231)")

tab1, tab2, tab3, tab4 = st.tabs(["Infrastructure Health", "Predictive Analytics", "AI Copilot", "Alert Center"])

with tab1:
    st.header("Asset Registry & Real-Time Health")
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Refresh Infrastructure State"):
            try:
                res = requests.get(f"{API_URL}/assets/")
                if res.status_code == 200:
                    assets = res.json()
                    df = pd.DataFrame(assets)
                    if not df.empty:
                        st.dataframe(df.style.highlight_between(subset=['health_score'], left=0, right=50, color='red'))
                    else:
                        st.write("No active infrastructure found.")
            except Exception as e:
                st.error(f"Failed to connect to API: {e}")
    with col2:
        st.metric("Total Monitored Assets", "100")
        st.metric("Global Health Average", "94.2%")

with tab2:
    st.header("Predictive Operations & Root Cause Analysis")
    st.markdown("**Simulate an Anomaly Analysis:**")
    failed_asset = st.text_input("Enter Failed Asset ID (e.g., asset-0042):", "asset-0042")
    if st.button("Run Diagnostics & Self-Healing Workflow"):
        st.info("Executing Graph Traversal (Neo4j) & Heuristics...")
        # In a real app, this hits the backend RCA API. Mocking visual for Streamlit:
        st.error(f"Primary Failure Identified: {failed_asset}")
        st.warning(f"Root Cause Candidates: Upstream Power Station (asset-0012)")
        st.success("Self-Healing Action Triggered: Traffic rerouted to Backup Grid.")

with tab3:
    st.header("AI Operations Copilot")
    st.markdown("*Powered by LangChain & LlamaIndex*")
    query = st.text_input("Query Infrastructure Knowledge Graph:")
    if st.button("Ask Copilot"):
        with st.spinner("AI is thinking..."):
            try:
                res = requests.post(f"{API_URL}/copilot/chat", json={"query": query})
                if res.status_code == 200:
                    data = res.json()
                    st.info(data['answer'])
                    st.write(f"**Explainable AI Confidence:** {data['confidence'] * 100:.1f}%")
                    st.markdown("**Root Cause Evidence:**")
                    for ev in data['evidence']:
                        st.write(f"- 🔎 {ev}")
            except Exception as e:
                st.error(f"API Error: {e}")

with tab4:
    st.header("Alert Center")
    st.error("🚨 CRITICAL: Data Center Alpha (asset-0001) temperature exceeded 105C.")
    st.warning("⚠️ WARNING: Telecom Tower 4 capacity predicted to exhaust in 14 hours.")
    st.success("✅ RESOLVED: Network routing switch restored by Autonomous Coordinator.")
