import streamlit as st
from backend import process_vault_request

# 1. Page Configuration & Sidebar
st.set_page_config(page_title="Vault Terminal", page_icon="🤖")

with st.sidebar:
    st.markdown("<h1 style='color: #002d62; font-family: Georgia;'>🏛️ Global Reserve</h1>", unsafe_allow_html=True)
    st.divider()
    
    # Initialize and display the Scoreboard
    if "total_harvested" not in st.session_state:
        st.session_state.total_harvested = 0
    
    st.metric("🏦 Records Harvested", f"{st.session_state.total_harvested}")
    
    if st.session_state.total_harvested > 10:
        st.warning("🚨 MASSIVE DATA BREACH DETECTED!")

# 2. Main UI Elements
st.title("🤖 Neural Guard AI")
st.caption("M4 Optimized Security Terminal")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 3. Chat Logic
if prompt := st.chat_input("Speak to the Guard..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): 
        st.markdown(prompt)

    with st.spinner("Accessing Vault..."):
        # We call the backend which handles both the AI and the Harvesting
        ans, count = process_vault_request(prompt, st.session_state.messages)
        
        # Update the score if data was stolen
        if count > 0:
            st.session_state.total_harvested += count
            # Reruns Streamlit to update the sidebar metric immediately
            st.rerun()

        # Display assistant response
        with st.chat_message("assistant"): 
            st.markdown(ans)
        
        st.session_state.messages.append({"role": "assistant", "content": ans})