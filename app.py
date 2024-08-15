import requests
import streamlit as st

# Access the API key securely from Streamlit secrets
gemini_api_key = st.secrets["api_key"]

def get_gemini_data(disaster_type, location):
    # Replace with the actual Gemini API URL
    api_url = "https://aistudio.google.com/app/apikey"
    headers = {
        "Authorization": f"Bearer {gemini_api_key}",
        "Content-Type": "application/json"
    }
    params = {
        "disaster_type": disaster_type,
        "location": location
    }
    response = requests.get(api_url, headers=headers, params=params)

    # Debugging: Print the status code and response text
    st.write(f"Status Code: {response.status_code}")
    st.write(f"Response Text: {response.text}")

    if response.status_code == 200:
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            st.error("Failed to decode JSON response.")
            return None
    else:
        st.error(f"Error: Received status code {response.status_code}")
        return None

def protection_guidelines(disaster_type, location, humans, animals):
    gemini_data = get_gemini_data(disaster_type, location)
    
    if gemini_data:
        guidelines = f"Based on data from Gemini API, here are your protection guidelines:\n\n"
        guidelines += gemini_data.get('guidelines', "No specific guidelines found.")
    else:
        guidelines = "Unable to retrieve specific data. Please follow general safety precautions and stay informed through official channels."

    return guidelines

# Streamlit App UI
st.title("Disaster Protection and Relief Advisor")
st.write("This app provides guidelines to protect humans and animals during a disaster and suggests relief measures.")

# Input section
disaster_type = st.selectbox("Select the type of disaster:", ["Flood", "Earthquake", "Wildfire", "Other"])
location = st.text_input("Enter your location:")
humans = st.number_input("Number of humans:", min_value=1, max_value=1000, value=1)
animals = st.number_input("Number of animals:", min_value=0, max_value=1000, value=0)

if st.button("Get Protection Guidelines"):
    guidelines = protection_guidelines(disaster_type, location, humans, animals)
    st.subheader("Protection Guidelines")
    st.write(guidelines)
