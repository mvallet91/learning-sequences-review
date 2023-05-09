# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import numpy as np
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
        id='interactive-datatable',
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'lineHeight': '15px'
        },
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c, "selectable": True} for c in df.columns],
        filter_action="native",
        filter_options={"placeholder_text": "Filter column..."},
        editable=False,
        sort_action="native",
        sort_mode="single",
        column_selectable="multi",
        row_selectable=False,
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    dcc.Graph(id='sankey-container', style={'width': '95vw'}),
    html.Div(id='datatable-graph-container')
])


# Define the callback function to update the bar chart
@app.callback(
    Output('datatable-graph-container', 'children'),
    Input('interactive-datatable', 'selected_columns'),
    Input('interactive-datatable', "derived_virtual_data"),
)
def update_bar_chart(selected_columns, rows):
    dff = df if rows is None else pd.DataFrame(rows)

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "y": dff[column].value_counts(),
                        "x": dff[column].value_counts().index,
                        "type": "bar",
                        "orientation": 'v',
                        'marker': {'color': 'lightsteelblue'},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 250,
                    "margin": {"t": 50, "l": 50, "r": 50},
                },
            },
        )

        for column in selected_columns if column in dff
    ]


@app.callback(
    Output('sankey-container', 'figure'),
    Input('interactive-datatable', 'selected_columns'),
    Input('interactive-datatable', "derived_virtual_data"),
    Input('interactive-datatable', 'active_cell')
)
def update_sankey_chart(selected_columns, rows, active_cell):
    dff = df if rows is None else pd.DataFrame(rows)
    dimensions = []
    for col in selected_columns:
        dimensions.append({
            'label': col,
            'values': dff[col]
        })

    color = np.zeros(len(dff), dtype='uint8')
    if active_cell:
        active_row_id = active_cell['row']
        color[active_row_id] = 1

    colorscale = [[0, 'lightsteelblue'], [1, 'firebrick']];

    fig = go.Figure(
        go.Parcats(
            dimensions=dimensions,
            tickfont={'size': 14, 'family': 'Times'},
            labelfont={'size': 16, 'family': 'Times'},
            arrangement='freeform',
            line={'colorscale': colorscale, 'cmin': 0,
                  'cmax': 1, 'color': color, 'shape': 'hspline'}
        )
    )

    title = f'{selected_columns} Relationship' if selected_columns else ''
    fig.update_layout(
        title_text=title,
        font_size=12,
        margin=dict(l=250, r=250, t=50, b=20),
    )

    return fig


# @app.callback(
#     Output("sankey-selector", "options"),
#     Input("sankey-selector", "value"),
# )
# def update_multi_options(value):
#     options = [{'label': c, 'value': c} for c in df.columns]
#     if len(value) >= 3:
#         options = [
#             {
#                 "label": option["label"],
#                 "value": option["value"],
#                 "disabled": option["value"] not in value,
#             }
#             for option in options
#         ]
#     return options


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
