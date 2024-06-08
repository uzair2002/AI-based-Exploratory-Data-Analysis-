import streamlit as st
st.set_page_config(layout="wide",initial_sidebar_state="expanded")


from Random_Important_Functions import Sidebar_Title
from authenticator import read_configuration,create_authenticator,update_configuration
if "authentication_status" in st.session_state:
    if st.session_state["authentication_status"]:
        st.header("Settings")
        config=read_configuration()
        # Step 2: Create an authenticator object
        authenticator = create_authenticator(config)
        Sidebar_Title()
        st.sidebar.markdown("<div style='margin-bottom:600px;'></div>", unsafe_allow_html=True)
        st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
        authenticator.logout("Logout", "sidebar")
        if not st.session_state["authentication_status"]:
            st.switch_page("Home.py")  
        # Step 5: Create a reset password widget
    
        try:
            if authenticator.reset_password(st.session_state.get("username", "")):
                st.success('Password modified successfully')
        except Exception as e:
            st.error(e)

        # Step 9: Create an update user details widget
        # if "authentication_status" in st.session_state:
        #     if st.session_state["authentication_status"]:
        try:
            if authenticator.update_user_details(st.session_state.get("username", "")):
                st.success('Entries updated successfully')
        except Exception as e:
            st.error(e)



        # Step 10: Update the configuration file
        update_configuration(config)

    else:
        st.write("Please [Log in](Home) to get started!!")
