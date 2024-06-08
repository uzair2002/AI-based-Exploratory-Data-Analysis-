import streamlit as st
st.set_page_config(layout="wide",page_title="Multivarient Analysis",initial_sidebar_state="expanded")

# Custom imports
from plots.multiplots import scatter_plot,histogram_plot
from Random_Important_Functions import delete_columns_with_high_unique_values
# from init_session_state import initialize_session_state
from authenticator import check_login 

# Call the function to initialize session state
# initialize_session_state()



st.title('Multivarient Analysis')


#num, cat, date = classify_data(df)

def scatter():
    st.subheader("Multivariate Scatter Plot")
    if num.empty or  cat.empty or num.shape[1] < 2:
        st.info("Unable to plot. Please ensure  that two numerical and one categorical column is available for plotting.")
    else:
        num_columns_1=num.columns
        # Select X-axis column
        x_axis_col = st.selectbox("Select X-axis column:", options=num_columns_1) 
        # Select Y-axis column
        f_num_columns_1 = num_columns_1[num_columns_1 != x_axis_col]
        y_axis_col = st.selectbox("Select Y-axis column:", options=f_num_columns_1)
        # Select categorical columns
        cat_cols = st.multiselect("Select categorical columns (at most 2):", options=cat.columns)
        show_ols = st.checkbox("Show OLS Trend Line")
        # Check the number of selected categorical columns
        if len(cat_cols) > 2:
            st.error("You can select at most two categorical columns.")
        else:
            # Checkbox for OLS trend line
            
            # Plot scatter plot
            buff, col2,buff = st.columns([1,5,1])
            with col2:fig=scatter_plot(df, x_axis_col, y_axis_col, cat_cols, show_ols)
            #st.plotly_chart(fig)
    # else:st.info("Unable to plot. Please either select a different plot type or ensure  that  and one categorical column is available for plotting.")


##################################################################################

def histogram():
    st.subheader("Multivariate Histogram")
    if num.empty or  cat.empty or num.shape[1] < 2:
        st.info("Unable to plot. Please ensure  that two numerical and one categorical column is available for plotting.")
    else:
        num_columns_2=num.columns
        x_axis_col = st.selectbox("Select column for x-axis:", options=num_columns_2)
        f_num_columns_2 = num_columns_2[num_columns_2 != x_axis_col]

        y_axis_col = st.selectbox("Select column for y-axis:", options=f_num_columns_2)

        # Select categorical column for color encoding
        cat_col = st.selectbox("Select categorical column for color encoding:", options=cat.columns)

        # Checkbox options for show_rug, show_curve, and show_hist
        show_rug = st.checkbox("Show Rug Plot")
        show_curve = st.checkbox("Show Curve Plot")
        show_hist = st.checkbox("Show Histogram Plot", value=True)

        # Plot histogram with color encoding
        buff,col2,buff = st.columns([1,5,1])
        with col2:histogram_plot(df, x_axis_col, y_axis_col, cat_col, show_rug, show_curve, show_hist)


# # #st.write(df)
# # AI_response= Multivarient_AI()
# # st.write(AI_response)


if "authentication_status" in st.session_state:
    if st.session_state["authentication_status"]:
        check_login()
        try:
            if "my_input" in st.session_state:
                df=st.session_state["my_input"]
            delete_columns_with_high_unique_values(df, threshold=0.99)
            categorical_columns = df.select_dtypes(include=['object']).columns
            numerical_columns = df.select_dtypes(exclude=['object']).columns
            cat=df[categorical_columns]
            num=df[numerical_columns]

            st.divider()
            scatter()
            st.divider()
            histogram()

        except :
            st.write('***')
            st.warning("NO DATA AVAILABLE. PLEASE UPLOAD YOUR CSV FILE ON THE [Home](Home) TO CONTINUE.")
    else:
        st.write("Please [Log in](Home) to get started!!")