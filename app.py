# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Incorporate data
df = pd.read_excel('data/ArticlesByCategory.xlsx', sheet_name='Sheet1')

# Initialize the app
app = Dash(__name__)
server = app.server


# App layout
app.layout = html.Div([
    dash_table.DataTable(
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'lineHeight': '15px'
        },
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        filter_action="native",
        filter_options={"placeholder_text": "Filter column..."},
        editable=False,
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    dcc.RadioItems(
        id='column-selector',
        options=[{'label': c, 'value': c} for c in df.columns],
        value=df.columns.values[0],
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id='bar-chart'),

    dcc.Checklist(
        id='sankey-selector',
        options=[{'label': c, 'value': c} for c in df.columns],
        value=['Task', 'Purpose'],
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id='sankey')
])


# Define the callback function to update the bar chart
@app.callback(
    Output('bar-chart', 'figure'),
    Input('column-selector', 'value'))
def update_bar_chart(selected_column):
    # Create a count of each unique value in the selected column
    value_counts = df[selected_column].value_counts()

    # Create the bar chart
    fig = go.Figure(data=[go.Bar(
        x=value_counts,
        y=value_counts.index,
        orientation='h'
    )])

    # Update the layout
    fig.update_layout(
        title=f'{selected_column} distribution',
        xaxis_title='Count',
        yaxis_title=selected_column
    )

    return fig


@app.callback(
    Output('sankey', 'figure'),
    Input('sankey-selector', 'value'))
def update_sankey_chart(selected_columns):
    dimensions = []
    for col in selected_columns:
        dimensions.append({
            'label': col,
            'values': df[col]
        })

    fig = go.Figure(go.Parcats(
        dimensions=dimensions
    ))

    title = f'{selected_columns} Relationship'
    fig.update_layout(title_text=title, font_size=10)
    return fig


@app.callback(
    Output("sankey-selector", "options"),
    Input("sankey-selector", "value"),
)
def update_multi_options(value):
    options = [{'label': c, 'value': c} for c in df.columns]
    if len(value) >= 3:
        options = [
            {
                "label": option["label"],
                "value": option["value"],
                "disabled": option["value"] not in value,
            }
            for option in options
        ]
    return options


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
