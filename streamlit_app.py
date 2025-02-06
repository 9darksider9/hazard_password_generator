import streamlit as st
import requests

st.set_page_config(page_title="Password Generator", page_icon="🔐", layout="centered")

st.title("🔐 Secure Password & Passphrase Generator")

API_BASE_URL = "http://localhost:8000"

# ✅ Removed the OAuth token input
st.warning("⚠️ This app no longer requires authentication.")

# ✅ Password Generator Section
st.header("🔑 Generate a Secure Password")
password_length = st.slider("Password Length", min_value=6, max_value=64, value=12)
use_uppercase = st.checkbox("Include Uppercase Letters")
use_lowercase = st.checkbox("Include Lowercase Letters", value=True)
use_numbers = st.checkbox("Include Numbers")
use_specials = st.checkbox("Include Special Characters")

if st.button("Generate Password"):
    response = requests.post(f"{API_BASE_URL}/generate_password", json={
        "length": password_length,
        "use_uppercase": use_uppercase,
        "use_lowercase": use_lowercase,
        "use_numbers": use_numbers,
        "use_specials": use_specials
    })
    if response.status_code == 200:
        generated_password = response.json()['password']
        st.success("🔒 Your Secure Password:")
        st.code(generated_password, language="")
    else:
        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

# ✅ Passphrase Generator Section
st.header("🔐 Generate a Secure Passphrase")
use_passphrase = st.checkbox("Generate a Passphrase Instead")
num_words = st.slider("Number of Words", min_value=2, max_value=10, value=4)

if use_passphrase and st.button("Generate Passphrase"):
    response = requests.post(f"{API_BASE_URL}/generate_passphrase", json={"num_words": num_words})
    if response.status_code == 200:
        generated_passphrase = response.json()['passphrase']
        st.success("🔒 Your Secure Passphrase:")
        st.code(generated_passphrase, language="")
    else:
        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")