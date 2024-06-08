import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def plot_donut_chart(df, column_name):

    null=df[column_name].isnull().sum()
    total=len(df)
    null_percentage = (null/ total) * 100

    # Create donut chart data
    labels = ['Non-Null Values', 'Null Values']   #    labels = [f'Non-Null Values ({null_percentage:.2f}%)', f'Null Values ({null_percentage:.2f}%)']
    values = [(total-null), null] 

    # Create donut chart figure
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, marker=dict(colors=['#FFD0EC', '#81689D', 'lightgrey']))])

    # # Update layout
    # fig.update_layout(title_text="null val Donut Chart")

    return fig,null_percentage



def column_type_pie(df):

    # Get column names and their types
    column_names = df.columns.tolist()
    column_types = df.dtypes.map(lambda x: 'Categorical' if x == 'object' else 'Numerical').tolist()

    # Create DataFrame for the table
    data = {'Column Name': column_types, 'Column Type': column_names}
    type_df = pd.DataFrame(data)

    # Display the table
    fig_sunburst = px.sunburst(df, path=[column_types, column_names], 
                color=column_types, 
                color_discrete_map={'Categorical': '#FFD0EC', 'Numerical': '#81689D'})


    # Add Sunburst Chart to plots dictionary
    return fig_sunburst


def Plolt_Num_describe(df):
    
    # Plot mean, min, max, count, and std values for all columns
    mean_values = df.mean()
    min_values = df.min()
    max_values = df.max()
    count_values = df.count()
    std_values = df.std()
    
    fig = go.Figure()
    
    # Add traces for mean, min, max, count, and std values
    fig.add_trace(go.Scatter(x=mean_values.index, y=mean_values.values, mode='lines+markers', name='Mean'))
    fig.add_trace(go.Scatter(x=min_values.index, y=min_values.values, mode='lines+markers', name='Min'))
    fig.add_trace(go.Scatter(x=max_values.index, y=max_values.values, mode='lines+markers', name='Max'))
    fig.add_trace(go.Scatter(x=count_values.index, y=count_values.values, mode='lines+markers', name='Count'))
    fig.add_trace(go.Scatter(x=std_values.index, y=std_values.values, mode='lines+markers', name='Standard Deviation'))
    
    fig.update_layout(
        title="Descriptive Statistics of Each Column",
        xaxis_title="Columns",
        yaxis_title="Values"
    )
    
    return fig


def Plolt_cat_describe(df):


    categorical_cols = df.select_dtypes(include='object').columns
    unique_values = [df[col].nunique() for col in categorical_cols]
    counts = [len(df[col]) for col in categorical_cols]
    
    # Create bar graph showing number of unique values and count for each categorical column
    fig = go.Figure()
    fig.add_trace(go.Bar(x=categorical_cols, y=unique_values, name='Unique Values'))
    fig.add_trace(go.Bar(x=categorical_cols, y=counts, name='Count'))
    fig.update_layout(title="Number of Unique Values and Count for Each Categorical Column", xaxis_title="Columns", yaxis_title="Values")
    return fig
