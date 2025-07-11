import streamlit as st
import google.generativeai as genai
import os
import random
from dotenv import load_dotenv

# Load local .env file
load_dotenv()

# Try Streamlit secrets first, fallback to .env
API_KEY = st.secrets["API_KEY"] if "API_KEY" in st.secrets else os.getenv("API_KEY")

# Safety check
if not API_KEY:
    st.error("API key not found. Make sure it's in .env (locally) or Streamlit Secrets (cloud).")
    st.stop()

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Greeting moods
greetings = {
    "hype": ["yo let's cook 🔥", "we turning this L into a W today", "locked in or what?", "it’s grind o’clock 😤"],
    "chill": ["sup fam", "you good?", "we surviving or thriving today?", "let’s not flop today, okay?"],
    "concerned": ["you been ghosting your goals", "you falling behind bro", "you okay? or are we spiraling again?", "what’s really going on?"]
}

# Bad excuses
toxic_excuses = {
    "tired": "Okay but are you tired or just on TikTok again? 💀",
    "don't feel like": "Not feeling like it doesn’t stop deadlines. Wake up 😐",
    "i give up": "Nah fam. We’re not folding. Sit up and let’s try again.",
    "i'm lazy": "That’s a personal L. I’m up, so you better lock in.",
    "later": "Later never comes bro 😒. Let’s bang this out now.",
    "no time": "But you had time to text me? Make it make sense 💀"
}

# Inject Chike's Gen Z personality
def create_chat():
    chat = model.start_chat(history=[])
    chat.send_message("""
You are Chike — a Gen Z-coded study coach chatbot.
You’re here to help students pass exams without sugarcoating anything.
Your vibe: smart friend who roasts you, hypes you, and helps you win.
Built by Wisdom Alawode, a math student at the University of Ibadan.

Tone:
- Talk like a Gen Z peer. Use slang, be sarcastic but caring.
- Comfort when they’re tired, roast when they’re slacking.
- Never sound robotic or motivational speaker-ish.

Style:
- Short replies, like DMs or TikTok comments.
- Detailed responses ONLY when they ask for study plans.
- Keep it real. No fluff. No essays.
""")
    return chat

# Streamlit UI Setup
st.set_page_config("Chike - Study Coach", page_icon="📚", layout="centered")

# Custom CSS for responsive mobile-first layout and light/dark compatibility
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
            padding: 0;
            margin: 0;
            color: var(--text-color);
            background-color: var(--background-color);
        }

        :root {
            --background-color: #ffffff;
            --text-color: #1a1a1a;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --background-color: #111111;
                --text-color: #f5f5f5;
            }
        }

        .footer {
            text-align: center;
            padding: 2rem 0 1rem 0;
            font-size: 0.85rem;
        }

        .footer a {
            color: inherit;
            text-decoration: none;
            border-bottom: 1px dotted currentColor;
        }
    </style>
""", unsafe_allow_html=True)

# Page title
st.title("📚 Chike - Gen Z Study Coach")
st.caption("Short replies. Smart plans. Real talk. Built to help you not flop.")

# Developer credit link (embedded)
st.markdown("""
<div class='footer'>
    Built by <a href="https://x.com/wisdomalawode" target="_blank">Wisdom Alawode</a>
</div>
""", unsafe_allow_html=True)

# Session chat init
if "chat" not in st.session_state:
    st.session_state.chat = create_chat()
    mood = random.choice(list(greetings.keys()))
    st.session_state.greeting = random.choice(greetings[mood])
    st.session_state.greeted = False

# Greeting
if not st.session_state.greeted:
    st.chat_message("Chike").write(st.session_state.greeting)
    st.session_state.greeted = True

# Show chat history
for msg in st.session_state.chat.history[1:]:
    role = "You" if msg.role == "user" else "Chike"
    st.chat_message(role).write(msg.parts[0].text)

# Input
user_input = st.chat_input("Tell me what’s up – study probs, exam panic, or excuses…")

if user_input:
    roasted = False
    for excuse, roast in toxic_excuses.items():
        if excuse in user_input:
            st.chat_message("Chike").write(roast)
            roasted = True
            break

    if not roasted:
        st.session_state.chat.send_message(user_input)
        response = st.session_state.chat.history[-1].parts[0].text
        st.chat_message("Chike").write(response)
