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
    st.session_state['message_history'].append({"role":"user","content":inp})
    # with st.chat_message("user"):
    #     st.text(inp)


    # with st.chat_message("assistant"):
    response = chatbot.invoke({"messages":[HumanMessage(content=inp)]},config=config1)
    st.session_state['message_history'].append({"role":"assistant","content":response['messages'][-1].content})
        # print(response)
        # st.text(response['messages'][-1].content)
        
    load_convos()
    
