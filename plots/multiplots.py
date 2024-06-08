import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

def scatter_plot(df, x_axis_col, y_axis_col, cat_cols, show_ols):
    if not x_axis_col or not y_axis_col:
        st.error("Please select both X-axis and Y-axis columns.")
        return
    
    selected_cols = [x_axis_col, y_axis_col] + cat_cols
    df_selected = df[selected_cols]

    if not all(col in df.columns for col in selected_cols):
        st.error("One or more selected columns do not exist in the DataFrame.")
        return

    fig_scatter = px.scatter(df_selected, x=x_axis_col, y=y_axis_col,
                     color=cat_cols[0] if cat_cols else None,
                     symbol=cat_cols[1] if len(cat_cols) > 1 else None,
                     title="Scatter Plot",
                     width=1280, height=720,
                     trendline="ols" if show_ols else None)
    st.plotly_chart(fig_scatter)

    return fig_scatter
    


def histogram_plot(df, num_col1, num_col2, cat_col, show_rug=False, show_curve=False, show_hist=True):
    data = df[[num_col1, num_col2, cat_col]].dropna()
    
    if len(data) == 0:
        st.warning("No data available to plot the histogram.")
        return

    hist_data = [data[data[cat_col] == category][num_col1].tolist() for category in data[cat_col].unique()]
    group_labels = [str(category) for category in data[cat_col].unique()]
    
    # Choose a color scheme
    colors = ['#A6ACEC','#37AA9C', '#94F3E4','#2BCDC1', '#F66095','#A56CC1', '#A6ACEC', '#63F5EF']  # Example color scheme 3

    fig_histogram_plot = ff.create_distplot(
        hist_data=hist_data,
        group_labels=group_labels,
        colors=colors,
        show_rug=show_rug,
        show_curve=show_curve,
        show_hist=show_hist
    )
    
    fig_histogram_plot.update_layout(
        title=f"Histogram with Color Encoding for {num_col1} and {num_col2}",
        xaxis_title=num_col1,
        yaxis_title=num_col2,
        width=1280, height=720
    )
    st.plotly_chart(fig_histogram_plot)
