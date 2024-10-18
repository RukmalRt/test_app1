import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.markdown(
    """
    <style>
    /* Set background color to light blue and grey mix */
    .stApp {
        background-color: #EAF2F8;  /* Light Blue */
        background-image: linear-gradient(135deg, #EAF2F8 40%, #BDC3C7 100%);  /* Light blue to grey gradient */
    }

    /* Set sidebar background color to dark grey */
    .css-1d391kg {
        background-color: #2E2E2E !important;  /* Dark Grey */
    }

    /* Style for sidebar titles and texts (white) */
    .css-1vbd788, .css-j7qwjs, .css-1vencpc {
        color: white !important;  /* Make sidebar text white */
    }

    /* Style for the main section titles (dark grey) */
    .css-10trblm {
        color: #2C3E50 !important;  /* Darker grey for the main section titles */
    }

    /* Style for KPI metric numbers */
    .css-2trqyj {
        font-size: 2rem !important;  /* Increase KPI font size */
        color: #34495E !important;   /* Dark blue-grey */
    }
    </style>
    """,
    unsafe_allow_html=True
)
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

st.sidebar.image('housing-market-.jpg')


page = st.sidebar.selectbox("Select Page", ["KPIs and Main Features", "Charts and Overview", "Deap Analysis"])


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

df = df[df['Price'].notnull() & df['Year'].notnull()]
# Group by Suburb and Year, then calculate the average price for each Suburb in each Year


form1.form_submit_button("Apply")

filtered_data = df[
    (df['Regionname'].isin(selected_regions)) &
    (df['Type'].isin(selected_type)) &
    (df['Rooms'].isin(selected_rooms)) &
    (df['Year'].isin(select_year)) &
    (df['Bathroom'].isin(select_bathroom)) &
    (df['Price'])]

avg_price_per_year = filtered_data.groupby(['Suburb', 'Year'])['Price'].mean().unstack()

rows = []

# Loop through each Suburb to calculate changes
for suburb in avg_price_per_year.index:
    avg_price_2016 = avg_price_per_year.iloc[avg_price_per_year.index.get_loc(suburb), 0]  # First year price
    avg_price_2017 = avg_price_per_year.iloc[avg_price_per_year.index.get_loc(suburb), 1]  # Second year price

    # Calculate the price change and percentage change
    price_change = avg_price_2016 - avg_price_2017
    pct_change = (price_change / avg_price_2016) * 100 if avg_price_2016 != 0 else 0

    # Add data as a dictionary to the list
    rows.append({
        'Suburb': suburb,
        '2016 Price': avg_price_2016,
        '2017 Price': avg_price_2017,
        'Price Change': price_change,
        'Percentage Change (%)': pct_change
    })

# Convert the list of dictionaries into a DataFrame
price_change_df = pd.DataFrame(rows)

# Round values for better readability
price_change_df = price_change_df.round(2)
price_change_df = price_change_df.sort_values(by='Percentage Change (%)', ascending=False)

top_5_price_change = price_change_df.nlargest(5, 'Price Change')
top_5_pct_change = price_change_df.nlargest(5, 'Percentage Change (%)')

if page == "Charts and Overview":
    st.title("Melbourne Housing - Charts and Overview")
    col1, col2 = st.columns([4, 4])


    with col1:
        st.subheader("Price by Region and Room Count")
        heatmap_data = df.pivot_table(values='Price', index='Rooms', columns='Regionname', aggfunc='mean')
        fig1, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="coolwarm", ax=ax)
        ax.set_title("Average Price Heatmap (Region vs. Rooms)")
        st.pyplot(fig1)

        st.subheader("Distance vs Price")
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.scatterplot(x=filtered_data['Distance'], y=filtered_data['Price'], ax=ax)
        ax.set_title("Price Variation by Distance", fontsize=18)
        ax.set_xlabel("Distance (km)", fontsize=18)
        ax.set_ylabel("Price", fontsize=18)
        st.pyplot(fig)

    with col2:
        st.subheader("Price Vs Land Size")
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.scatterplot(x=filtered_data['Landsize'], y=filtered_data['Price'], hue=filtered_data['Type'], ax=ax)
        ax.set_title("Price Variation According to the Land Size", fontsize=18)
        ax.set_xlabel("Land Size", fontsize=18)
        ax.set_ylabel("Price", fontsize=18)
        st.pyplot(fig)

        st.subheader("Correlation Matrix of Housing Features")
        corr = df[['Price', 'Rooms', 'Distance', 'Landsize', 'BuildingArea', 'Bathroom']].corr()
        fig2, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap="Blues", ax=ax)
        ax.set_title("Correlation Between Features", fontsize=18)
        st.pyplot(fig2)


elif page == "KPIs and Main Features":
    st.title("Melbourne Housing - KPIs and Main Features")
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

        st.subheader("Price Trending")
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.lineplot(x=filtered_data['Date'], y=filtered_data['Price'], ax=ax)
        ax.set_title("Price Trend Over Time", fontsize=18)
        ax.set_xlabel("Date", fontsize=18)
        ax.set_ylabel("Price", fontsize=18)
        plt.xticks(rotation=45)
        st.pyplot(fig)


    with col2:
        st.subheader("Property Type Distribution")
        property_count = filtered_data['Type'].value_counts()
        fig4, ax4 = plt.subplots(figsize=(10, 8))
        ax4.pie(property_count.values, labels=property_count.index, autopct='%1.1f%%', startangle=90,
                colors=sns.color_palette('coolwarm', len(property_count)))
        ax4.set_title("Property Type Distribution", fontsize=18)

        # Equal aspect ratio ensures that pie chart is drawn as a circle.
        ax4.axis('equal')
        st.pyplot(fig4)

elif page == "Deap Analysis":
    st.title("Melbourne Housing - Deap Analysis")
    col1, col2 = st.columns([4, 2])

    with col1:

        st.title("Yearly Change in Property Price by Suburb")
        st.dataframe(price_change_df)



    with col2:
        st.subheader("Top 5 Suburbs by Yearly Price Change")

        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Price Change', y='Suburb', data=top_5_price_change, palette='viridis', ax=ax1)
        ax1.set_title('Yearly Price Change - Top 5)', fontsize=16)
        ax1.set_xlabel('Price Change (AUD)', fontsize=14)
        ax1.set_ylabel('Suburb', fontsize=14)
        st.pyplot(fig1)

        st.subheader("Top 5 Suburbs by Yearly Price Change %")

        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Percentage Change (%)', y='Suburb', data=top_5_pct_change, palette='magma', ax=ax2)
        ax2.set_title('Yearly Price Change % - Top 5 Suburbs', fontsize=16)
        ax2.set_xlabel('Percentage Change (%)', fontsize=14)
        ax2.set_ylabel('Suburb', fontsize=14)
        st.pyplot(fig2)

