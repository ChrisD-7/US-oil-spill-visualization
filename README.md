# Interactive Incident Impact Analysis

This project creates an interactive visualization of oil spill incidents using PyDeck. Inspired by the need for job-ready projects and the compelling map-based storytelling by Jonny Harris, this project uses a dataset from [Kaggle](https://www.kaggle.com/datasets/kkhandekar/oil-spills-off-us-coastal-waters/data).

## Project Overview

The project explores and visualizes oil spill incidents using PyDeck for map-based visualizations and Streamlit for interactive web applications. It covers data loading, cleaning, exploratory data analysis (EDA), and creating various visualizations including scatter plots, heatmaps, impact analysis, threat-specific analysis, and time-based animations.


## Data Collection

The dataset comprises oil spill incidents off US coastal waters where NOAA's Office of Response and Restoration (OR&R) provided scientific support for the spill response. The dataset includes features such as incident name, location, latitude, longitude, threat type, commodity spilled, and various response measures.

## Data Processing

### Data Cleaning
- Dropped rows with missing latitude or longitude.
- Converted `open_date` to datetime format.
- Filled missing values in `threat` with 'Unknown'.
- Filled missing values in other columns with appropriate placeholders.

### Feature Engineering
- Standardized the `max_ptl_release_gallons` using `StandardScaler`. # the only sklearn package used

### Exploratory Data Analysis (EDA)
- Analyzed the distribution of `max_ptl_release_gallons`.
- Visualized the count of incidents by threat type and year.

## Visualizations

### PyDeck Visualizations
1. **Scatter Plot**: Visualizes all incidents on a map.
2. **Heatmap**: Shows the density of incidents based on `max_ptl_release_gallons`.
3. **Impact Analysis**: Highlights incidents based on the standardized potential release in gallons.
4. **Threat-Specific Analysis**: Differentiates incidents by threat type using color coding.

## Requirements

To run the project, install the following packages:
```bash
pip install pandas matplotlib seaborn scikit-learn pydeck 
```

## Running the Streamlit Application

Save the following script as `app.py` and run it using:
```bash
streamlit run app.py
```

## Contributing

Contributions are welcome. Please fork the repository, make your changes, and submit a pull request. For major changes, open an issue to discuss what you would like to change.

## References

- [PyDeck Example on Kaggle](https://www.kaggle.com/code/jeongbinpark/visualization-3d-map-using-pydeck)
- [Kaggle Dataset](https://www.kaggle.com/datasets/kkhandekar/oil-spills-off-us-coastal-waters/data)
