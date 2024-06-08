import streamlit as st
st.set_page_config(layout="wide",page_title="Bivarient Analysis",initial_sidebar_state="expanded")

# Custom imports
from plots.byplots import numerical_column_plots,cat_to_num_column_plots
from plots.byplots import categorical_column_plots
from Random_Important_Functions import delete_columns_with_high_unique_values
#from init_session_state import initialize_session_state
from authenticator import check_login 

# initialize_session_state()



st.title('Bivarient Analysis')

if "My_numCol" in st.session_state:
    num=st.session_state["My_numCol"]
    delete_columns_with_high_unique_values(num, threshold=0.99)
if "My_catCol" in st.session_state:
    cat=st.session_state["My_catCol"]
    delete_columns_with_high_unique_values(cat, threshold=0.99)
if "My_dateCol" in st.session_state:
    date=st.session_state["My_dateCol"]



def num_to_num():

    # Call the function to get the plots
    st.write("### **Numerical to Numerical Analysis**")
    col1, col2, col3 = st.columns([3,1,1])
    with col1:
        plot_type = st.selectbox("Select plot type", ['Histogram','Scatter Plot'])
    with col2:
        numerical_columns=num.columns
        selected_column1 = st.selectbox("Select numerical column 1", numerical_columns, key="selectbox1")
    with col3:
        # Filter out the selected_column1 from the options for selected_column2
        filtered_numerical_columns = numerical_columns[numerical_columns != selected_column1]
        selected_column2 = st.selectbox("Select numerical column 2", filtered_numerical_columns)

    numerical_plots, num_df1, num_df2 = numerical_column_plots(num, selected_column1, selected_column2)
    try:

        with col1:
            if plot_type == 'Scatter Plot':
                st.plotly_chart(numerical_plots['scatter'])
            elif plot_type == 'Histogram':
                st.plotly_chart(numerical_plots['hist'])
    
        with col2:        
            st.write("Column 1 Description:")
            st.write(num_df1[selected_column1].describe())

        with col3:
            st.write("Column 2 Description:")
            st.write(num_df2[selected_column2].describe())
        
        with st.expander("***Numeric Correlation Heatmap***"):
            c1,c2,c3= st.columns([1,5,1])
            with c2:
                st.plotly_chart(numerical_plots['heatmap']) 

    except:
        st.info("Unable to plot. Please either select a different plot type or ensure there are two numerical columns available for plotting")
    
 

def cat_to_cat():

    st.write("### **Catogarocal To Catogarocal Analysis**")

    col1, col2, col3 = st.columns([1,1,3])
    with col3:
        plot_type = st.selectbox("Select plot type", ['Bar', 'Sankey','Sunburst',"Heatmap"])
    with col1:
        categorical_column = cat.columns
        selected_column1 = st.selectbox("Select categorical column 1", categorical_column, key="selectbox2")
    with col2:
        # Filter out the selected_column1 from the options for selected_column2
        filtered_categorical_column = categorical_column[categorical_column != selected_column1]
        selected_column2 = st.selectbox("Select categorical column 2", filtered_categorical_column)
    try:
        with col3:
            #if selected_column1 and selected_column2:    
                categorical_plots,cat_df1,cat_df2 = categorical_column_plots(cat, selected_column1, selected_column2)
                #st.write(pd.concat([col_df1[selected_column1].value_counts(), col_df2[selected_column2].value_counts()], axis=0))
                if plot_type == 'Heatmap':
                    # Display heatmap
                    st.plotly_chart(categorical_plots['crosstab_heatmap'])
            
                elif plot_type == 'Bar':
                
                    # Display bar chart
                    st.plotly_chart(categorical_plots['crosstab_bar'])

                elif plot_type =='Sunburst':
                
                    st.plotly_chart(categorical_plots['sunburst_chart'])   
                
                elif plot_type=='Sankey':
                    st.plotly_chart(categorical_plots['fig_sankey'])
                    

        

        with col1:
            st.write(cat_df1[selected_column1].value_counts())
                
        with col2:
            st.write(cat_df2[selected_column2].value_counts())



    except :
        st.info("Unable to plot. Please either select a different plot type or ensure there are two categorical columns available for plotting.")

    # except NameError:
    #     st.info("Plot not available/num col not present. Please select a different plot type or column.")

 

def cat_to_num():

    st.write("### **Catogarical To Numerical**")
    try:
        col1, col2, col3 = st.columns([1,3,1])
        with col2:
            plot_type = st.selectbox("Select plot type", ['Violin','Bar','Histogram','Swarm','Box'])
        with col1:
            categorical_column = cat.columns

            selected_column1 = st.selectbox("Select categorical column 1", categorical_column,key="selectbox3")
            pass
        with col3:
            numerical_columns = num.columns
            selected_column2 = st.selectbox("Select numerical column 2", numerical_columns,key="selectbox4")

        cat_num_plots,cat_df3,num_df3=cat_to_num_column_plots(df,selected_column1,selected_column2)
        with col1:
            st.write(cat_df3[selected_column1].value_counts())
            pass
        with col3:
            st.write(num_df3[selected_column2].describe())
        with col2:
            if selected_column1 and selected_column2:    
                #plots,cat_df1,cat_df2 = categorical_column_plots(df, selected_column1, selected_column2)

                if plot_type == 'Box':
                    # Display heatmap
                    st.plotly_chart(cat_num_plots['box_plot'])

                elif plot_type == 'Histogram':
                    st.plotly_chart(cat_num_plots['fig_hist'])
                elif plot_type == 'Bar':
                    if selected_column1 and selected_column2:
                        # Display bar chart
                        st.plotly_chart(cat_num_plots['crosstab_bar'])

                elif plot_type =='Sunburst':
                    if selected_column1 and selected_column2:
                        st.plotly_chart(cat_num_plots['sunburst_chart'])

                elif plot_type =='Violin':
                    if selected_column1 and selected_column2:
                        st.plotly_chart(cat_num_plots['fig_violin'])

                elif plot_type=='Swarm':
                    if selected_column1 and selected_column2:
                        st.plotly_chart(cat_num_plots['fig_swarm'])    
    except:
        st.info("Unable to plot. Please either select a different plot type or ensure  that one numerical and one categorical column is available for plotting.")
        

if "authentication_status" in st.session_state:
    if st.session_state["authentication_status"]:
        check_login()
        try:
            if "my_input" in st.session_state:
                df=st.session_state["my_input"]
    
            delete_columns_with_high_unique_values(df, threshold=0.99)
            st.divider()
            num_to_num()
            st.divider()
            cat_to_cat()
            st.divider()
            cat_to_num()
        except :
            st.divider()
            st.warning("NO DATA AVAILABLE. PLEASE UPLOAD YOUR CSV FILE ON THE [Home](Home) TO CONTINUE.")

    else:
        st.write("Please [Log in](main) to get started!!")
