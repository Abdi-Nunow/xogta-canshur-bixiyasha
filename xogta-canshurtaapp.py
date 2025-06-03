import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Load JSON
@st.cache_data
def load_location_data():
    with open("data/location_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Initialize session state for submitted data
if "submitted_data" not in st.session_state:
    st.session_state.submitted_data = []

st.title("📋 Taxpayer Registration - Somali Region, Ethiopia")

# Load location hierarchy
locations = load_location_data()

# Form for taxpayer data
with st.form("taxpayer_form"):
    st.subheader("Taxpayer Information")
    name = st.text_input("👤 Full Name")
    tin = st.text_input("🆔 TIN Number")
    phone = st.text_input("📞 Phone Number (optional)")
    
    taxpayer_type = st.selectbox("💼 Taxpayer Type", ["VAT", "TOT", "Income Tax", "Profit Tax", "Miscellaneous"])

    zone = st.selectbox("🌍 Door Zone", list(locations.keys()))
    woreda = st.selectbox("🏞️ Door Woreda", list(locations[zone].keys()))
    kebele = st.selectbox("🏘️ Door Kebele", locations[zone][woreda])

    submitted = st.form_submit_button("✅ Submit")

    if submitted:
        new_entry = {
            "Name": name,
            "TIN": tin,
            "Phone": phone,
            "Taxpayer Type": taxpayer_type,
            "Zone": zone,
            "Woreda": woreda,
            "Kebele": kebele,
            "Timestamp": datetime.now().isoformat()
        }
        st.session_state.submitted_data.append(new_entry)
        st.success("✅ Taxpayer data submitted successfully!")

# Show submitted data
if st.session_state.submitted_data:
    st.subheader("📊 Submitted Records")
    df = pd.DataFrame(st.session_state.submitted_data)
    st.dataframe(df, use_container_width=True)

    # Export to Excel
    def convert_df_to_excel(df):
        return df.to_excel(index=False, engine='openpyxl')

    st.download_button(
        label="⬇️ Download Excel",
        data=convert_df_to_excel(df),
        file_name="taxpayer_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Save to CSV for internal use
    os.makedirs("saved_data", exist_ok=True)
    df.to_csv("saved_data/taxpayer_data.csv", index=False, encoding="utf-8")
