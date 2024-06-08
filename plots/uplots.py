import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
#from .GenAI import create_agent

# Define the categorical_column_plots function
def categorical_column_plots(cat):
    categorical_columns = cat
    plots = {}
    column_dataframes = {}
    for col in categorical_columns:
        # Create bar chart plot using Plotly Express
        fig_bar = px.bar(cat[col].value_counts(), x=cat[col].value_counts().index, y=cat[col].value_counts().values,
                         labels={'x': col, 'y': 'Frequency'}, title=f'Bar Chart: Frequency count for {col}')
        # Create pie chart plot using Plotly Express
        fig_pie = px.pie(cat[col].value_counts(), names=cat[col].value_counts().index, values=cat[col].value_counts().values,
                         title=f'Pie Chart: Frequency count for {col}')
        plots[col] = {'bar': fig_bar, 'pie': fig_pie}
        # Create DataFrame for the categorical column
        column_df = cat[col].value_counts().reset_index()
        column_df.columns = [col, 'Frequency']
        column_dataframes[col] = column_df
    return plots, column_dataframes




def numerical_column_plots(num):
    numerical_columns = num
    plots = {}
    column_dataframes = {}
    for col in numerical_columns:
        cleaned_df=num[col].dropna()

        cleaned_list = cleaned_df.tolist()

        group_labels = [f'Histogram for {col}']
        fig_hist = ff.create_distplot([cleaned_list], group_labels, colors=['#83c9ff'],)
        plots[f'{col}_hist'] = fig_hist

        # Create box plot using Plotly Express
        fig_box = px.box(num, y=col, title=f'Box Plot for {col}')
        plots[f'{col}_box'] = fig_box

        # Create KDE plot using Plotly Express
        fig_kde = px.density_contour(num, x=col, y=col, title=f'Kernel Density Estimate for {col}')
        plots[f'{col}_kde'] = fig_kde

        # Create DataFrame for the numerical column
        column_df = num[[col]]
        column_dataframes[col] = column_df
    return plots, column_dataframes
