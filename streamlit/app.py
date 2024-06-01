import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk
from sklearn.preprocessing import StandardScaler
import io

# Load the dataset
df = pd.read_csv('dataset/incidents.csv')  # make sure to link the dataset perfectly

# Data cleaning steps
df['open_date'] = pd.to_datetime(df['open_date'])
df['threat'] = df['threat'].fillna('Unknown')
df['location'] = df['location'].fillna('Unknown Location')
df['description'] = df['description'].fillna('No description available')
df['commodity'] = df['commodity'].fillna('Unknown')
df['tags'] = df['tags'].fillna('No tags')
boolean_columns = ['measure_skim', 'measure_shore', 'measure_bio', 'measure_disperse', 'measure_burn']
df[boolean_columns] = df[boolean_columns].fillna(0)
df['max_ptl_release_gallons'] = df['max_ptl_release_gallons'].fillna(df['max_ptl_release_gallons'].median())
df['year'] = df['open_date'].dt.year

st.sidebar.title("US Oil Spill Visualization")
option = st.sidebar.selectbox(
    'Select Visualization Type',
    ['Data Overview', 'Threat Analysis', 'Yearly Incidents', 'Geospatial Visualization']
)

if option == 'Data Overview':
    st.header('Data Overview')
    st.write("This section provides a comprehensive overview of the dataset, including a preview of the entire dataset, summary statistics, and null values in the dataset.")
    
    st.subheader('Dataset Preview')
    st.dataframe(df)
    
    st.subheader('Summary Statistics')
    st.write(df.describe())
    
    st.subheader('Null Values in the Dataset')
    st.write(df.isnull().sum())
    
    st.subheader('Basic Information')
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

if option == 'Threat Analysis':
    st.header('Threat Analysis')
    st.write("This section shows the distribution of incidents by threat type.")
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='threat', order=df['threat'].value_counts().index)
    plt.xticks(rotation=45)
    plt.title('Number of Incidents by Threat Type')
    st.pyplot(plt)

if option == 'Yearly Incidents':
    st.header('Yearly Incidents')
    st.write("This section shows the number of incidents recorded each year, allowing us to observe trends over time.")
    st.write(
        '''
        From this chart, we can observe trends over time.

        Here are some key points:

        - **Peak Years**: There is a noticeable peak in incidents during the years 2017, 2008, and 2016.
        - **Recent Decline**: The number of incidents appears to decline in recent years, particularly after 2017.
        - **Historical Data**: There are fewer recorded incidents before the 1980s, which could be due to less comprehensive reporting during those times.
        '''
    )
    plt.figure(figsize=(14, 8))
    sns.countplot(data=df, x='year', order=df['year'].value_counts().index)
    plt.xticks(rotation=90)
    plt.title('Number of Incidents by Year')
    st.pyplot(plt)

if option == 'Geospatial Visualization':
    st.header('Geospatial Visualization')
    st.write("This section provides geospatial visualizations of the incidents, including scatter plots and heatmaps, to show the geographical distribution of incidents.")

    # Add slider for selecting year range
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    year_range = st.slider('Select Year Range', min_year, max_year, (min_year, max_year))

    # Filter dataset based on selected year range
    df_filtered = df[(df['year'] >= year_range[0]) && (df['year'] <= year_range[1])]

    # Scatter plot of all incidents
    scatter_layer = pdk.Layer(
        'ScatterplotLayer',
        data=df_filtered,
        get_position='[lon, lat]',
        get_radius=50000,
        get_color='[200, 30, 0, 160]',
        pickable=True
    )

    # Heatmap of incidents
    heatmap_layer = pdk.Layer(
        'HeatmapLayer',
        data=df_filtered,
        get_position='[lon, lat]',
        get_weight='max_ptl_release_gallons',
        radius_pixels=60
    )

    # Impact analysis
    scaler = StandardScaler()
    df_filtered['scaled_release_gallons'] = scaler.fit_transform(df_filtered[['max_ptl_release_gallons']]) * 10000 #adjust to make the visualizations better
    impact_layer = pdk.Layer(
        'ScatterplotLayer',
        data=df_filtered,
        get_position='[lon, lat]',
        get_radius='scaled_release_gallons',
        get_color='[200, 30, 0, 160]',
        pickable=True,
        auto_highlight=True
    )

    view_state = pdk.ViewState(
        latitude=37.7749,
        longitude=-122.4194,
        zoom=4,
        pitch=50
    )

    # Threat analysis
    def get_threat_color(threat):
        colors = {
            'Oil': [255, 0, 0],
            'Chemical': [0, 255, 0],
            'Other': [0, 0, 255],
            'Unknown': [128, 128, 128]
        }
        return colors.get(threat, [128, 128, 128])

    df_filtered['threat_color'] = df_filtered['threat'].apply(get_threat_color)

    map_type = st.selectbox("Select Map Type", ["Scatter Plot", "Heatmap", "Impact Analysis", "Threat Analysis"])

    if map_type == "Scatter Plot":
        st.pydeck_chart(pdk.Deck(layers=[scatter_layer], initial_view_state=view_state, width=800, height=600))
    elif map_type == "Heatmap":
        st.pydeck_chart(pdk.Deck(layers=[heatmap_layer], initial_view_state=view_state, width=800, height=600))
    elif map_type == "Impact Analysis":
        st.pydeck_chart(pdk.Deck(layers=[impact_layer], initial_view_state=view_state, width=800, height=600))
    elif map_type == "Threat Analysis":
        st.subheader("Select Threat Types")
        threat_types = df_filtered['threat'].unique()
        selected_threats = st.multiselect('Threat Types', threat_types, default=threat_types)

        filtered_df = df_filtered[df_filtered['threat'].isin(selected_threats)]
        filtered_df['threat_color'] = filtered_df['threat'].apply(get_threat_color)

        threat_layer = pdk.Layer(
            'ScatterplotLayer',
            data=filtered_df,
            get_position='[lon, lat]',
            get_fill_color='[threat_color[0], threat_color[1], threat_color[2], 150]',
            get_radius=50000,
            pickable=True,
            auto_highlight=True
        )

        threat_tooltip = {"text": "{name}\nLocation: {location}\nThreat: {threat}"}
        threat_deck = pdk.Deck(layers=[threat_layer], initial_view_state=view_state, tooltip=threat_tooltip)
        st.pydeck_chart(threat_deck)
