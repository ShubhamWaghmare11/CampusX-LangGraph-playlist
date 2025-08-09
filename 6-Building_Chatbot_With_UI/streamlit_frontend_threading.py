import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

x = []

# ---------------------Utility functions---------------------
def load_convos():
    # print(st.session_state['message_history'])
    for i in st.session_state['message_history']:
        with st.chat_message(i['role']):
            st.text(i['content'])


def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id


def reset_chat():
    thread_id = generate_thread_id()

    add_thread(st.session_state['thread_id'])
    print(st.session_state['chat_threads'])
    st.session_state['message_history'] = []
    st.session_state['thread_id'] = thread_id
    st.rerun()

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    convos =chatbot.get_state(config={"configurable":{'thread_id':thread_id}})
    print(convos) 
    return chatbot.get_state(config={"configurable":{'thread_id':thread_id}}).values['messages']

# ---------------------Session Setup---------------------
if "message_history" not in st.session_state:
    st.session_state['message_history'] = []

if "thread_id" not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state['chat_threads'] = []

# add_thread(st.session_state['thread_id'])


# ---------------------SIdebar UI---------------------

st.sidebar.title("LangGraph ChatBot")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Conversations")

st.sidebar.text("=============Current==============")
st.sidebar.text("-".join(str(st.session_state['thread_id']).split("-")[:4]))

st.sidebar.text("=============Previous==============")
for i in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button("-".join(str(i).split("-")[:4])):
        print(f"CHAT BUTTON CLICKED: {i}")
        st.session_state['thread_id'] = i
        messages = load_conversation(i)
        print("Workign till HERE")
        temp_messages = []

        print(messages)
        for message in messages:
            if isinstance(message,HumanMessage):
                role = "user"
            else:
                role = 'assistant'

            temp_messages.append({'role':role,"content":message.content})

        st.session_state['message_history'] = temp_messages
# ---------------------Main UI---------------------



load_convos()
inp =st.chat_input(placeholder="Your Message")


config1 = {"configurable":{"thread_id":st.session_state['thread_id']}}

if inp:
    st.session_state['message_history'].append({"role":"user","content":inp})
    with st.chat_message("user"):
        st.text(inp)


    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {"messages":[HumanMessage(content=inp)]},
                config=config1,
                stream_mode="messages"
            )
        )

        st.session_state['message_history'].append({'role':"assistant","content":ai_message})    

        
    


    


