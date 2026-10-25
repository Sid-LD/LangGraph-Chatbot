
import streamlit as st
import ast
from langgraph_database_backend import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage
import uuid


# ******************************** utility functions ********************************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id


def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []


def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


def load_conversation(thread_id):
    state = chatbot.get_state(
        config={'configurable': {'thread_id': thread_id}}
    )

    # Return an empty list if messages do not exist
    return state.values.get('messages', [])


def extract_text(content):
    """Extract readable text from strings or structured content blocks."""

    if isinstance(content, str):
        stripped = content.strip()

        # Handle a Python-style list converted into a string
        if (
            stripped.startswith("[")
            and "'type': 'text'" in stripped
        ):
            try:
                parsed = ast.literal_eval(stripped)

                if isinstance(parsed, (list, dict)):
                    return extract_text(parsed)

            except (ValueError, SyntaxError):
                pass

        # Convert literal newline characters into real line breaks
        return content.replace("\\n", "\n")

    elif isinstance(content, list):
        text_parts = []

        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    text_parts.append(
                        extract_text(block.get("text", ""))
                    )

            elif isinstance(block, str):
                text_parts.append(extract_text(block))

        return "".join(text_parts)

    elif isinstance(content, dict):
        if content.get("type") == "text":
            return extract_text(content.get("text", ""))

    return ""


# ******************************** Session Setup ********************************

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])


# ******************************** Sidebar UI ********************************

st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:

    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'

            content = extract_text(msg.content)

            if content:
                temp_messages.append({
                    'role': role,
                    'content': content
                })

        st.session_state['message_history'] = temp_messages


# ******************************** Main UI ********************************

# Display the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


user_input = st.chat_input('Type here')

if user_input:

    # Add and display the user message
    st.session_state['message_history'].append({
        'role': 'user',
        'content': user_input
    })

    with st.chat_message('user'):
        st.markdown(user_input)

    CONFIG = {
        'configurable': {
            'thread_id': st.session_state['thread_id']
        }
    }

    # Stream the assistant response
    with st.chat_message("assistant"):

        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            ):
                if isinstance(message_chunk, AIMessage):

                    # Extract only readable text
                    content = extract_text(message_chunk.content)

                    if content:
                        yield content

        ai_message = st.write_stream(ai_only_stream())

    # Save the assistant response in message history
    st.session_state['message_history'].append({
        'role': 'assistant',
        'content': ai_message
    })
