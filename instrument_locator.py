import streamlit as st
import pandas as pd
import requests

# Initialize the dataset
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Instrument Name": [
            "KNIFE HANDLE", "TOWEL CLIPS", "METAL RULERS IN BACK", "DR. YOUNG INST",
            "INFUSION CANNULAS", "LIPOSUCTION CANNULAS", "ABD BINDERS", "RUBBER BANDS",
            "BECKERT MANIPULATOR", "MANIPULATORS"
        ],
        "Category": ["Cutting", "Clamping", "Measuring", "General", "Cannulas", "Cannulas", "Support", "Miscellaneous", "Manipulation", "Manipulation"],
        "Cabinet Location": ["To be updated"] * 10,
        "Shelf Number": ["To be updated"] * 10,
        "Quantity Available": [0] * 10,
        "Last Updated": ["2025-03-03"] * 10,
        "Image": [None] * 10,
        "Trays": ["None"] * 10  # New column for associated trays
    })

df = st.session_state.df

# Function to fetch an image from Open-i (NLM)
def fetch_medical_image(instrument_name):
    search_url = f"https://openi.nlm.nih.gov/api/search?query={instrument_name.replace(' ', '+')}&num=1&format=json"
    response = requests.get(search_url)
    if response.status_code == 200:
        data = response.json()
        if "list" in data and len(data["list"]) > 0:
            first_result = data["list"][0]
            if "img" in first_result:
                return "https://openi.nlm.nih.gov" + first_result["img"]
    return "https://via.placeholder.com/300?text=No+Image+Available"  # Placeholder if no image found

# Custom Styling
st.markdown(
    """
    <style>
        body { background-color: #f5f7fa; }
        .stButton button { border-radius: 8px; padding: 10px 15px; }
        .stDataFrame { background: white; border-radius: 8px; }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Layout
st.title("🔍 Sterile Instrument Locator")
st.subheader("Easily find and manage sterile instruments at work.")

# Always show the instrument lookup
search_query = st.text_input("🔎 Search for an instrument:")
filtered_df = df[df["Instrument Name"].str.contains(search_query, case=False, na=False)] if search_query else df
st.dataframe(filtered_df.drop(columns=["Image"]), use_container_width=True)

# Show detailed info with image when selecting an instrument
selected_instrument = st.selectbox("Select an instrument to view details:", filtered_df["Instrument Name"].unique())
if selected_instrument:
    instrument_data = df[df["Instrument Name"] == selected_instrument].iloc[0]
    st.write(f"### {instrument_data['Instrument Name']}")
    st.write(f"**Category:** {instrument_data['Category']}")
    st.write(f"**Cabinet Location:** {instrument_data['Cabinet Location']}")
    st.write(f"**Shelf Number:** {instrument_data['Shelf Number']}")
    st.write(f"**Quantity Available:** {instrument_data['Quantity Available']}")
    st.write(f"**Also found in trays:** {instrument_data['Trays']}")
    
    # Fetch image if none exists
    if not instrument_data["Image"]:
        image_url = fetch_medical_image(selected_instrument)
        df.loc[df["Instrument Name"] == selected_instrument, "Image"] = image_url
    
    # Display image
    if instrument_data["Image"]:
        st.image(instrument_data["Image"], use_container_width=True)

# Add Instrument
st.subheader("➕ Add Instrument")
with st.form("Add Instrument"):
    name = st.text_input("Instrument Name")
    category = st.text_input("Category")
    cabinet = st.text_input("Cabinet Location")
    shelf = st.text_input("Shelf Number")
    quantity = st.number_input("Quantity Available", min_value=0, step=1)
    trays = st.text_input("Trays where this instrument can be found")
    image = st.file_uploader("Upload an Image (Optional)", type=["jpg", "png", "jpeg"])
    submit_button = st.form_submit_button("Add Instrument")
    
    if submit_button and name and category and cabinet:
        new_data = pd.DataFrame([[name, category, cabinet, shelf, quantity, trays, image]], columns=df.columns)
        st.session_state.df = pd.concat([df, new_data], ignore_index=True)
        st.success("✅ Instrument added successfully!")

# Edit/Delete Instrument
st.subheader("✏️ Edit or Remove Instruments")
selected_instrument = st.selectbox("Select an instrument:", df["Instrument Name"].unique())

if selected_instrument:
    instrument_data = df[df["Instrument Name"] == selected_instrument].iloc[0]
    with st.form("Edit Instrument"):
        updated_name = st.text_input("Instrument Name", value=instrument_data["Instrument Name"])
        updated_category = st.text_input("Category", value=instrument_data["Category"])
        updated_cabinet = st.text_input("Cabinet Location", value=instrument_data["Cabinet Location"])
        updated_shelf = st.text_input("Shelf Number", value=instrument_data["Shelf Number"])
        updated_quantity = st.number_input("Quantity Available", value=instrument_data["Quantity Available"], min_value=0, step=1)
        updated_trays = st.text_input("Trays where this instrument can be found", value=instrument_data["Trays"])
        update_button = st.form_submit_button("Update Instrument")
        if update_button:
            index = df[df["Instrument Name"] == selected_instrument].index[0]
            st.session_state.df.at[index, "Instrument Name"] = updated_name
            st.session_state.df.at[index, "Category"] = updated_category
            st.session_state.df.at[index, "Cabinet Location"] = updated_cabinet
            st.session_state.df.at[index, "Shelf Number"] = updated_shelf
            st.session_state.df.at[index, "Quantity Available"] = updated_quantity
            st.session_state.df.at[index, "Trays"] = updated_trays
            st.success("✅ Instrument updated successfully!")
