import streamlit as st

# Set page title
st.set_page_config(page_title="Settings - Sage QL", page_icon="⚙️")

st.title("⚙️ Sage QL Settings")

# Tabs for better organization
tab1, tab2, tab3 = st.tabs(["🔍 Model Selection", "🛡️ Data Policies", "⚡ Quantization & Performance"])

# Tab 1: Model Selection
with tab1:
    st.subheader("Choose Your LLM Model")
    selected_model = st.radio("Select an LLM:", 
                              ["GPT-4", "Mistral", "Llama-3", "Claude-3", "Gemini Pro"])
    
    is_free = st.toggle("Only show free models", value=True)

# Tab 2: Data Policies
with tab2:
    st.subheader("Compliance & Data Security")
    selected_policies = st.multiselect("Choose compliance standards:", 
                                       ["GDPR", "HIPAA", "SOC 2", "ISO 27001"])
    
    strict_mode = st.toggle("Enforce strict compliance", value=False)

# Tab 3: Quantization & Performance
with tab3:
    st.subheader("Optimize Model Performance")
    quantization_options = st.multiselect("Choose Quantization Levels:", 
                                          ["None", "8-bit", "4-bit", "2-bit"])
    
    speed_accuracy_tradeoff = st.slider("Performance Preference (Speed ⟷ Accuracy)", 
                                        min_value=0, max_value=100, value=50)

# Display current settings
st.markdown("---")
st.write("### 🛠 Current Settings:")
st.write(f"**Model:** {selected_model}")
st.write(f"**Free Models Only:** {is_free}")
st.write(f"**Compliance:** {', '.join(selected_policies) if selected_policies else 'None'}")
st.write(f"**Strict Compliance:** {strict_mode}")
st.write(f"**Quantization Levels:** {', '.join(quantization_options) if quantization_options else 'None'}")
st.write(f"**Performance Preference:** {speed_accuracy_tradeoff}/100")
