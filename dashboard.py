import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go

def create_dashboard(data):
    """
    Create an interactive dashboard using the analyzed data.
    
    Args:
    data (pd.DataFrame): Analyzed data to be displayed.
    """
    # Sort the data by month
    data['month'] = pd.to_datetime(data['month'])
    data = data.sort_values('month')

    # Prepare data for top 10 purchases
    top_10_purchases = pd.concat([df for df in data['top_10_purchases']])
    top_10_purchases = top_10_purchases.nlargest(10, 'amount')

    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.H1("Financial Report Dashboard"),
        dcc.Graph(id='monthly-total-graph'),
        dcc.Graph(id='top-10-purchases-graph'),
    ])

    @app.callback(
        Output('monthly-total-graph', 'figure'),
        Input('monthly-total-graph', 'relayoutData')
    )
    def update_graph(relayout_data):
        fig = px.bar(data, x='month', y='total_amount', title='Total Amount by Month')
        fig.update_xaxes(tickformat="%Y-%m")
        return fig

    @app.callback(
        Output('top-10-purchases-graph', 'figure'),
        Input('top-10-purchases-graph', 'relayoutData')
    )
    def update_top_10_graph(relayout_data):
        top_10_purchases = data['top_10_purchases'].iloc[0]
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=top_10_purchases['amount'],
            y=top_10_purchases['title'],
            text=top_10_purchases['date'].dt.strftime('%Y-%m-%d'),
            orientation='h'
        ))
        
        fig.update_traces(textposition='inside')
        fig.update_layout(
            title='Top 10 Most Expensive Purchases',
            yaxis={'categoryorder':'total ascending'},
            xaxis_title='Amount',
            yaxis_title='Description'
        )
        return fig

    return app

# Remove the app.run_server(debug=True) line from here
