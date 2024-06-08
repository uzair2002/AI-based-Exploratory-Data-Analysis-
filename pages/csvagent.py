import streamlit as st
st.set_page_config(layout="wide",page_title="Ask your CSV",initial_sidebar_state="expanded")
#from langchain_experimental.agents import create_csv_agent  # Import from langchain_experimental
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_google_genai import ChatGoogleGenerativeAI 
from dotenv import load_dotenv
import os
from authenticator import check_login 

from Random_Important_Functions import Sidebar_Title
Sidebar_Title()
#from Api_Key import GOOGLE_API_KEY

# os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
# genai.configure(api_key=GOOGLE_API_KEY)
llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0, convert_system_message_to_human=True)

def main():
    load_dotenv()

    # Load the OpenAI API key from the environment variable
    if os.getenv("GOOGLE_API_KEY") is None or os.getenv("GOOGLE_API_KEY") == "":
        print("GOOGLE_API_KEY is not set")
        exit(1)
    else:
        print("GOOGLE_API_KEY is set")

   
    st.header("Ask your CSV 📈")

    csv_file = st.file_uploader("Upload a CSV file", type="csv")
    if csv_file is not None:

        
        agent = create_csv_agent(
            llm,
            
            csv_file,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
        )
        # agent = create_csv_agent(
        #     llm(temperature=0), csv_file, verbose=True)
        # st.write(csv_file)
        user_question = st.text_input("Ask a question about your CSV: ")

        if user_question is not None and user_question != "":
            with st.spinner(text="In progress..."):
                try:
                    st.write(agent.run(user_question))
                except Exception as e:
                    st.warning("An error occurred: {}".format(e))



if "authentication_status" in st.session_state:
    if st.session_state["authentication_status"]:
        check_login()
        main()

    else:
        st.write("Please [Log in](home) to get started!!")