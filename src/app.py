import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]

st.set_page_config(page_title="Streaming Bot")
st.title("Streaming Bot")



# Get Response
def get_response(user_query, chat_hostory):

    template = """
        As an accommodating assistant, please respond to the questions taking into account our conversation history 
        Chat history : {chat_history}
        User question: {user_question}

        """
    
    prompt = ChatPromptTemplate.from_template(template=template)

    llm  = ChatOpenAI()
    
    chain = prompt | llm | StrOutputParser()
    
    return chain.stream (
        {
            "chat_history": chat_hostory,
            "user_question": user_query
        }
    )





# conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)    

user_query = st.chat_input("Your message")



if user_query is not None and user_query !="":
    st.session_state.chat_history.append(HumanMessage(user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        respone = st.write_stream(get_response(user_query, st.session_state.chat_history))
        

    st.session_state.chat_history.append(AIMessage(content=respone))

