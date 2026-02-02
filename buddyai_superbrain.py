import streamlit as st
import openai
import pyttsx3
import speech_recognition as sr
from datetime import datetime

# ---------------------------
# OPENAI KEY
# ---------------------------
openai.api_key = "YOUR_API_KEY_HERE"

# ---------------------------
# VOICE ENGINE
# ---------------------------
engine = pyttsx3.init()
engine.setProperty('rate', 135)
engine.setProperty('volume', 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ---------------------------
# AI RESPONSE
# ---------------------------
def get_ai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a kind, patient helper for seniors. Speak clearly, warmly, and briefly."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=120
    )
    return response["choices"][0]["message"]["content"]

# ---------------------------
# SPEECH INPUT
# ---------------------------
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎧 Listening...")
        audio = r.listen(source)
        try:
            return r.recognize_google(audio)
        except:
            return "I didn’t quite hear you."

# ---------------------------
# PAGE STYLE
# ---------------------------
st.set_page_config(page_title="BuddyAI", page_icon="🤖")

st.markdown("""
<style>
body { font-size: 28px; }
button {
    font-size: 32px !important;
    padding: 30px !important;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# UI
# ---------------------------
st.title("🤖 BuddyAI")
st.write("I’m here to help you.")

# Free vs Premium toggle simulation
premium_enabled = st.checkbox("Premium Mode (unlock extra features)")

if st.button("🎤 TALK TO BUDDYAI"):
    user_input = listen()
    st.write("You said:")
    st.write(user_input)

    reply = get_ai_response(user_input)
    st.write("BuddyAI says:")
    st.write(reply)
    speak(reply)

st.subheader("⏰ Set a Reminder")
reminder_text = st.text_input("What should I remind you about?")
reminder_time = st.time_input("What time?", datetime.now().time())

if st.button("✅ Save Reminder"):
    if premium_enabled or reminder_text != "":
        message = f"I will remind you at {reminder_time.strftime('%I:%M %p')} to {reminder_text}"
        st.success(message)
        speak(message)
    else:
        st.warning("Upgrade to Premium for unlimited reminders!")

st.markdown("---")
st.markdown("**BuddyAI is not a medical professional.**")
