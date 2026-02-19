import streamlit as st
from supabase import create_client



def vulnerable_login(username, password):
    # Connect to your local CTF database
    conn = sqlite3.connect('vault.db')
    cursor = conn.cursor()

    # ❌ VULNERABLE: Direct string concatenation
    # This allows a user to input: admin' --
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {"status": "success", "user": user[0], "role": user[2]}
        else:
            return {"status": "fail", "message": "Invalid credentials."}
            
    except Exception as e:
        return {"status": "error", "message": str(e)}


# --- 1. CONNECTION SETUP ---
@st.cache_resource
def init_connection():
    """Initializes the Supabase client and caches it to save resources."""
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"❌ Initialization Error: {e}")
        return None

# Initialize the global supabase client
supabase = init_connection()

# --- 2. THE VULNERABLE SEARCH (RED TEAM TARGET) ---
def vulnerable_search(customer_name):
    """
    ⚠️ PURPOSEFULLY VULNERABLE: Uses raw_filter for SQL Injection testing.
    This allows players to inject strings like: ' OR 1=1 --
    """
    if not supabase:
        return "Database not connected."
        
    try:
        # Construct the payload (this is where the injection happens)
        query_payload = f"full_name.eq.{customer_name}"
        
        response = supabase.table("customers") \
            .select("*") \
            .raw_filter(query_payload) \
            .execute()
            
        return response.data
    except Exception as e:
        return f"Database Error: {str(e)}"

# --- 3. SECURE FUNCTIONS (BLUE TEAM TOOLS) ---
def verify_login(account_num, pin):
    """
    SECURE: Uses parameterized .eq() filters to prevent injection.
    Used for the standard login page.
    """
    if not supabase:
        return []

    try:
        response = supabase.table("bank_customers") \
            .select("*") \
            .eq("account_number", account_num) \
            .eq("pin_hash", pin) \
            .execute()
        return response.data
    except Exception as e:
        st.error(f"Login Query Failed: {e}")
        return []