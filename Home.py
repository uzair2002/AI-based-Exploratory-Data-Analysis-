import pandas as pd
import streamlit as st
st.set_page_config(layout="wide",page_title="Home",initial_sidebar_state="collapsed")


# Custom imports
from calculations import about_data,descriptive_statistics,classify_data,nulls
from plots.homeplots import column_type_pie,plot_donut_chart
from plots.homeplots import Plolt_cat_describe,Plolt_Num_describe
#from GenAI import store_df
#from init_session_state import initialize_session_state
from authenticator import read_configuration,create_authenticator,initialize_session_state_Auth,render_content, update_configuration
from Random_Important_Functions import hide_sidebar_and_deploy_button,Sidebar_Title
def initialize_page():
    Sidebar_Title()
    st.title('**AI Based Exploratory Data Analysis (EDA)**')


def File_uploader():
    
    uploaded_file = st.file_uploader(f"Choose a file", type="csv")  # Specify file type as CSV
    # Custom CSS for file uploader
    css = '''
    <style>
        [data-testid='stFileUploader'] {
            float: right;
        }
        [data-testid='stFileUploader'] section {
            padding: 0;
            float: left;
        }
        [data-testid='stFileUploader'] section > input + div {
            display: none;
        }
        [data-testid='stFileUploader'] section + div {
            float: right;
            padding-top: 0;
        }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)
    
    # Check if file is uploaded at the beginning and if a new file is uploaded
    if "uploaded_file" not in st.session_state or uploaded_file is not None:
        if uploaded_file is None:
            st.info("No data to analyze.\n PLEASE UPLOAD YOUR FILE")
        else:
            st.session_state["uploaded_file"] = uploaded_file
            st.success("File uploaded successfully !!")
        
        # Read the uploaded file and store it in session state
        if "uploaded_file" in st.session_state:
            df1 = pd.read_csv(st.session_state["uploaded_file"])
            st.session_state["my_input"] = df1
    
    # Return the DataFrame
    if "my_input" in st.session_state:
        return st.session_state["my_input"]


def Data_Preview(df):
    with st.expander("***Data Preview***"):
        col_E1,col_E2=st.columns([5,1])
        with col_E1:
            st.dataframe(df)
        with col_E2:
            temp_df=pd.DataFrame.from_dict(about_data(df), orient='index', columns=['Value'])
            st.write(temp_df)
            st.write("***About Data***")

def null_check(df,num,cat):
    col1a,col2a,col3a = st.columns([3,3,3])
    with col1a:
       # Display the session state variable
        i=0
        st.write("## **Data Schema Visualization**")
        fig_sunburst=column_type_pie(df)
        fig_sunburst.update_layout(width=450, height=450)
       
    with col2a:
        if not cat.empty:
            selected_column_cat = st.selectbox("Select column to check null percentage of **_Catogarical Data_**", options=cat.columns)
        else:
            st.info("Catogarical Data not available")
        # fig_null.update_layout(width=450, height=450)
        # st.write(f"The percentage of null values in column '{selected_column}' is: {null_percentage:.2f}%")
        
      #  st.write(f"The percentage of null values in column '{selected_column}' is: {null_percentage:.2f}%")
    with col3a:
        if not num.empty:
            selected_column_num = st.selectbox("Select column to check null percentage of **_Numreical Data_**", options=num.columns)
        else:
            st.info("Numreical Data not available")
       # st.write(f"The percentage of null values in column '{selected_column}' is: {null_percentage:.2f}%")

   
    col1b,col2b,col3b = st.columns([3,3,3])       
    with col1b:
       # Display the session state variable
       
        fig_sunburst=column_type_pie(df)
        fig_sunburst.update_layout(width=450, height=400)
        with st.container(height=400):
            st.plotly_chart(fig_sunburst)
    with col2b:
        
        # fig_null.update_layout(width=450, height=450)
        # st.write(f"The percentage of null values in column '{selected_column}' is: {null_percentage:.2f}%")
        with st.container(height=400):
            if not cat.empty:
                fig_null_cat,null_percentage_cat = plot_donut_chart(cat, selected_column_cat)
                fig_null_cat.update_layout(width=450, height=400)
                st.plotly_chart(fig_null_cat)
            else:
                st.caption("No Catogarical Data available for visualization.")   
        if not cat.empty:st.write(f"The percentage of null values in column {selected_column_cat} is: {null_percentage_cat:.2f}%")
    with col3b:
        
        with st.container(height=400):
            if not num.empty:
                fig_null_num,null_percentage_num = plot_donut_chart(num, selected_column_num)
                fig_null_num.update_layout(width=450, height=400)
                st.plotly_chart(fig_null_num)
            else:
               st.caption("No Numreical Data available for visualization.")
        if not num.empty:st.write(f"The percentage of null values in column {selected_column_num} is: {null_percentage_num:.2f}%")


def cat_stats(cat):
    if not cat.empty:
        st.divider()  ##################################################################################################
        col1c, col2c = st.columns(2)
        with col1c:
            st.write("### Descriptive Statistics and Plot for Categorical Data")
            st.write(descriptive_statistics(cat))
        with col2c:
            with st.container(height=500):
                fig_line= Plolt_cat_describe(cat)
                st.plotly_chart(fig_line)
    
def num_stats(num):
    if not num.empty:
        st.divider()  ##################################################################################################
        col1d, col2d = st.columns(2)
        with col1d:
          with st.container(height=500):
            fig_line= Plolt_Num_describe(num)
            st.plotly_chart(fig_line)
            # Select column to check null percentage
            
        with col2d:
            st.write("### Descriptive Statistics and Plot for Numreical Data")                
            st.write(descriptive_statistics(num))


def date_stats(date):
    if not date.empty:
        st.divider()
        col1e, col2e = st.columns(2)
        with col1e: st.write("Date Data", date)
        with col2e:
            # st.write(date.max() - date.min())
            # st.write(date.max())
            # st.write(date.min())
            # st.write([date.min(), date.max(), date.max() - date.min()])
# Create a DataFrame with minimum, maximum, and their difference
            data = {
                'Statistic': ['Minimum Date', 'Maximum Date', 'Difference'],
                'Value': [date.min(), date.max(), date.max() - date.min()]
            }
            # Create the DataFrame
            df_stats = pd.DataFrame(data)
            # Display the DataFrame as a table
            st.write(df_stats)
    # st.write("Nulls",nulls(df))
    


def main():
    
    initialize_page()
    # initialize_session_state()
    df=File_uploader()
    if df is not None:
        num, cat, date = classify_data(df)
        st.session_state["My_numCol"]= num
        st.session_state["My_catCol"]= cat
        st.session_state["My_dateCol"]= date
        Data_Preview(df)
        null_check(df,num,cat)
        cat_stats(cat)
        num_stats(num)
        date_stats(date)
        st.divider()
        col1f, col2f = st.columns(2)
        with col1f: 
            if not cat.empty:st.write("Categorical Data", cat)  
        with col2f: 
            if not num.empty:st.write("Numerical Data", num)
         
       
        

hide_sidebar_and_deploy_button()
config = read_configuration()
authenticator = create_authenticator(config)
initialize_session_state_Auth()
render_content(config, authenticator)
if "authentication_status" in st.session_state:
    if st.session_state["authentication_status"]:
        main()
update_configuration(config)
