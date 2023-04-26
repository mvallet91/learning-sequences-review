# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
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
    html.Div(id='datatable-interactivity-container')
])


# import plotly.graph_objects as go
#
# # Define the Sankey figure using plotly.graph_objects
# sankey_fig = go.Figure(data=[go.Sankey(
#     node=dict(
#       pad=15,
#       thickness=20,
#       line=dict(color="black", width=0.5),
#       label=df['Category']
#     ),
#     link=dict(
#       source=df['Source'],
#       target=df['Target'],
#       value=df['Value']
#   ))])
#
# # Define the app layout
# app.layout = html.Div([
#     dash_table.DataTable(
#         style_data={
#             'whiteSpace': 'normal',
#             'height': 'auto',
#             'lineHeight': '15px'
#         },
#         data=df.to_dict('records'),
#         columns=[{'id': c, 'name': c} for c in df.columns],
#         filter_action="native",
#         filter_options={"placeholder_text": "Filter column..."},
#         editable=False,
#         sort_action="native",
#         sort_mode="multi",
#         column_selectable="single",
#         row_selectable="multi",
#         row_deletable=True,
#         selected_columns=[],
#         selected_rows=[],
#         page_action="native",
#         page_current=0,
#         page_size=10,
#     ),
#     dcc.RadioItems(
#         id='column-selector',
#         options=[{'label': c, 'value': c} for c in df.columns],
#         value=df.columns[0],
#         labelStyle={'display': 'inline-block'}
#     ),
#     dcc.Graph(id='sankey-graph', figure=sankey_fig)
# ])
#
#
# # Define the callback function to update the Sankey figure
# @app.callback(
#     Output('sankey-graph', 'figure'),
#     Input('column-selector', 'value'))
# def update_sankey(selected_column):
#     filtered_df = df[['Source', 'Target', selected_column]]
#     filtered_df = filtered_df.groupby(['Source', 'Target', selected_column]).sum().reset_index()
#     fig = go.Figure(data=[go.Sankey(
#         node=dict(
#           pad=15,
#           thickness=20,
#           line=dict(color="black", width=0.5),
#           label=df['Category']
#         ),
#         link=dict(
#           source=filtered_df['Source'],
#           target=filtered_df['Target'],
#           value=filtered_df[selected_column]
#       ))])
#     return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
