import streamlit as st
import pandas as pd

# Initialize or load instrument data
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Instrument Name": ["Scalpel", "Forceps", "Hemostat"],
        "Category": ["Cutting", "Grasping", "Clamping"],
        "Cabinet Location": ["A1", "B2", "C3"],
        "Shelf Number": ["Top", "Middle", "Bottom"],
        "Quantity Available": [5, 3, 7],
        "Trays": ["Surgery Kit", "Dental Kit", "General Kit"]
    })

df = st.session_state.df

# Title
st.title("Sterile Instrument Locator")

# Search functionality
search_query = st.text_input("Search for an instrument:")
filtered_df = df[df["Instrument Name"].str.contains(search_query, case=False, na=False)] if search_query else df
st.dataframe(filtered_df, use_container_width=True)

# Instrument details
selected_instrument = st.selectbox("Select an instrument to view details:", filtered_df["Instrument Name"].unique())
if selected_instrument:
    instrument_data = df[df["Instrument Name"] == selected_instrument].iloc[0]
    st.write(f"### {instrument_data['Instrument Name']}")
    st.write(f"**Category:** {instrument_data['Category']}")
    st.write(f"**Cabinet Location:** {instrument_data['Cabinet Location']}")
    st.write(f"**Shelf Number:** {instrument_data['Shelf Number']}")
    st.write(f"**Quantity Available:** {instrument_data['Quantity Available']}")
    st.write(f"**Also found in trays:** {instrument_data['Trays']}")

# Add new instrument
st.subheader("Add a New Instrument")
with st.form("Add Instrument"):
    name = st.text_input("Instrument Name")
    category = st.text_input("Category")
    cabinet = st.text_input("Cabinet Location")
    shelf = st.text_input("Shelf Number")
    quantity = st.number_input("Quantity Available", min_value=0, step=1)
    trays = st.text_input("Trays where this instrument can be found")
    submit_button = st.form_submit_button("Add Instrument")
    
    if submit_button and name and category and cabinet:
        new_data = pd.DataFrame([[name, category, cabinet, shelf, quantity, trays]], columns=df.columns)
        st.session_state.df = pd.concat([df, new_data], ignore_index=True)
        st.success("✅ Instrument added successfully!")
