from dash import Dash, dash_table, Input, Output, dcc, html
import pandas as pd
import os
from flask import session
import dash_leaflet as dl  # for interactive map
import matplotlib.cm as cm
import matplotlib.colors as colors
import dash_dangerously_set_inner_html 

# Dictionary for translations (german data from immoscout to english UI)
feature_name_translation = {
    'Balkon': 'Balcony',
    'Garage': 'Garage',
    'Parkplatz': 'Parking',
    'Neubau': 'Newly Built',
    'Swimmingpool': 'Swimming Pool',
    'Lift': 'Elevator',
    'Aussicht': 'View',
    'Cheminée': 'Fireplace',
    'Rollstuhlgängig': 'Wheelchair Accessible',
    'Kinderfreundlich': 'Child Friendly',
    'Kabel-TV': 'Cable TV',
    'Minergie Bauweise': 'Minergie Building',
    'Minergie zertifiziert': 'Minergie Certified'
}

# Function to load property data from csv file
def load_property_data():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'dat_clean.csv')
    df = pd.read_csv(data_path)
    # Ensure coordinates are numeric
    df['lat'] = pd.to_numeric(df['lat'])
    df['long'] = pd.to_numeric(df['long'])
    # Drop missing values
    df = df.dropna(subset=['lat', 'long'])
    return df

# Function to compute table output
def calculate_averages(df, columns):
    # Compute average values
    avg_values = df[columns].mean()
    avg_values = pd.DataFrame(avg_values).transpose()  # Convert to df
    # Round values
    avg_values = avg_values.round({'living_area': 0, 'Balkon': 0, 'Garage': 0, 'Parkplatz': 0, 'price': 0, 'Neubau': 0,
                                   'Swimmingpool': 0, 'Lift': 0, 'Aussicht': 0, 'Cheminée': 0, 'Rollstuhlgängig': 0,
                                   'Kinderfreundlich': 0, 'Kabel-TV': 0, 'Minergie Bauweise': 0, 'Minergie zertifiziert': 0})  # Round to 0 decimal points
    # Convert binary variables to yes/no depending on their value 1/0
    for column in ['Balkon', 'Garage', 'Parkplatz', 'Neubau', 'Swimmingpool', 'Lift', 'Aussicht', 'Cheminée', 'Rollstuhlgängig',
                   'Kinderfreundlich', 'Kabel-TV', 'Minergie Bauweise', 'Minergie zertifiziert']:  ######################## VARIABLES
        avg_values[column] = avg_values[column].apply(lambda x: 'Yes' if x == 1 else 'No')
    # Convert back to series and then dict
    avg_values = avg_values.iloc[0]
    return avg_values.to_dict()

# Function to compute quantiles and return a colormap (used for interactive map)
def get_color_map(df, n_quantiles=10, palette="plasma"):
    # Fix the quantile values extraction to ensure correct indexing
    quantile_values = df['price'].quantile([i / n_quantiles for i in range(n_quantiles + 1)]).values

    def get_quantile_category(price):
        for i in range(len(quantile_values) - 1):
            if quantile_values[i] <= price < quantile_values[i + 1]:
                return i
        return len(quantile_values) - 2

    colormap = cm.get_cmap(palette, n_quantiles)
    colors_map = [colors.to_hex(colormap(i / (n_quantiles - 1))) for i in range(n_quantiles)]

    def color_code(price):
        quantile_category = get_quantile_category(price)
        return colors_map[quantile_category]

    return color_code, quantile_values, colors_map

# Function to create the predicted price range graph
def create_static_price_range_graph(min_value, max_value):
    svg_content = f'''
        <svg width="400px" height="100px">
            <!-- Circles -->
            <circle cx="25%" cy="50%" r="8" fill="#3498db"/>
            <circle cx="75%" cy="50%" r="8" fill="#3498db"/>

            <!-- Connecting Line -->
            <line x1="25%" y1="50%" x2="75%" y2="50%" stroke="#3498db" stroke-width="4"/>

            <!-- Texts for Min and Max Values -->
            <text x="25%" y="35%" font-size="14" text-anchor="middle" fill="#333">CHF {min_value:,}</text>
            <text x="75%" y="35%" font-size="14" text-anchor="middle" fill="#333">CHF {max_value:,}</text>
        </svg>
    '''
    return html.Div(
        children=dash_dangerously_set_inner_html.DangerouslySetInnerHTML(svg_content),
        style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'margin-top': '10px'}
    )

# Function to create a textual message with arguments
def create_property_info_text(percentile, total_listings):
    text_content = f"Congratulations, based on the predicted price your property belongs to the <strong>top {percentile}%</strong> among <strong>{total_listings} listings </strong>on Immoscout24.ch!"

    return html.Div(
        children=dash_dangerously_set_inner_html.DangerouslySetInnerHTML(text_content),
        style={
            'padding': '15px',
            'font-size': '16px',
            'color': 'black',
            'background-color': 'white',
            'border': '1px solid black',
            'border-radius': '5px',
            'box-shadow': '2px 2px 10px rgba(0, 0, 0, 0.1)',
            'margin-top': '20px'
        }
    )

# Function to calculate the percentile rank
def calculate_percentile(price, prices):
    count_below = sum(p < price for p in prices)
    percentile = (count_below / len(prices)) * 100
    return str(round(100 - percentile,0))

# Create Dash app
def create_dash_app(flask_app):
    # Style sheet to make app look more modern
    external_stylesheets = ["https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"]
    dash_app = Dash(__name__, server=flask_app, routes_pathname_prefix='/dash_analytics/', external_stylesheets=external_stylesheets)

    # Load data
    df = load_property_data()

    # Columns of data to include (for the table)
    columns_to_include = ['price', 'living_area', 'Balkon', 'Garage', 'Parkplatz', 'Neubau', 'Swimmingpool', 'Lift', 'Aussicht', 'Cheminée', 'Rollstuhlgängig',
                          'Kinderfreundlich', 'Kabel-TV', 'Minergie Bauweise', 'Minergie zertifiziert']  ######################## VARIABLES
    avg_data = calculate_averages(df, columns_to_include)

    # Compute quantiles and get color map
    color_code, quantile_values, colors_map = get_color_map(df)

    # Markers for properties
    property_markers = [
        dl.CircleMarker(center=[row['lat'], row['long']], fill=True, fillColor=color_code(row["price"]), color=color_code(row["price"]),
                        stroke=True, fillOpacity=0.9, radius=5, children=[dl.Tooltip(f"CHF {int(row['price']):,}")]) for _, row in df.iterrows()
    ]

    # Create a function to return the user's property coordinates
    def get_my_property_coords():
        property_data = session.get('property_data', {})
        lat = property_data.get('lat', 47.6648435)  # default placeholder if not found
        long = property_data.get('long', 8.7022888)  # default placeholder if not found
        return [lat, long]

    # Create a custom legend based on quantiles
    legend_items = [html.Div([
        html.Span(style={'backgroundColor': colors_map[i], 'display': 'inline-block', 'width': '15px', 'height': '8px'}),
        f" CHF {quantile_values[i]:,.0f} - CHF {quantile_values[i + 1]:,.0f}"
    ]) for i in range(len(colors_map))]
    legend = html.Div([
        html.H5("Property Prices (deciles)", style={'font-size': '14px', 'margin': '0px 0px 10px 0px'}),
        *legend_items
    ], style={'position': 'absolute', 'bottom': '2px', 'right': '2px', 'padding': '5px', 'font-size': '12px', 'backgroundColor': 'white', 'border': '1px solid black', 'zIndex': '1000'})

    # Values for text in text box
    x1 = len(df)  # Total amount of listings

    # App layout
    dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div([
            html.Div([
                html.H5("Your Property's Predicted Price Range", style={'textAlign': 'center', 'margin-bottom': '15px'}),
                html.Div(id='price-range-graph'),
                html.H5("Comparison to the Market", style={'textAlign': 'center', 'margin-bottom': '15px'}),
                html.Div(id='data-table-container', style={'padding': '10px', 'margin-top': '20px'}),
            ], style={'flex': '1', 'padding': '20px', 'margin-right': '5px'}),  # Left column for the table

            html.Div([
                html.H5("Current Listings", style={'textAlign': 'center', 'margin-bottom': '15px'}),
                dl.Map(center=[df['lat'].mean(), df['long'].mean()], zoom=10, children=[
                    dl.TileLayer(),
                    dl.LayersControl(id='layers-control'),
                    legend  # Adjusted legend size and position
                ], style={'height': '500px', 'width': '110%'})  # Increased height and width
            ], style={'flex': '1', 'padding': '30px', 'margin-left': '5px'})  # Right column for the map
        ], style={'display': 'flex', 'flex-direction': 'row', 'width': '100%', 'padding': '20px'}),  # Adjusted main layout

        # Adding text block below table and map
        html.Div([
            html.Div(id='property-info-text')
        ], style={'padding': '20px', 'width': '100%'})
    ])

    # Callback to update table with user input
    @dash_app.callback(
        [Output('data-table-container', 'children'),
         Output('price-range-graph', 'children'),
         Output('layers-control', 'children'),
         Output('property-info-text', 'children')],
        [Input('url', 'pathname')]  # Trigger on page load
    )
    def update_table_and_price_range_graph(pathname):
        # Retrieve property data from session (inside the request context)
        my_property_data = session.get('property_data', {})

        # Prepare data for the table
        rows = []
        for col in columns_to_include:
            your_property_value = my_property_data.get(col, 'N/A')
            english_col_name = feature_name_translation.get(col, col)  # Translate names to English

            # Format price values
            if col == 'price':
                your_property_value = my_property_data.get('predicted_price', 'N/A')
                if your_property_value != 'N/A':
                    your_property_value = f"CHF {int(your_property_value):,}"
                avg_value = f"CHF {int(avg_data[col]):,}"
            # Append "m²" for living_area
            elif col == 'living_area':
                if your_property_value != 'N/A':
                    your_property_value = f"{int(your_property_value)} m²"
                avg_value = f"{int(avg_data[col])} m²"
            else:
                avg_value = avg_data[col] if col in avg_data else 'N/A'

            rows.append({
                '': english_col_name,
                'Your Property': your_property_value,
                'Average Property': avg_value
            })

        table_df = pd.DataFrame(rows)

        # Adjusting the table style
        table_component = dash_table.DataTable(
            id='data-table',
            columns=[{"name": col, "id": col} for col in table_df.columns],
            data=table_df.to_dict('records'),
            style_table={'width': '90%', 'margin': 'auto', 'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)'},  # Modern box shadow and table width
            style_cell={'textAlign': 'left', 'padding': '10px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '14px'},  # Modern font and size
            style_header={
                "fontWeight": "bold",
                'fontSize': '15px', 'textAlign': 'center', 'backgroundColor': '#f2f2f2', 'borderBottom': '2px solid #d9d9d9'
            },  # Modern header style
            style_as_list_view=True,
            page_size=10  # Limit page size to 10 rows
        )

        # Update price range graph
        price_lower = my_property_data.get('price_lower', 0)
        price_upper = my_property_data.get('price_upper', 0)
        price_range_graph = create_static_price_range_graph(price_lower, price_upper)

        # Retrieve my_property_coords within the callback
        my_property_coords = get_my_property_coords()
        house_icon = dict(iconUrl="/static/home.png", iconSize=[28, 28], iconAnchor=[16, 32])
        my_property_marker = dl.Marker(position=my_property_coords, icon=house_icon, children=[
            dl.Tooltip("Your Property")
        ])

        # Create the updated markers including user's property marker
        updated_property_markers = [
            dl.CircleMarker(center=[row['lat'], row['long']], fill=True, fillColor=color_code(row["price"]), color=color_code(row["price"]),
                            stroke=True, fillOpacity=0.9, radius=5, children=[dl.Tooltip(f"CHF {int(row['price']):,}")]) for _, row in df.iterrows()
        ] + [my_property_marker]
        property_markers_layer = dl.LayerGroup(updated_property_markers)

        # Calculate the percentile rank
        predicted_price = my_property_data.get('predicted_price', 0)
        percentile = calculate_percentile(predicted_price, df['price'].values)

        # Update property info text
        property_info_text = create_property_info_text(percentile, x1)

        return table_component, price_range_graph, property_markers_layer, property_info_text

    return dash_app
