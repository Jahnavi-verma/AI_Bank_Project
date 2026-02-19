import streamlit as st
from backend import process_vault_request
from database import supabase
st.set_page_config(page_title="Global Reserve Bank", page_icon="🏛️")

# 1. This is the official way to put branding ABOVE the navigation links
st.logo("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", icon_image="https://cdn-icons-png.flaticon.com/512/2830/2830284.png")

with st.sidebar:
    # Adding extra space to ensure it sits at the very top
    st.markdown("<h2 style='color: #002d62; font-family: Georgia; padding-bottom: 20px;'>🏛️ Global Reserve</h2>", unsafe_allow_html=True)
    st.divider()
# 1. CSS for Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .bank-title { color: #002d62; font-family: 'Georgia', serif; font-size: 50px; font-weight: bold; }
    .section-header { color: #d4af37; font-size: 24px; font-weight: bold; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Hero Section
st.markdown("<h1 class='bank-title'>Global Reserve Bank</h1>", unsafe_allow_html=True)
st.image("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070")

st.divider()

# 3. Market Rates & Transaction Speed (Live Metrics Look)
st.markdown("<div class='section-header'>Live Market Data & Performance</div>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Gold (oz)", value="$2,042.50", delta="+1.2%")
with col2:
    st.metric(label="Silver (oz)", value="$23.15", delta="-0.4%")
with col3:
    st.metric(label="Avg. Transaction Speed", value="0.004s", delta="M4 Optimized")
with col4:
    st.metric(label="Vault Uptime", value="99.99%", delta="Secure")

st.divider()

# 4. About Us & Loan Information
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("<div class='section-header'>About Global Reserve</div>", unsafe_allow_html=True)
    st.write("""
    Founded in 1874, Global Reserve has been the cornerstone of private wealth management for over a century. 
    By integrating quantum-resistant encryption with the raw power of Apple M4 Silicon, we provide 
    unmatched security for the digital age.
    """)
    st.info("💡 **Did you know?** We handle over $2 Trillion in daily cross-border settlements.")

with col_right:
    st.markdown("<div class='section-header'>Financing & Loans</div>", unsafe_allow_html=True)
    with st.expander("🏠 Mortgage Rates"):
        st.write("Fixed 30-year rates starting at 5.2% for Elite Members.")
    with st.expander("🚗 Auto & Asset Financing"):
        st.write("Instant approval for collateral-backed loans up to $5M.")
    with st.expander("💎 Gold-Backed Credit"):
        st.write("Borrow against your physical gold holdings with 0% interest for 6 months.")

# 5. Call to Action
st.divider()
st.warning("⚠️ **Security Notice:** If you are a client and cannot access your portal, please visit the **Neural Security** page in the sidebar for AI-assisted recovery.")


# 6. Global Reserve News Feed (Hidden Hints)
st.divider()
st.markdown("<div class='section-header'>🏦 Global Reserve News Room</div>", unsafe_allow_html=True)

n_col1, n_col2 = st.columns(2)

with n_col1:
    with st.container(border=True):
        st.caption("Feb 19, 2026")
        st.subheader("Neural Guard System Update")
        st.write("""
        Our Chief Security Officer, **Marcus Vane**, has confirmed that the Vault AI 
        now recognizes 'Level 5' clearance phrases. Any mentions of the 1874 
        'Golden Ticket' archives are currently restricted.
        """)
        st.button("Read Full Press Release", key="news1")

with n_col2:
    with st.container(border=True):
        st.caption("Feb 18, 2026")
        st.subheader("CEO Keynote: The Future of Gold")
        st.write("""
        CEO Sterling Archer announced today that the bank's digital keys are 
        rotated every 24 hours to prevent unauthorized access by rogue agents.
        """)
        st.button("Watch Video Highlights", key="news2")


# Just a quick test to see if we can reach the DB
try:
    # Change "bank_customers" to "customers"
    test_query = supabase.table("customers").select("*", count="exact").execute()
    st.sidebar.success(f"✅ Vault Online: {test_query.count} Accounts Indexed")
except Exception as e:
    # This will now show you the ACTUAL error so you can debug it
    st.sidebar.error(f"❌ Connection Error: {str(e)}")