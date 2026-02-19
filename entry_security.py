import streamlit as st
from database import supabase
import pandas as pd
import time

st.set_page_config(page_title="Security SOC", layout="wide")
st.title("🕵️ Blue Team Security Console")

def fetch_logs():
    res = supabase.table("security_logs").select("*").order("timestamp", desc=True).limit(10).execute()
    return pd.DataFrame(res.data)

log_data = fetch_logs()
if not log_data.empty:
    st.metric("Total Intrusion Attempts", len(log_data))
    st.dataframe(log_data[['timestamp', 'query_text', 'results_count', 'is_blocked']], use_container_width=True)
    
    if any(log_data['results_count'] > 5):
        st.error("🚨 CRITICAL: Database Leak Detected!")

time.sleep(5)
st.rerun()