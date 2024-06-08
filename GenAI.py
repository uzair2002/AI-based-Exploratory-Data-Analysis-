import google.generativeai as genai
import google 
from init_session_state import initialize_session_state
import streamlit as st
import os
# from dotenv import load_dotenv

# load_dotenv()

# # Load the OpenAI API key from the environment variable
# if os.getenv("GOOGLE_API_KEY") is None or os.getenv("GOOGLE_API_KEY") == "":
#     print("GOOGLE_API_KEY is not set")
#     exit(1)
# else:
#     print("GOOGLE_API_KEY is set")


from API_key import GOOGLE_API_KEY

   



os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)


def listmodle():   #list no of modles presen for use
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
listmodle()
def hello():
    str="Hello from GenAI"
    return str



def init_chat(df):
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])


    #def store_df(df):
        # Convert DataFrame to a string
    df_str = df.to_string(index=False)
    # Send the string representation to the chat
    chat.send_message(df_str)
    chat.send_message("from now only give the ans related to the previously given query if asked questions other than that tell you dont have sufficent data")
    return chat


def questions(chat):
    response = chat.send_message("""list 10 analytical questions that can be asked related to the giver data, 
                                 only show questions and nothing else
                                """)
    return response.text

def genai_response(quri,chat):
    #chat= model.start_chat(history=[])
    #quri=input("type your question")
    try:
        # Send the message to the model and handle potential exceptions
        response = chat.send_message(quri)
        print("Uzair:", response.text)
        result=response.text
    except google.generativeai.types.generation_types.BlockedPromptException as e:
        error_message = "Error: The prompt was blocked due to potential safety concerns."
        guidelines = [
            "Please revise your prompt to avoid:",
            "- Explicit language or derogatory terms",
            "- Hate speech or discriminatory content",
            "- Harassment or threats",
            "Consider providing additional context if your prompt is for a specific purpose."
        ]
        
        response = {
            "error_message": error_message,
            "guidelines": guidelines
        }
        
        print(response)
        result=response
    return result



