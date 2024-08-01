import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime
import calendar

def create_dashboard(data, top_10_purchases, monthly_top_5):
    """
    Create an interactive dashboard using the analyzed data.
    
    Args:
    data (pd.DataFrame): Analyzed data to be displayed.
    top_10_purchases (pd.DataFrame): Top 10 most expensive purchases.
    monthly_top_5 (dict): Dictionary containing top 5 expenses for each month.
    """
    # Sort the data by month
    data['month'] = pd.to_datetime(data['month'])
    data = data.sort_values('month')

    app = dash.Dash(__name__)

    # Create a list of month options for the dropdown
    month_options = [{'label': f"{calendar.month_name[d.month]} {d.year}", 'value': d.strftime('%Y-%m')} 
                     for d in data['month'].dt.to_period('M').unique()]

    app.layout = html.Div([
        html.H1("Financial Report Dashboard"),
        dcc.Dropdown(
            id='month-range-dropdown',
            options=month_options,
            multi=True,
            value=[option['value'] for option in month_options],  # Select all months by default
            placeholder="Select month(s)",
        ),
        dcc.Graph(id='monthly-total-graph'),
        dcc.Graph(id='top-10-purchases-graph'),
        html.Div(id='monthly-top-5-expenses')
    ])

    @app.callback(
        [Output('monthly-total-graph', 'figure'),
         Output('top-10-purchases-graph', 'figure'),
         Output('monthly-top-5-expenses', 'children')],
        [Input('month-range-dropdown', 'value')]
    )
    def update_graphs(selected_months):
        if not selected_months:
            filtered_data = data
            filtered_top_10 = top_10_purchases
            selected_monthly_top_5 = monthly_top_5
        else:
            filtered_data = data[data['month'].isin(selected_months)]
            filtered_top_10 = top_10_purchases[top_10_purchases['date'].dt.strftime('%Y-%m').isin(selected_months)]
            selected_monthly_top_5 = {k: v for k, v in monthly_top_5.items() if k in selected_months}
        
        # Monthly total graph
        monthly_fig = px.bar(filtered_data, x='month', y='total_amount', title='Total Amount by Month')
        monthly_fig.update_traces(y=abs(filtered_data['total_amount']))
        monthly_fig.update_xaxes(tickformat="%Y-%m")
        
        # Top 10 purchases graph
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
        
        # Generate monthly top 5 expenses charts
        monthly_top_5_charts = []
        sorted_months = sorted(selected_monthly_top_5.keys(), reverse=True)
        for month in sorted_months:
            top_5_expenses = selected_monthly_top_5[month]
            top_5_expenses = top_5_expenses.sort_values('amount', ascending=False)
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=top_5_expenses['amount'],
                y=top_5_expenses['title'],
                orientation='h',
                text=top_5_expenses['amount'].round(2),
                textposition='outside'
            ))
            fig.update_layout(
                title=f'Top 5 Expenses for {pd.to_datetime(month).strftime("%B %Y")}',
                yaxis={'categoryorder':'array', 'categoryarray': top_5_expenses['title'][::-1]},
                xaxis_title='Amount',
                yaxis_title='Description',
                height=300,
                margin=dict(l=0, r=0, t=30, b=0)
            )
            
            monthly_top_5_charts.append(dcc.Graph(figure=fig))
        
        return monthly_fig, top_10_fig, monthly_top_5_charts

    return app

# Remove the app.run_server(debug=True) line from here
