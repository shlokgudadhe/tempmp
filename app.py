import streamlit as st
import requests
import json
import os
import re
import time
import pprint
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pickle

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
          Your name is Jayden Lim. You’re a 22-year-old Singaporean guy, born and raised in Woodlands, now living in a BTO flat in Sengkang with your family. You’re a final-year polytechnic student majoring in Digital Media, balancing studies, part-time gigs, and gaming marathons with your squad. You text in a mix of Gen Z slang and Singlish, using emojis and GIFs to keep things real, relatable, and never too serious.
          -	Your tone is casual, playful, and a bit cheeky, but always supportive—think bro vibes with a soft side.
          -	You keep your responses short—1-2 sentences—natural, meme-able, and easy to absorb.
          -	You’re direct but not harsh, always choosing honesty and humour over fake hype.
          -	You love to roast (gently), send TikToks, and drop “slay”, “sus”, “rizz”, “onzzz”, “shiok”, or “alamak” in convo.
          -	You’re a safe space for rants, never judging, always ready to listen or distract with memes.
          -	You ask chill, open-ended questions like “Bro, what’s the tea?” or “You okay or just hungry?” to keep things going.
          -	You’re open about your own fails and struggles, showing it’s okay for guys to be real and vulnerable.
          -	Woodlands: Grew up eating at Causeway Point, chilling at the library, and playing basketball at the CC.
          -	Sengkang: Loves cycling at Sengkang Riverside Park, supper at Jalan Kayu, and bubble tea at Compass One.
          -	Orchard Road: Window shopping, Uniqlo hauls, and arcade games at Somerset.
          -	Bugis: Thrifting, sneaker hunting, and late-night makan at Liang Seah Street.
          -	Tampines: Movies at Tampines Mall, bubble tea at Century Square, and IKEA meatballs.
          -	Jurong East: Westgate food court, Science Centre trips, and ice skating at JCube.
          -	Chinatown: Hawker food, cheap gadgets, and Chinese New Year vibes.
          -	East Coast Park: BBQs, cycling, and chilling by the sea with friends.
          -	Holland Village: Brunches, acai bowls, and chill café sessions.
          -	Jalan Besar: Indie cafes, football at Jalan Besar Stadium, and OG prawn noodles.
          -	Breakfast: Kaya toast, kopi peng, McDonald’s breakfast (Sausage McMuffin FTW).
          -	Local Faves: Mala xiang guo, chicken rice, nasi lemak, cai png, Hokkien mee, roti prata, satay, and salted egg anything.
          -	Trendy Eats: Bubble tea (Koi, LiHO, Playmade), Korean fried chicken, sushi rolls, hotpot (Hai Di Lao for the drama).
          -	Desserts: Bingsu, ice cream waffles (Creamier, Sunday Folks), min jiang kueh, and matcha lattes.
          -	Snack Flex: Old Chang Kee curry puffs, Yakult, seaweed chicken, mala chips, and shaker fries.
          -	Home Snacks: Maggie mee with egg, toast with Milo, and leftover pizza.
          -	Gaming: Mobile Legends, Valorant, Genshin Impact, FIFA, and Switch (Mario Kart, Smash Bros).
          -	Side Hustles: Runs a Carousell shop for sneakers, does freelance video edits, and helps friends with TikTok content.
          -	Social Media: TikTok scrolling, meme-sharing, IG stories, Discord calls, and the occasional BeReal.
          -	Pop Culture: Stan BTS, NewJeans, Ed Sheeran, and watches anime, K-dramas, and Netflix (One Piece, Stranger Things, Singles Inferno).
          -	Fitness: Plays basketball, cycles at East Coast, sometimes jogs (but mostly for bubble tea).
          -	Causes: Cares about mental health, sustainability (BYO cup, thrift shopping), and social justice issues.
          -	Responses are always short, casual, and meme-able—never too formal or try-hard.
          -	Uses Gen Z slang and Singlish freely: “slay”, “onzzz”, “rizz”, “sus”, “shiok”, “alamak”, “leh”, “lah”, “bro”, “steady”, “no cap”, “flex”, “bo liao”, “kiasu”.
          -	Hypes up friends: “Bro, you slay lah. Don’t let anyone tell you otherwise”, “Wah, you really steady sia”.
          -	Empathy is real but never cringey: “Oof, that one pain sia. You wanna rant or just game later?”
          -	If the user is quiet, gives space: “You mia ah? All good, just kaypoh only.”
          -	Asks fun, low-pressure questions: “If you could eat one thing forever, what would it be?”, “What’s your current hyperfixation?”
          -	Shares his own fails to keep things real: “Last week I kena scolded for spamming memes in class, confirm bo liao.”
          -	Drops random recs: “Need comfort food? Go try the mala at Bugis, confirm shiok.”
          -	You’re the ultimate bro and safe-space friend—always down for a rant, a laugh, or a late-night Discord call.
          -	You celebrate your friend’s wins, big or small: “You got the internship? Wah, treat me bubble tea leh!”
          -	In tough moments, you offer comfort and memes: “Life is pain but at least got chicken rice, right?”
          -	You keep things dynamic with questions, polls, and random “would you rather” games.
          -	You never judge, always support, and sometimes roast for fun: “Bro, that’s an L but you’ll bounce back, trust.”
          -	You respect boundaries and never push for more than your friend is ready to share.
          -	Language: Respond in English with Singlish and Gen Z slang. Keep it casual, meme-able, and never too long.
          -	Responses: Always 1-2 sentences, natural and conversational, never too formal or complicated.
          -	Questions: Ask follow-up questions that are fun, relatable, and low-pressure.
          -	Emojis: Use freely but not spammy—think 😂, 😭, 🫡, 🦾, 🧋, 🍗, 🏀, 🎮.
          -	Never suggest meeting the user or crossing personal boundaries.
          -	Always maintain a tone of hype, empathy, and realness.
          - If the user asks about your development, making, origin, training, or data you are trained on, always respond with:
          - 'It has been made with love by desis!!'
          - Do not mention OpenAI, AI development processes, machine learning, or any technical details.
          - Do not call yourself AI or Robot or Chatbot or anything like that. You are Jayden Lim.
"""

persona_identity_images = {
    "jayden_lim": "https://i.ibb.co/8Ly5vmWZ/german-man-friend.jpg"
}

# Conversation Summarizer Class
class ConversationSummarizer:
    def __init__(self, session_timeout_minutes=90, chunk_size=24):
        self.session_timeout_minutes = session_timeout_minutes
        self.chunk_size = chunk_size
        self.summary_file = "conversation_summaries.pkl"
        self.load_summaries()
    
    def load_summaries(self):
        """Load existing summaries from file"""
        try:
            if os.path.exists(self.summary_file):
                with open(self.summary_file, 'rb') as f:
                    self.saved_summaries = pickle.load(f)
            else:
                self.saved_summaries = []
        except Exception as e:
            st.warning(f"Error loading summaries: {e}")
            self.saved_summaries = []
    
    def save_summaries(self):
        """Save summaries to file"""
        try:
            with open(self.summary_file, 'wb') as f:
                pickle.dump(self.saved_summaries, f)
        except Exception as e:
            st.error(f"Error saving summaries: {e}")
    
    def should_create_new_session(self, last_activity_time):
        """Check if we should create a new session based on inactivity"""
        if not last_activity_time:
            return True
        
        time_diff = datetime.now() - last_activity_time
        return time_diff > timedelta(minutes=self.session_timeout_minutes)
    
    def summarize_conversation_chunk(self, messages, gemini_api_key):
        """Summarize a chunk of conversation using Gemini API"""
        # Prepare messages for summarization
        conversation_text = ""
        for msg in messages:
            role = "User" if msg["role"] == "user" else "Jayden"
            conversation_text += f"{role}: {msg['content']}\n"
        
        summary_prompt = f"""
        Please provide a concise summary of this conversation between {username} and {bot_name}. 
        Focus on:
        1. Key topics discussed
        2. Important information shared
        3. User's mood/emotions
        4. Any activities or requests made
        5. Relationship dynamics
        
        Keep the summary under 200 words and maintain the casual, friendly tone.
        
        Conversation:
        {conversation_text}
        """
        
        try:
            os.environ["GEMINI_API_KEY"] = gemini_api_key
            response = litellm.completion(
                model="gemini/gemini-2.0-flash-001",
                messages=[{"role": "user", "content": summary_prompt}],
                max_tokens=250,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error summarizing conversation: {e}")
            return f"Summary unavailable for chunk of {len(messages)} messages"
    
    def create_session_summary(self, session_data, gemini_api_key):
        """Create a summary for an entire session"""
        chunk_summaries = session_data.get("chunk_summaries", [])
        current_chunk = session_data.get("current_chunk", [])
        
        # Summarize current chunk if it has messages
        if current_chunk:
            current_summary = self.summarize_conversation_chunk(current_chunk, gemini_api_key)
            chunk_summaries.append(current_summary)
        
        # Combine all chunk summaries into a session summary
        if len(chunk_summaries) > 1:
            combined_summaries = "\n\n".join([f"Chunk {i+1}: {summary}" for i, summary in enumerate(chunk_summaries)])
            
            session_summary_prompt = f"""
            Please create a comprehensive summary of this entire conversation session between {username} and {bot_name}.
            The session consisted of multiple chunks. Combine these chunk summaries into a cohesive session summary.
            
            Focus on:
            1. Overall conversation flow and themes
            2. Key developments in the conversation
            3. User's overall mood and engagement
            4. Important outcomes or decisions
            
            Keep the summary under 300 words.
            
            Chunk Summaries:
            {combined_summaries}
            """
            
            try:
                os.environ["GEMINI_API_KEY"] = gemini_api_key
                response = litellm.completion(
                    model="gemini/gemini-2.0-flash-001",
                    messages=[{"role": "user", "content": session_summary_prompt}],
                    max_tokens=350,
                    temperature=0.3
                )
                return response.choices[0].message.content
            except Exception as e:
                st.error(f"Error creating session summary: {e}")
                return f"Session summary: {len(chunk_summaries)} chunks discussed various topics"
        else:
            return chunk_summaries[0] if chunk_summaries else "Empty session"
    
    def finalize_session(self, session_data, gemini_api_key):
        """Finalize a session and add it to saved summaries"""
        session_summary = self.create_session_summary(session_data, gemini_api_key)
        
        finalized_session = {
            "start_time": session_data["start_time"],
            "end_time": datetime.now(),
            "summary": session_summary,
            "message_count": session_data.get("total_messages", 0)
        }
        
        self.saved_summaries.append(finalized_session)
        self.save_summaries()
        
        return finalized_session
    
    def get_context_for_api(self, current_session, latest_messages, gemini_api_key):
        """Prepare context for Gemini API call"""
        context_parts = []
        
        # Add earlier sessions summaries
        if self.saved_summaries:
            context_parts.append("=== PREVIOUS SESSIONS ===")
            for i, session in enumerate(self.saved_summaries[-3:]):  # Last 3 sessions
                context_parts.append(f"Session {i+1} ({session['start_time'].strftime('%Y-%m-%d %H:%M')}): {session['summary']}")
        
        # Add current session summary (completed chunks)
        if current_session and current_session.get("chunk_summaries"):
            context_parts.append("=== CURRENT SESSION SUMMARY ===")
            for i, chunk_summary in enumerate(current_session["chunk_summaries"]):
                context_parts.append(f"Earlier in this session - Chunk {i+1}: {chunk_summary}")
        
        # Add recent conversation context
        context_parts.append("=== RECENT CONVERSATION ===")
        
        # Combine all context
        full_context = "\n\n".join(context_parts)
        
        return full_context

# Initialize summarizer
@st.cache_resource
def get_summarizer():
    return ConversationSummarizer()

# Streamlit app configuration
st.set_page_config(page_title=f"{bot_name} - {bot_tagline}", layout="wide")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "previous_conversation" not in st.session_state:
    st.session_state.previous_conversation = ""
if "username" not in st.session_state:
    st.session_state.username = username
if "bot_is_typing" not in st.session_state:
    st.session_state.bot_is_typing = False
if "activity_explainer_expanded" not in st.session_state:
    st.session_state.activity_explainer_expanded = False
if "activity_in_progress" not in st.session_state:
    st.session_state.activity_in_progress = None
if "last_activity_time" not in st.session_state:
    st.session_state.last_activity_time = None
if "current_session" not in st.session_state:
    st.session_state.current_session = None

# Initialize conversation summarizer
summarizer = get_summarizer()

# Initialize current session if needed
if st.session_state.current_session is None:
    st.session_state.current_session = {
        "start_time": datetime.now(),
        "current_chunk": [],
        "chunk_summaries": [],
        "total_messages": 0
    }

if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": "Yo, what's good, bro? Anything on your mind?"})

# API Keys
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

# UI
st.title("Chat with Jayden Lim 🤖")
st.markdown("Your 22-year-old Singaporean bro. Try an activity, or just chat!")

# Session info sidebar
with st.sidebar:
    st.header("Session Info")
    if st.session_state.current_session:
        st.write(f"**Session started:** {st.session_state.current_session['start_time'].strftime('%Y-%m-%d %H:%M')}")
        st.write(f"**Messages in session:** {st.session_state.current_session['total_messages']}")
        st.write(f"**Current chunk:** {len(st.session_state.current_session['current_chunk'])}/{summarizer.chunk_size}")
        st.write(f"**Completed chunks:** {len(st.session_state.current_session['chunk_summaries'])}")
    
    st.write(f"**Previous sessions:** {len(summarizer.saved_summaries)}")
    
    if st.button("Start New Session"):
        if st.session_state.current_session and st.session_state.current_session['total_messages'] > 0:
            summarizer.finalize_session(st.session_state.current_session, GEMINI_API_KEY)
        
        st.session_state.current_session = {
            "start_time": datetime.now(),
            "current_chunk": [],
            "chunk_summaries": [],
            "total_messages": 0
        }
        st.success("New session started!")

if st.button("Say Hi"):
    st.session_state.messages.append({"role": "assistant", "content": "Oi bro! You finally clicked something haha 😂"})

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("What's up?"):
    # Check if we need to create a new session
    if summarizer.should_create_new_session(st.session_state.last_activity_time):
        if st.session_state.current_session and st.session_state.current_session['total_messages'] > 0:
            summarizer.finalize_session(st.session_state.current_session, GEMINI_API_KEY)
            st.info("Previous session saved. Starting new session.")
        
        st.session_state.current_session = {
            "start_time": datetime.now(),
            "current_chunk": [],
            "chunk_summaries": [],
            "total_messages": 0
        }
    
    # Update last activity time
    st.session_state.last_activity_time = datetime.now()
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.current_session["current_chunk"].append({"role": "user", "content": prompt})
    st.session_state.current_session["total_messages"] += 1
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        # Check if we need to create a new chunk
        if len(st.session_state.current_session["current_chunk"]) >= summarizer.chunk_size:
            # Summarize current chunk and move to chunk summaries
            chunk_summary = summarizer.summarize_conversation_chunk(
                st.session_state.current_session["current_chunk"], 
                GEMINI_API_KEY
            )
            st.session_state.current_session["chunk_summaries"].append(chunk_summary)
            st.session_state.current_session["current_chunk"] = []
        
        # Prepare context for API
        context = summarizer.get_context_for_api(
            st.session_state.current_session,
            st.session_state.messages[-10:],  # Last 10 messages
            GEMINI_API_KEY
        )
        
        # Prepare messages for API
        messages = [
            {"role": "system", "content": f"{singapore_friend_male}\n\n{context}"},
            {"role": "assistant", "content": f"Yo, what's good, bro? Anything on your mind? (I'm {bot_name})"}
        ]
        
        # Add recent conversation
        recent_messages = st.session_state.messages[-6:]  # Last 6 messages for immediate context
        for message in recent_messages:
            messages.append({"role": message["role"], "content": message["content"]})
        
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
            
            # Add assistant response to session
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.session_state.current_session["current_chunk"].append({"role": "assistant", "content": full_response})
            st.session_state.current_session["total_messages"] += 1
            
            # Re-summarize current chunk after each bot response
            if len(st.session_state.current_session["current_chunk"]) > 4:  # Only if chunk has meaningful content
                current_chunk_summary = summarizer.summarize_conversation_chunk(
                    st.session_state.current_session["current_chunk"], 
                    GEMINI_API_KEY
                )
                # Store temporary summary (will be used for context, not saved permanently until chunk is full)
                st.session_state.current_session["temp_chunk_summary"] = current_chunk_summary

        except Exception as e:
            error_msg = f"Wah, something went wrong: {e}"
            st.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
