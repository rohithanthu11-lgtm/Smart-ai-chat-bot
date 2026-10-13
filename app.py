"""A beginner-friendly Streamlit chatbot powered by local Ollama or simple rules."""

import logging
import string

import ollama
import streamlit as st


APP_TITLE = "Local AI Chat"
DEFAULT_MODEL = "qwen2.5:3b"
WELCOME_MESSAGE = (
    "Hi! I'm your friendly local AI assistant. Ask me anything to get started."
)
SYSTEM_MESSAGE = (
    "You are a friendly, helpful assistant. Give clear answers in a warm tone. "
    "When a question is unclear, ask a short follow-up question."
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_rule_based_response(message: str) -> str:
    """Return a simple response without contacting an AI model."""
    cleaned_message = message.lower().strip().rstrip(string.punctuation)

    if cleaned_message in {"hi", "hello", "hey", "good morning", "good afternoon"}:
        return "Hello! It's nice to meet you. What would you like help with?"
    if "who are you" in cleaned_message or "what are you" in cleaned_message:
        return (
            "I'm a friendly chatbot running in this Streamlit app. "
            "Choose Local Ollama in the sidebar to chat with your Qwen model."
        )
    if "how are you" in cleaned_message:
        return "I'm doing well, thanks for asking! How can I help you today?"
    if "thank" in cleaned_message:
        return "You're very welcome! Let me know if there's anything else I can do."
    if "help" in cleaned_message or "what can you do" in cleaned_message:
        return (
            "I can chat with you, answer questions, and help explain ideas. "
            "For more capable answers, select Local Ollama in the sidebar."
        )

    return (
        "That's an interesting question. The rule-based demo has limited answers. "
        "Select Local Ollama in the sidebar for a fuller response from Qwen."
    )


def get_ollama_response(
    message: str, conversation: list[dict[str, str]], host: str, model: str
) -> str:
    """Send the conversation to the selected model running in local Ollama."""
    client = ollama.Client(host=host.strip())
    messages = [{"role": "system", "content": SYSTEM_MESSAGE}]

    # Keep the current conversation context, excluding the welcome message.
    messages.extend(
        {"role": item["role"], "content": item["content"]}
        for item in conversation
        if item["role"] in {"user", "assistant"}
        and item["content"] != WELCOME_MESSAGE
    )
    messages.append({"role": "user", "content": message})

    response = client.chat(model=model.strip(), messages=messages)
    return response.message.content or "I couldn't generate a response this time."


def initialize_chat() -> None:
    """Start a fresh conversation the first time the app is opened."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": WELCOME_MESSAGE}
        ]


def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="💬",
        layout="centered",
        initial_sidebar_state="expanded",
    )
    initialize_chat()

    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(ellipse at 50% 0%, #172746 0%, transparent 48%),
                #0b1020;
            color: #edf2ff;
        }
        [data-testid="stHeader"] { background: transparent; }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #111a2e 0%, #0d1424 100%);
            border-right: 1px solid #26324b;
        }
        .hero {
            padding: 1.4rem 0 1rem;
        }
        .hero h1 {
            color: #f3f6ff;
            font-size: clamp(2rem, 5vw, 2.7rem);
            letter-spacing: -0.04em;
            margin-bottom: 0.3rem;
        }
        .hero p { color: #aab7d0; font-size: 1.02rem; }
        [data-testid="stChatMessage"] {
            background: #121b2d;
            border: 1px solid #25324a;
            border-radius: 18px;
            padding: 0.65rem 0.85rem;
            margin: 0.8rem 0;
        }
        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
            background: #18243a;
        }
        [data-testid="stChatInput"] {
            border-color: #405274;
            border-radius: 16px;
        }
        div.stButton > button {
            border-radius: 12px;
            min-height: 2.7rem;
        }
        @media (max-width: 640px) {
            .hero { padding-top: 0.6rem; }
            [data-testid="stChatMessage"] { padding: 0.5rem 0.65rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("## 💬 Local AI Chat")
        st.caption("A private, beginner-friendly chatbot running on your computer.")
        st.divider()

        st.markdown("### Chat settings")
        chat_mode = st.radio(
            "Response engine",
            ["Local Ollama", "Rule-based demo"],
            help="Local Ollama uses the model installed on your computer.",
        )
        ollama_host = st.text_input(
            "Ollama address",
            value="http://localhost:11434",
            help="The usual Ollama address. Change this only if your Ollama server uses another address.",
            disabled=chat_mode != "Local Ollama",
        )
        model_name = st.text_input(
            "Model name",
            value=DEFAULT_MODEL,
            help="This must match a model shown by the `ollama list` command.",
            disabled=chat_mode != "Local Ollama",
        )

        st.divider()
        st.markdown("### About")
        st.write(
            "Your messages are sent to Ollama on your own machine. "
            "They are not sent to a hosted AI service."
        )
        if st.button(
            "Clear chat",
            icon=":material/delete_outline:",
            width="stretch",
        ):
            st.session_state.messages = [
                {"role": "assistant", "content": WELCOME_MESSAGE}
            ]
            st.rerun()

    st.markdown(
        f"""
        <div class="hero">
            <h1>{APP_TITLE}</h1>
            <p>Thoughtful answers, powered by your own local Qwen model.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for chat_message in st.session_state.messages:
        avatar = "✨" if chat_message["role"] == "assistant" else "🧑"
        with st.chat_message(chat_message["role"], avatar=avatar):
            st.markdown(chat_message["content"])

    prompt = st.chat_input("Write a message…")
    if prompt is None:
        return

    prompt = prompt.strip()
    if not prompt:
        st.warning("Please type a message before sending.")
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant", avatar="✨"):
            with st.spinner("Thinking…"):
                if chat_mode == "Local Ollama":
                    if not model_name.strip():
                        raise ValueError("Enter the name of an Ollama model.")
                    answer = get_ollama_response(
                        prompt,
                        st.session_state.messages[:-1],
                        ollama_host,
                        model_name,
                    )
                else:
                    answer = get_rule_based_response(prompt)
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    except ollama.ResponseError as error:
        logger.exception("Ollama returned an error")
        st.error(
            f"Ollama could not use model '{model_name}': {error}. "
            f"Check `ollama list` and make sure the model name is correct."
        )
    except (ollama.RequestError, ConnectionError) as error:
        logger.exception("Could not reach the local Ollama server")
        st.error(
            f"Could not connect to Ollama at '{ollama_host}': {error}. "
            "Make sure Ollama is running, then try again."
        )
    except Exception as error:
        logger.exception("Unexpected error while generating a reply")
        st.error(f"Something went wrong while generating a reply: {error}")


if __name__ == "__main__":
    main()
