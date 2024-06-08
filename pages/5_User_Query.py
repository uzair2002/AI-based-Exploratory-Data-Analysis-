import streamlit as st
st.set_page_config(layout="wide",page_title="User Quries",initial_sidebar_state="expanded")

# Custom imports
#SSfrom init_session_state import initialize_session_state
from GenAI import questions,init_chat
from GenAI import hello
from GenAI import  genai_response
from authenticator import check_login 


st.title('User Quries')


if "my_input" in st.session_state:
    df=st.session_state["my_input"]
      


# Streamlit app content
def main():
    st.write(hello())
    # Access the uploaded CSV data from session state

    #st.write(df.describe())
    chat=init_chat(df)
    with st.spinner(text="In progress..."):
        AI_QUE= questions(chat)
        st.write(AI_QUE)

    with st.form("my_form"):
        user_input = st.text_input("Ask your Query about the uploaded CSV here.")
        st.write("<p style='color:gray;font-size:smaller;'>Press the Submit button below to apply.</p>", unsafe_allow_html=True)
        submit = st.form_submit_button("Submit")




    #AI.log_history()
    # Handle form submission
    if submit:
        if  user_input is not None and user_input != "":  # Check if user_input is an empty string
            st.write("Please write a question before pressing the submit button.")
        else:
            with st.spinner(text="In progress..."):
                ans=genai_response(user_input,chat)
                st.write("Model:\n", ans)

if "authentication_status" in st.session_state:
    if st.session_state["authentication_status"]:
        check_login()
        try:main()
        except Exception as e:
            st.warning("An error occurred: {}".format(e)) 
    else:
        st.write("Please [Log in](Home) to get started!!")