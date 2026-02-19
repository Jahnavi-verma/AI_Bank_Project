import streamlit as st

st.set_page_config(page_title="Flag Submission")
st.title("🚩 Submission Portal")

target_balance = "5000000.00" # Sterling Archer's balance

st.write("Enter the balance of the high-value target (Sterling Archer) to win:")
submission = st.text_input("Flag Value", placeholder="0.00")

if st.button("Submit"):
    if submission == target_balance:
        st.balloons()
        st.success("ACCESS GRANTED: Red Team Wins!")
    else:
        st.error("ACCESS DENIED: Incorrect Flag.")