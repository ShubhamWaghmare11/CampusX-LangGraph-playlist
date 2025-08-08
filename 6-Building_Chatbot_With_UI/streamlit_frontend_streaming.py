

import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

# print(type(st.session_state))
if "message_history" not in st.session_state:
    st.session_state['message_history'] = []


def load_convos():
    print(st.session_state['message_history'])
    for i in st.session_state['message_history']:
        with st.chat_message(i['role']):
            st.text(i['content'])


inp =st.chat_input(placeholder="Your Message")


config1 = {"configurable":{"thread_id":"1"}}

if inp:
    load_convos()
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
        
    


    


