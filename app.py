import streamlit as st
import time
import markdown2
from financial_agent import get_financial_agent

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(
    page_title="Finance AI Assistant",
    page_icon="📈",
    layout="wide"
)

# ------------------------------------------------------
# PREMIUM MODERN CSS
# ------------------------------------------------------
st.markdown("""
<style>

body {
    background-color: #eef1f6;
    font-family: "Inter", sans-serif;
}

/* Title Styling */
.title {
    text-align: center;
    font-size: 40px;
    font-weight: 800;
    margin: 10px 0 0 0;
    color: #1a1a1a;
}

.subtitle {
    text-align: center;
    font-size: 17px;
    color: #555;
    margin-bottom: 25px;
}

/* Chat container */
.chat-container {
    max-width: 780px;
    margin: auto;
}

/* Chat bubbles */
.chat-bubble {
    padding: 14px 18px;
    border-radius: 16px;
    max-width: 80%;
    margin: 12px 0;
    display: flex;
    align-items: flex-start;
    gap: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.07);
}

.bot-bubble {
    background: #ffffff;
    border: 1px solid #dce2eb;
    margin-right: auto;
}

.user-bubble {
    background: #d6e4ff;
    border: 1px solid #c2d4ff;
    margin-left: auto;
}

/* Bubble text area */
.bubble-text {
    font-size: 16px;
    line-height: 1.55;
    color: #1b1b1b;
}

/* Emojis */
.emoji {
    font-size: 28px;
    margin-top: 4px;
}

/* Clickable links */
.bubble-text a {
    color: #0056d6 !important;
    text-decoration: underline !important;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------
# PAGE HEADER
# ------------------------------------------------------
st.markdown("<div class='title'>📈 Finance AI Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Ask about stocks, news, 10-year analysis, performance, comparisons, and more.</div>", unsafe_allow_html=True)

# ------------------------------------------------------
# LOAD AGENT
# ------------------------------------------------------
@st.cache_resource
def load_agent():
    return get_financial_agent()

agent = load_agent()

# ------------------------------------------------------
# SESSION CHAT MEMORY
# ------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your financial assistant. What can I help you analyze today?"}
    ]

# ------------------------------------------------------
# RENDER CHAT HISTORY
# ------------------------------------------------------
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        bubble = "bot-bubble"
        emoji = "🤖"
    else:
        bubble = "user-bubble"
        emoji = "👤"

    # Convert Markdown → HTML BEFORE inserting into bubble
    html_text = markdown2.markdown(msg["content"])

    st.markdown(
        f"""
        <div class="chat-bubble {bubble}">
            <div class="emoji">{emoji}</div>
            <div class="bubble-text">{html_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------
# USER INPUT
# ------------------------------------------------------
prompt = st.chat_input("Type your financial question...")

if prompt:

    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user bubble
    st.markdown(
        f"""
        <div class="chat-bubble user-bubble">
            <div class="emoji">👤</div>
            <div class="bubble-text">{prompt}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    stream_box = st.empty()
    full_response = ""

    # ------------------------------------------------------
    # STREAMING + TYPING EFFECT
    # ------------------------------------------------------
    for chunk in agent.run(message=prompt, stream=True):
        if hasattr(chunk, "content") and chunk.content:
            text = chunk.content
        elif isinstance(chunk, str):
            text = chunk
        else:
            continue

        for c in text:
            full_response += c

            html_text = markdown2.markdown(full_response + "▌")

            stream_box.markdown(
                f"""
                <div class="chat-bubble bot-bubble">
                    <div class="emoji">🤖</div>
                    <div class="bubble-text">{html_text}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            time.sleep(0.006)

    # Final bubble (remove cursor ▌)
    html_text = markdown2.markdown(full_response)

    stream_box.markdown(
        f"""
        <div class="chat-bubble bot-bubble">
            <div class="emoji">🤖</div>
            <div class="bubble-text">{html_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Save assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
