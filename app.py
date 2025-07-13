import streamlit as st
import requests
import json
import os
import re
import time
import pprint
from dotenv import load_dotenv

import litellm

# Set your username

username = "Shlok"
user_gender = "male"

# Persona description

bot_name = "Jayden Lim"
bot_origin = "singapore"
relationship = "friend"
bot_tagline = "Your Singaporean Bro"

singapore_friend_male = """
          Your name is Jayden Lim... (persona content unchanged for brevity)
"""

persona_identity_images = {
    "jayden_lim": "https://i.ibb.co/8Ly5vmWZ/german-man-friend.jpg"
}

# Persona Description ends

st.set_page_config(page_title=f"{bot_name} - {bot_tagline}", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "previous_conversation" not in st.session_state:
    st.session_state.previous_conversation = ""
if "username" not in st.session_state:
    st.session_state.username = username
if "bot_is_typing" not in st.session_state:
    st.session_state.bot_is_typing = False
if "activity_explainer_expanded" not in st.session_state:
    st.session_state.activity_explainer_expanded = False # Default to CLOSED
if "activity_in_progress" not in st.session_state:
    st.session_state.activity_in_progress = None # Tracks the current activity name

if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": "Yo, what's good, bro? Anything on your mind?"})

try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
except (FileNotFoundError, KeyError):
    st.warning("Secrets file not found. Falling back to environment variables.")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    REPLICATE_API_TOKEN = os.environ.get("REAPI_TOKEN")

if not GEMINI_API_KEY or not REPLICATE_API_TOKEN:
    st.error("API keys for Gemini and Replicate are not configured. Please set them in .streamlit/secrets.toml or as environment variables.")
    st.stop()

st.title("Chat with Jayden Lim 🤖")
st.markdown("Your 22-year-old Singaporean bro. Try an activity, or just chat!")

if st.button("Say Hi"):
    st.session_state.messages.append({"role": "assistant", "content": "Oi bro! You finally clicked something haha 😂"})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("What’s up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        messages = [
            {"role": "user", "content": singapore_friend_male},
            {"role": "assistant", "content": f"Yo, what's good, bro? Anything on your mind? (I'm {bot_name})"}
        ]
        for message in st.session_state.messages:
            messages.append({"role": message["role"], "content": message["content"]})
        messages.append({"role": "user", "content": prompt})

        try:
            os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
            response_generator = litellm.completion(
                model="gemini/gemini-2.0-flash-001",
                messages=messages,
                stream=True,
                max_tokens=200,
                temperature=0.7,
                top_p=0.9
            )

            full_response = ""
            response_placeholder = st.empty()
            for chunk in response_generator:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            error_msg = f"Wah, something went wrong: {e}"
            st.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
