import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
df = pd.read_csv('melbourne.csv')

# Data preprocessing
df['Date'] = pd.to_datetime(df['Date'], format='mixed', errors='coerce')
df['M/Y'] = df['Date'].dt.to_period('M').astype(str)
df['Year'] = df['Date'].dt.year
df['Bathroom'] = df['Bathroom'].fillna(0)
df_new = df[
    ['Suburb', 'Rooms', 'Type', 'Price', 'Distance', 'Bathroom', 'Landsize', 'BuildingArea', 'YearBuilt', 'Regionname',
     'M/Y', 'Year']]

st.markdown("""
    <style>
        /* Set the overall background color of the app to black */
        [data-testid="stAppViewContainer"] {
            background-color: #000000;  /* Pure black background */
            color: #00bfff;  /* Light blue text for better readability */
        }

        /* Modify the sidebar */
        [data-testid="stSidebar"] {
            background-color: #111111; /* Slightly lighter black sidebar */
            color: #00bfff; /* Light blue text for the sidebar */
        }

        /* Sidebar header and filter section headings */
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 {
            color: #FFD700;  /* Yellow for filter section headings */
        }

        /* Set KPI containers and headings to yellow */
        [data-testid="metric-container"] {
            background-color: #111111;  /* Darker background for metric containers */
            color: #FFD700;  /* Yellow for KPI text inside metric containers */
            border-radius: 10px; /* Rounded corners for better aesthetics */
        }

        /* Main page headings in yellow */
        h1 {
            font-size: 36px;  /* Large font size for h1 headers */
            color: #FFD700;   /* Yellow for main page titles */
        }

        h2 {
            font-size: 30px;
            color: #FFD700;   /* Yellow for subheaders */
        }

        h3 {
            font-size: 24px;
            color: #FFD700;  /* Yellow text for smaller headers */
        }

        h4 {
            font-size: 20px;
            color: #FFD700;  /* Yellow for even smaller headers */
        }

        /* Adjust font for text across the app */
        * {
            font-family: 'Arial', sans-serif;
        }

        /* Styling buttons */
        button {
            background-color: #222222;  /* Dark gray background for buttons */
            color: #00bfff;  /* Light blue text for buttons */
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }

        /* Modify the font and background of inputs and select boxes */
        input, select {
            background-color: #333333;  /* Darker input background */
            color: #00bfff;  /* Light blue input text */
            border: 1px solid #555555;  /* Subtle border for inputs */
        }

        /* Add hover effects for better interaction */
        input:hover, select:hover, button:hover {
            background-color: #444444;  /* Darker hover effect */
        }

        /* Change the look of the slider */
        [role="slider"] {
            background-color: #666666; /* Dark slider background */
        }

        /* Modify the scrollbar to fit the dark theme */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-thumb {
            background-color: #555555; /* Dark scrollbar handle */
            border-radius: 10px;
        }

        ::-webkit-scrollbar-track {
            background-color: #000000; /* Black scrollbar track */
        }

        /* Adjust Streamlit tables and dataframes */
        [data-testid="stTable"], [data-testid="stDataFrame"] {
            background-color: #111111;  /* Dark background for tables */
            color: #00bfff;  /* Light blue text for tables */
            border: 1px solid #333333;  /* Subtle border for tables */
        }

        /* Hyperlink styling for visibility in dark mode */
        a {
            color: #00bfff; /* Light blue color for hyperlinks */
        }

        a:hover {
            color: #1e90ff; /* Brighter blue on hover */
        }

        /* Page selection headings */
        [data-testid="stSidebar"] label {
            color: #FFD700; /* Yellow for page selection headings */
        }
    </style>
""", unsafe_allow_html=True)


st.sidebar.image('housing-market-.jpg')


page = st.sidebar.selectbox("Select Page", ["KPIs and Main Charts", "Other Charts and Overview", "Price Calculator"])


form1 = st.sidebar.form("Options")
form1.header("Filters")

regions = df['Regionname'].unique()
selected_regions = form1.multiselect("Select Region", regions, default=regions)

types = df['Type'].unique()
selected_type = form1.multiselect("Select Property Type", types, default=types)

year = df['Year'].unique()
select_year = form1.multiselect("Select Year", year, default=year)

rooms = df['Rooms'].unique()
selected_rooms = form1.multiselect("Select Number of Rooms", rooms, default=rooms)

bathroom = df['Bathroom'].unique()
select_bathroom = form1.multiselect("Select Number of Bathrooms", bathroom, default=bathroom)


form1.form_submit_button("Apply")

filtered_data = df[
    (df['Regionname'].isin(selected_regions)) &
    (df['Type'].isin(selected_type)) &
    (df['Rooms'].isin(selected_rooms)) &
    (df['Year'].isin(select_year)) &
    (df['Bathroom'].isin(select_bathroom))
    ]


if page == "Other Charts and Overview":
    st.title("Melbourne Housing - Other Charts and Overview")
    col1, col2 = st.columns([4, 4])


    with col1:
        st.subheader("Price Trending")
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.lineplot(x=filtered_data['Date'], y=filtered_data['Price'], ax=ax)
        ax.set_title("Price Trend Over Time", fontsize=18)
        ax.set_xlabel("Date", fontsize=18)
        ax.set_ylabel("Price", fontsize=18)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.subheader("Price by Region")
        fig3, ax3 = plt.subplots(figsize=(14, 8))
        avg_price_region = filtered_data.groupby('Regionname')['Price'].mean().sort_values()
        sns.barplot(x=avg_price_region.index, y=avg_price_region.values, ax=ax3, palette="viridis")
        ax3.set_title("Average Price by Region", fontsize=18)
        ax3.set_xlabel("Region", fontsize=14)
        ax3.set_ylabel("Average Price", fontsize=14)
        plt.xticks(rotation=45, fontsize=12)
        st.pyplot(fig3)

    with col2:
        st.subheader("Price Vs Land Size")
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.scatterplot(x=filtered_data['Landsize'], y=filtered_data['Price'], hue=filtered_data['Type'], ax=ax)
        ax.set_title("Price Variation According to the Land Size", fontsize=18)
        ax.set_xlabel("Land Size", fontsize=18)
        ax.set_ylabel("Price", fontsize=18)
        st.pyplot(fig)

        st.subheader("Property Type Distribution")
        property_count = filtered_data['Type'].value_counts()
        fig4, ax4 = plt.subplots(figsize=(10, 8))
        ax4.pie(property_count.values, labels=property_count.index, autopct='%1.1f%%', startangle=90,
                colors=sns.color_palette('coolwarm', len(property_count)))
        ax4.set_title("Property Type Distribution", fontsize=18)

        # Equal aspect ratio ensures that pie chart is drawn as a circle.
        ax4.axis('equal')
        st.pyplot(fig4)


elif page == "KPIs and Main Charts":
    st.title("Melbourne Housing - KPIs and Main Charts")


    st.subheader("Key Performance Indicators (KPIs)")


    col1, col2, col3, col4 = st.columns(4)

    avg_price = filtered_data['Price'].mean()
    median_price = filtered_data['Price'].median()
    max_price = filtered_data['Price'].max()
    min_price = filtered_data['Price'].min()


    col1.metric("Average Price", f"${avg_price:,.0f}")
    col2.metric("Median Price", f"${median_price:,.0f}")
    col3.metric("Maximum Price", f"${max_price:,.0f}")
    col4.metric("Minimum Price", f"${min_price:,.0f}")

    col1, col2 = st.columns([4, 4])

    with col1:
        st.subheader("Distance vs Price")
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.scatterplot(x=filtered_data['Distance'], y=filtered_data['Price'], ax=ax)
        ax.set_title("Price Variation by Distance", fontsize=18)
        ax.set_xlabel("Distance (km)", fontsize=18)
        ax.set_ylabel("Price", fontsize=18)
        st.pyplot(fig)


    with col2:
        st.subheader("Building Area vs Price")
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.scatterplot(x=filtered_data['BuildingArea'], y=filtered_data['Price'], ax=ax)
        ax.set_title("Price by Building Area", fontsize=18)
        ax.set_xlabel("Building Area", fontsize=18)
        ax.set_ylabel("Price", fontsize=18)
        st.pyplot(fig)

elif page == "Price Calculator":
    st.title("Price Calculator")

    # User inputs for the calculator
    st.subheader("Enter the details to estimate the price")
    distance = st.number_input("Distance (in km)", min_value=0.0, step=0.1)
    landsize = st.number_input("Land Size (in sqm)", min_value=0.0, step=1.0)
    building_area = st.number_input("Building Area (in sqm)", min_value=0.0, step=1.0)

    estimated_price = (distance * 10000) + (landsize * 300) + (building_area * 500)

    st.subheader(f"Estimated Price: ${estimated_price:,.0f}")
