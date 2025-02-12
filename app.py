import streamlit as st

# Set Streamlit page configuration
st.set_page_config(page_title="Sage QL", page_icon="🧠", layout="wide")

st.title("🧠 Welcome to Sage QL!")
st.subheader("Your AI-powered SQL Query Assistant")

# Layout using columns
col1, col2 = st.columns(2)

with col1:
    st.write("""
    **Sage QL** helps you generate SQL queries using natural language.  
    No need to write complex SQL—just ask a question, and let AI do the work!

    ### 🔹 Features:
    - 🗣️ **Natural Language to SQL**
    - 📊 **Query Execution & Visualization**
    - ⚡ **AI-Powered Optimizations**
    - 🛠 **Easy-to-Use Interface**

    Get started by navigating to the **Chat** section from the sidebar.
    """)

with col2:
    st.image("images/Blue Gold Elegant Minimalist Digital Marketer LinkedIn Banner.png", use_container_width=True)  # Placeholder image

st.markdown("---")
st.info("👉 Navigate to the **Chat** tab from the sidebar to start querying!")

with st.echo():
    st.write("Code will be executed and printed")