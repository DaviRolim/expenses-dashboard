import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

def create_dashboard(data):
    """
    Create an interactive dashboard using the analyzed data.
    
    Args:
    data (pd.DataFrame): Analyzed data to be displayed.
    """
    # Sort the data by month
    data['month'] = pd.to_datetime(data['month'])
    data = data.sort_values('month')

    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.H1("Financial Report Dashboard"),
        dcc.Graph(id='monthly-total-graph'),
    ])

    @app.callback(
        Output('monthly-total-graph', 'figure'),
        Input('monthly-total-graph', 'relayoutData')
    )
    def update_graph(relayout_data):
        fig = px.bar(data, x='month', y='total_amount', title='Total Amount by Month')
        fig.update_xaxes(tickformat="%Y-%m")
        return fig

    app.run_server(debug=True)
