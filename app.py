import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
# SETUP
# Load environment variables from a .env file for local development.
# This allows us to keep the API key out of the main script.
load_dotenv()

# --- DOCUMENTATION: Tried to set the page configuration first. ---
# This must be the first Streamlit command in the app.
# Page Configuration & Sidebar
st.set_page_config(page_title="Multi-Tool AI Assistant", page_icon="🤖", layout="wide")


#SIDEBAR
# --- DOCUMENTATION: Created a sidebar for navigation and controls. ---
# This keeps the main interface clean.
with st.sidebar:
    st.title("🤖 Multi-Tool AI Assistant")
    st.markdown("---")

    # MODE SELECTION
    st.subheader("Select a Tool")
    # The mode selector allows the user to switch between the app's functions.
    app_mode = st.radio(
        "Choose the tool you want to use:",
        ("Chatbot", "Text Summarizer"),
        label_visibility="collapsed"
    )
    st.markdown("---")

    # MODEL SELECTION
    # Display the model being used. This was simplified from a dropdown menu.
    st.subheader("Model Selection")
    # Set the primary model to be used.
    selected_model_name = "DeepSeek Qwen3 8B"
    st.session_state.selected_model = "deepseek/deepseek-r1-0528-qwen3-8b:free"
    st.info(f"Using model: **{selected_model_name}**")
    
    st.markdown("---")
    
    # Clear history for chatbot mode
    if app_mode == "Chatbot":
        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    with st.expander("ℹ️ About the App"):
        st.markdown(
            f"""
            - **Current Model:** `{st.session_state.selected_model}`
            - **API:** [OpenRouter.ai](https://openrouter.ai/)
            - **Framework:** [Streamlit](https://streamlit.io/)
            """
        )

# AUTHENTICATION & API CLIENT SETUP
# --- DOCUMENTATION:  Securely loading the API key. ---
# This is a critical step for security and user feedback.
# API Key Management
openrouter_key = os.getenv("OPENROUTER_API_KEY")
if not openrouter_key:
    st.error("OpenRouter API key not found! Please add it to your .env file or Streamlit secrets.")
    st.stop()
# --- DOCUMENTATION: Configuring the OpenAI client for OpenRouter. ---
# The base_url and headers are essential for this to work.
#  API Client Initialization
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_key,
    default_headers={
        "HTTP-Referer": "http://localhost:8501", 
        "X-Title": "Streamlit Multi-Tool Bot",
    },
)

# UI LOGIC BASED ON MODE
# --- DOCUMENTATION: Building the main UI based on the selected mode. ---
# An if/elif structure cleanly separates the logic for each tool
# CHATBOT MODE
if app_mode == "Chatbot":
    st.header(f"Chat with {selected_model_name}")
    # Initialize chat history in session state if it doesn't exist.
    if "messages" not in st.session_state:
        st.session_state.messages = []
    # Display a welcome message if the chat is new.
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            st.markdown("Hello! How can I help you today?")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    # --- DOCUMENTATION: Step 6 - Implementing the Chatbot's core logic. ---
    # Get user input from the chat box at the bottom of the screen.
    if prompt := st.chat_input("What would you like to ask?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
         # Get and display the assistant's response.
        with st.chat_message("assistant"):
            try:
                with st.spinner(f"{selected_model_name} is thinking..."):
                    response = client.chat.completions.create(
                        model=st.session_state.selected_model,
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                    )
                    ai_response = response.choices[0].message.content
                    st.markdown(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"An error occurred: {e}")

# TEXT SUMMARIZER MODE
elif app_mode == "Text Summarizer":
    st.header(f"Text Summarizer using {selected_model_name}")
    st.markdown("Paste a news article or any long text below to get a concise summary.")
    
    article_text = st.text_area("Article Text:", height=300, placeholder="Paste your text here...")
    # --- DOCUMENTATION: Implementing the Summarizer's core logic. ---
    if st.button("Summarize Text", use_container_width=True, type="primary"):
        if not article_text.strip():
            st.warning("Please paste some text to summarize.")
        else:
            try:
                # --- DOCUMENTATION: This prompt is specifically crafted to get a 3-line summary. ---
                # This was a direct user requirement.
                with st.spinner(f"{selected_model_name} is summarizing..."):
                    summarization_prompt = f"Please provide a concise summary of the following text in exactly 3 lines:\n\n---\n\n{article_text}"
                    
                    response = client.chat.completions.create(
                        model=st.session_state.selected_model,
                        messages=[
                            {"role": "system", "content": "You are an expert summarizer. Your goal is to extract the key points and main ideas from the provided text."},
                            {"role": "user", "content": summarization_prompt}
                        ],
                    )
                    summary = response.choices[0].message.content
                    
                    st.subheader("Summary:")
                    st.success(summary)
            except Exception as e:
                st.error(f"An error occurred: {e}")




