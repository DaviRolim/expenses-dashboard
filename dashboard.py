import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime

def create_dashboard(data, top_10_purchases):
    """
    Create an interactive dashboard using the analyzed data.
    
    Args:
    data (pd.DataFrame): Analyzed data to be displayed.
    top_10_purchases (pd.DataFrame): Top 10 most expensive purchases.
    """
    # Sort the data by month
    data['month'] = pd.to_datetime(data['month'])
    data = data.sort_values('month')

    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.H1("Financial Report Dashboard"),
        dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed=data['month'].min().date(),
            max_date_allowed=data['month'].max().date(),
            start_date=data['month'].min().date(),
            end_date=data['month'].max().date(),
        ),
        dcc.Graph(id='monthly-total-graph'),
        dcc.Graph(id='top-10-purchases-graph'),
    ])

    @app.callback(
        [Output('monthly-total-graph', 'figure'),
         Output('top-10-purchases-graph', 'figure')],
        [Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')]
    )
    def update_graphs(start_date, end_date):
        filtered_data = data[(data['month'] >= start_date) & (data['month'] <= end_date)]
        
        # Monthly total graph
        monthly_fig = px.bar(filtered_data, x='month', y='total_amount', title='Total Amount by Month')
        monthly_fig.update_traces(y=abs(filtered_data['total_amount']))
        monthly_fig.update_xaxes(tickformat="%Y-%m")
        
        # Top 10 purchases graph
        filtered_top_10 = top_10_purchases[
            (top_10_purchases['date'] >= start_date) & 
            (top_10_purchases['date'] <= end_date)
        ]
        
        top_10_fig = go.Figure()
        top_10_fig.add_trace(go.Bar(
            x=filtered_top_10['amount'],
            y=filtered_top_10['title'],
            text=filtered_top_10['date'].dt.strftime('%Y-%m-%d'),
            orientation='h'
        ))
        
        top_10_fig.update_traces(textposition='inside')
        top_10_fig.update_layout(
            title='Top 10 Most Expensive Purchases',
            yaxis={'categoryorder':'total ascending'},
            xaxis_title='Amount',
            yaxis_title='Description'
        )
        
        return monthly_fig, top_10_fig

    return app

# Remove the app.run_server(debug=True) line from here
