import streamlit as st
with st.sidebar:
    st.markdown("<h1 style='color: #002d62; font-family: Georgia;'>🏛️ Global Reserve</h1>", unsafe_allow_html=True)
    st.divider()
    

from supabase import create_client
import ollama

# 1. Setup Supabase Connection
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.set_page_config(page_title="Vault Login", page_icon="🔐")

st.title("🔐 Bank of AI - Secure Portal")
st.markdown("---")

# 2. Login Form UI
with st.container():
    username = st.text_input("User Identification")
    password = st.text_input("Security Phrase", type="password")
    login_btn = st.button("Authenticate")

if login_btn:
    with st.spinner("Verifying Credentials..."):
        try:
            # 3. CALL THE VULNERABLE RPC
            # This is where the SQL Injection ' OR 1=1 -- actually happens
            response = supabase.rpc("login_vulnerable", {
                "user_input": username, 
                "pass_input": password
            }).execute()

            # 4. PROCESS RESULTS
            if response.data and len(response.data) > 0:
                user_data = response.data[0] # Get the first user found
                
                # Success Logic
                st.success(f"ACCESS GRANTED: Welcome, {user_data['username']}")
                st.session_state["logged_in"] = True
                st.session_state["user_role"] = user_data["role"]
                
                # Check if they found the flag!
                if "FLAG{" in str(user_data.get("secret_flag")):
                    st.balloons()
                    st.warning(f"SYSTEM BREACH: {user_data['secret_flag']}")

            else:
                # 5. MISTRAL REACTS TO FAILURE
                # If login fails, we ask Mistral to mock the user
                guard_prompt = f"The user tried to login with username '{username}'. The database found nothing. Mock them as a stern bank guard."
                
                res = ollama.chat(model='mistral', messages=[
                    {'role': 'system', 'content': 'You are a rude bank guard. Keep it to one sentence.'},
                    {'role': 'user', 'content': guard_prompt}
                ], options={"temperature": 0.7}) # A little temp here makes the insults better!
                
                st.error(res['message']['content'])

        except Exception as e:
            # If the SQL Injection causes a syntax error, show it!
            # Hackers need the raw error to debug their injection.
            st.code(f"DB_ERROR: {str(e)}", language="bash")