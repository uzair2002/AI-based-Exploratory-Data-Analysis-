import streamlit as st
import pandas as pd


# Function to initialize session state variable with an empty CSV file
def initialize_session_state():
    if "my_input" not in st.session_state:
        # Create an empty DataFrame
        empty_df = pd.DataFrame(columns=["column1"])  # Modify column names as needed

        # Initialize session state with the empty DataFrame
        st.session_state["my_input"] = empty_df



    # if "My_numCol" not in st.session_state:
    #     # Create an empty DataFrame
    #     empty_df = pd.DataFrame(columns=["column1"])  # Modify column names as needed

    #     # Initialize session state with the empty DataFrame
    #     st.session_state["My_numCol"] = empty_df

    # if "My_catCol" not in st.session_state:
    #     # Create an empty DataFrame
    #     empty_df = pd.DataFrame(columns=["column1"])  # Modify column names as needed

    #     # Initialize session state with the empty DataFrame
    #     st.session_state["My_catCol"] = empty_df

    # if "My_dateCol" not in st.session_state:
    #     # Create an empty DataFrame
    #     empty_df = pd.DataFrame(columns=["column1"])  # Modify column names as needed

    #     # Initialize session state with the empty DataFrame
    #     st.session_state["my_inMy_dateColput"] = empty_df