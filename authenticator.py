import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from Random_Important_Functions import Sidebar_Title
    


# Set page background image
def set_page_background_image():
    page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-image: url("https://r4.wallpaperflare.com/wallpaper/998/592/1023/red-triangles-low-poly-low-poly-art-wallpaper-48661d4810307c88a01c511e9822548a.jpg");
        background-size: 120%;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: local;
    }
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    </style>
    """
    return page_bg_img

# Create signup button
def create_signup_button():
    st.header("NEW HERE ?")
    st.text(f"Ready to analyze your data with AI?\nSign in here to access our EDA website.")
    st.button("Go to Signup", on_click=switch_page)

# Read configuration from YAML file
def read_configuration():
    with open('data.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config

# Create authenticator object
def create_authenticator(config):
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    return authenticator

# Initialize session state variable for page number
def initialize_session_state_Auth():
    if "page" not in st.session_state:
        st.session_state.page = "login"

# Switch between login and signup page
def switch_page():
    if st.session_state.page == "login":
        st.session_state.page = "signup"
    else:
        st.session_state.page = "login"

# Render content based on the current page
def render_content(config, authenticator):
    if st.session_state.page == "login":
        render_login_page(authenticator)
    elif st.session_state.page == "signup":
        render_signup_page(authenticator)

# Render login page content
def render_login_page(authenticator):
    login_columns, _, SignupButton_column, _ = st.columns([5, 1, 2, 1])
    with login_columns:
        authenticator.login()
        if "authentication_status" in st.session_state:
            if st.session_state["authentication_status"]:
                st.sidebar.markdown("<div style='margin-bottom:600px;'></div>", unsafe_allow_html=True)
                st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
                authenticator.logout("Logout", "sidebar")
                st.markdown("""<style>.st-emotion-cache-g0dirf.eczjsme1{visibility:visible;}</style>""", unsafe_allow_html=True)
            elif st.session_state["authentication_status"] is False:
                st.error('Username/password is incorrect')
                # page_bg_img=set_page_background_image()
                # st.markdown(page_bg_img, unsafe_allow_html=True)
            elif st.session_state["authentication_status"] is None:
                st.info('Please enter your username and password')
                # page_bg_img=set_page_background_image()
                # st.markdown(page_bg_img, unsafe_allow_html=True)
    with SignupButton_column:
        if st.session_state["authentication_status"] is False or st.session_state["authentication_status"] is None:
            create_signup_button()

# Render signup page content
def render_signup_page(authenticator):
    # page_bg_img=set_page_background_image()
    # st.markdown(page_bg_img, unsafe_allow_html=True)
    LoginButton_column, _, Signup_columns, _ = st.columns([2, 1, 5, 1])
    with Signup_columns:
        try:
            email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(pre_authorization=False)
            if email_of_registered_user:
                st.success('User registered successfully')
        except Exception as e:
            st.error(e)
    with LoginButton_column:
        st.header("ALREADY HAVE AN ACCOUNT?")
        st.text("Let's get started! Please log in to continue.")
        st.button("Go to Login", on_click=switch_page)

# Update the configuration file
def update_configuration(config):
    with open('data.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)




def check_login():
    #if st.session_state["authentication_status"]:  
    config=read_configuration()
    # Step 2: Create an authenticator object
    authenticator = create_authenticator(config) 
    Sidebar_Title()
    st.sidebar.markdown("<div style='margin-bottom:600px;'></div>", unsafe_allow_html=True)
    st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
    authenticator.logout("Logout", "sidebar")
    if not st.session_state["authentication_status"]:
        st.switch_page("Home.py")
