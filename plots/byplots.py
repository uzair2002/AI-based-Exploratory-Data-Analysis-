import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
# from calculations import classify_data
from init_session_state import initialize_session_state

# Call the function to initialize session state
initialize_session_state()
def numerical_column_plots(num, selected_column1, selected_column2):
    plots = {}
    column_dataframes1 = {}
    column_dataframes2 = {}

    # Check if selected columns exist in the DataFrame
    if selected_column1 not in num.columns or selected_column2 not in num.columns:
        return plots, column_dataframes1, column_dataframes2


    fig_hist= px.histogram(num, x=selected_column1,
        y=selected_column2,
        hover_data=num.columns,
        title=f'Histogram for {selected_column1} with {selected_column2}')
    plots['hist'] = fig_hist
    
    
    # Create scatter plot
    fig_scatter = px.scatter(num, x=selected_column1,y=selected_column2,
        trendline="ols", trendline_color_override="#15F5BA",
        title=f'Scatter Plot for {selected_column1} with {selected_column2}')
    plots['scatter'] = fig_scatter

    # Calculate the correlation matrix
    corr_matrix = num.corr()

    # Create a heatmap
    fig_heatmap= px.imshow(corr_matrix,
                    labels=dict(color="Correlation"),
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    width=1120, height=630,
                    color_continuous_scale='Earth',
                    text_auto=True)

    fig_heatmap.update_layout(title='Numeric Correlation Heatmap')
    plots['heatmap']=fig_heatmap

    column_df1 = num[[selected_column1]]
    column_dataframes1[selected_column1] = column_df1

    column_df2 = num[[selected_column2]]
    column_dataframes2[selected_column2] = column_df2

    return plots, column_dataframes1, column_dataframes2






def categorical_column_plots(cat, selected_column1, selected_column2):
    plots = {}
    column_dataframes1 = {}
    column_dataframes2 = {}
    # Perform cross-tabulation
    crosstab_df = pd.crosstab(cat[selected_column1], cat[selected_column2])

# Create heatmap plot using Plotly Express
    fig_heatmap = px.imshow(crosstab_df,
                            labels=dict(x=selected_column2, y=selected_column1),
                            x=crosstab_df.columns,
                            y=crosstab_df.index,
                            text_auto=True, aspect="auto",
                            title=f'Cross Tabulation Heatmap between {selected_column1} and {selected_column2}')
    plots['crosstab_heatmap'] = fig_heatmap

    
# Create bar chart for cross-tabulation
    fig_bar = go.Figure(data=[
        go.Bar(x=crosstab_df.index, y=crosstab_df[col], name=col) for col in crosstab_df.columns
    ])
    fig_bar.update_layout(title=f'Cross Tabulation Bar Chart between {selected_column1} and {selected_column2}',
                          xaxis=dict(title=selected_column1),
                          yaxis=dict(title='Frequency'))
    plots['crosstab_bar'] = fig_bar

# Generate Sunburst Chart
    fig_sunburst = px.sunburst(cat, path=[selected_column1, selected_column2])

    # Add Sunburst Chart to plots dictionary
    plots['sunburst_chart'] = fig_sunburst

# Generate Sankey Chart

    links = cat.groupby([selected_column1, selected_column2]).size().reset_index()
    links.columns = ['source', 'target', 'value']

    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=cat[selected_column1].unique().tolist() + cat[selected_column2].unique().tolist(),
            color="#83c9ff"  # Color for nodes
        ),
        link=dict(
            source=links['source'].apply(lambda x: cat[selected_column1].unique().tolist().index(x)),
            target=links['target'].apply(lambda x: len(cat[selected_column1].unique().tolist()) + cat[selected_column2].unique().tolist().index(x)),
            value=links['value'],
            color="#6b9da0"  # Color for links
        ))])

    fig_sankey.update_layout(title_text=f'Sankey Chart: {selected_column1} to {selected_column2}')
    plots['fig_sankey'] = fig_sankey


    column_df1 = cat[[selected_column1]]
    column_dataframes1[selected_column1] = column_df1
    column_df2 = cat[[selected_column2]]
    column_dataframes2[selected_column2] = column_df2
    return plots, column_dataframes1, column_dataframes2    
    
    



def cat_to_num_column_plots(df, selected_column1, selected_column2):
    plots = {}
    column_dataframes1 = {}
    column_dataframes2 = {}
# Create Hist    
    fig_hist= px.histogram(df, x=selected_column2,
        color=selected_column1,marginal="rug",
        title=f'Histogram for {selected_column1} with {selected_column2}')
    fig_hist.update_layout(barmode='overlay',
    # xaxis_title_text='Value', # xaxis label
    # yaxis_title_text='Count', # yaxis label
    bargap=0.2, # gap between bars of adjacent location coordinates
    bargroupgap=0.1 # gap between bars of the same location coordinates
)
    plots['fig_hist'] = fig_hist

# Create bar chart 
    fig_bar = go.Figure(data=[
        go.Bar(x=df[selected_column1], y=df[selected_column2],)
    ])
    fig_bar.update_layout(title=f'Cross Tabulation Bar Chart between {selected_column1} and {selected_column2}',
                          xaxis=dict(title=selected_column1),
                          yaxis=dict(title='Frequency'))
    plots['crosstab_bar'] = fig_bar

    # Create line plot
    fig_line = px.line(df, x=selected_column1,
        y=selected_column2, 
        title=f'Line Plot for {selected_column1} with {selected_column2}')
    plots['fig_line'] = fig_line


    #violin
    fig_violin = px.violin(df, y=selected_column1, x=selected_column2,color=selected_column1, box=True, points="all",
              hover_data=df.columns)
    plots['fig_violin'] = fig_violin

    fig_box = px.box(df,x=selected_column2, y=selected_column1)
    plots['box_plot'] = fig_box

    fig_swarm = px.strip(df, x=selected_column1, y=selected_column2, color=selected_column1,
    
    )
    plots['fig_swarm'] = fig_swarm


    column_df1 = df[[selected_column1]]
    column_dataframes1[selected_column1] = column_df1
    column_df2 = df[[selected_column2]]
    column_dataframes2[selected_column2] = column_df2
    return plots, column_dataframes1, column_dataframes2    
    
