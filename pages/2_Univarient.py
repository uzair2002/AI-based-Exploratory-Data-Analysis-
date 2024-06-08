import streamlit as st
st.set_page_config(layout="wide",page_title="Univarient Analysis",initial_sidebar_state="expanded")

# Custom imports

#from init_session_state import initialize_session_state
from plots.uplots import numerical_column_plots
from plots.uplots import categorical_column_plots
from Random_Important_Functions import delete_columns_with_high_unique_values
from authenticator import check_login 



# Call the function to initialize session state
# initialize_session_state()




st.title('Univarient Analysis')
st.write('***')


if "My_numCol" in st.session_state:
    num=st.session_state["My_numCol"]
if "My_catCol" in st.session_state:
    cat=st.session_state["My_catCol"]
# else:st.write("cat no available")
if "My_dateCol" in st.session_state:
    date=st.session_state["My_dateCol"]

def cat_data_plot():
    ###                                           catogarical
    # Split the screen into two columns
    st.write("### **Catogarical Analysis**")
    col1, col2 = st.columns([3, 4])
    selected_column=None
    try:
        plots, column_dataframes = categorical_column_plots(cat)
        # Display dropdowns in the left column
        with col1:
            # Get plots and individual categorical column DataFrames
            categorical_columns = cat.columns
            selected_column = st.selectbox("Select column", categorical_columns)
            st.write(column_dataframes[selected_column])
            
    except :
        pass

        

    # Display plot in the right column
    with col2:
        selected_chart = st.selectbox("Select chart type", ['Bar Chart', 'Pie Chart'])
            #st.set_page_config(layout='centered')
        try:
            if selected_column is not None and selected_column in plots:
                if selected_chart == 'Bar Chart':
                    st.plotly_chart(plots[selected_column]['bar'])
                elif selected_chart == 'Pie Chart':
                    st.plotly_chart(plots[selected_column]['pie'])
            else:
                st.info("Plot not available for selected column/no catogarical col present.")
        except KeyError :
             st.info("Plot not available for selected column/no catogarical col present.")
        

###                                                numerical
def num_data_plot():
    st.write("#### **Numerical Analysis**")

    # Call the function to get the plots
    numerical_plots, numerical_dataframes = numerical_column_plots(num)

    # Split the screen into two columns
    col1, col2 = st.columns([4,3])
    # Dropdown to select plot type
    # Dropdown to select numerical column
    with col2:
        
        numerical_columns = num.columns
        selected_column = st.selectbox("Select numerical column", numerical_columns)
        if selected_column is not None:
        #num_col_des=numerical_dataframes[selected_column].describe()
            st.write(numerical_dataframes[selected_column].describe())


    with col1:
        # Display selected plot
        try:    
            plot_type = st.selectbox("Select plot type", ['Histogram', 'Box Plot', 'KDE Plot'])
            if plot_type == 'Histogram':
                #try:
                    st.plotly_chart(numerical_plots[f'{selected_column}_hist'])
                # except KeyError:
                    # st.error("Plot not available. Please select a different plot type or column.")
            elif plot_type == 'Box Plot':
                #try:
                    st.plotly_chart(numerical_plots[f'{selected_column}_box'])
                # except KeyError:
                    # st.error("Plot not available. Please select a different plot type or column.")
            elif plot_type == 'KDE Plot':
            
                    st.plotly_chart(numerical_plots[f'{selected_column}_kde'])
        except KeyError:
            st.info("Plot not available/num col not present. Please select a different plot type or column.")

if "authentication_status" in st.session_state:
    if st.session_state["authentication_status"]:
        check_login()
        try:
            #date=delete_columns_with_high_unique_values(date, threshold=0.99)
            delete_columns_with_high_unique_values(num, threshold=0.99)
            delete_columns_with_high_unique_values(cat, threshold=0.99)

            cat_data_plot()
            st.write('***')
            num_data_plot()
            
        except :
            st.warning("NO DATA AVAILABLE. PLEASE UPLOAD YOUR CSV FILE ON THE [Home](Home) TO CONTINUE.")
    else:
        st.write("Please [Log in](home) to get started!!")
