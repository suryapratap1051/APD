import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Amazon Products EDA",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("🛒 Amazon Products - Exploratory Data Analysis")
st.markdown("This dashboard performs EDA on a synthetic dataset of Amazon products.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('amazon_products.csv')
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Products")
categories = st.sidebar.multiselect(
    "Select Category",
    options=df['category'].unique(),
    default=df['category'].unique()
)

price_range = st.sidebar.slider(
    "Price Range (Discounted)",
    float(df['discounted_price'].min()),
    float(df['discounted_price'].max()),
    (float(df['discounted_price'].min()), float(df['discounted_price'].max()))
)

rating_range = st.sidebar.slider(
    "Rating Range",
    1.0, 5.0,
    (1.0, 5.0)
)

# Apply filters
filtered_df = df[
    (df['category'].isin(categories)) &
    (df['discounted_price'] >= price_range[0]) &
    (df['discounted_price'] <= price_range[1]) &
    (df['rating'] >= rating_range[0]) &
    (df['rating'] <= rating_range[1])
]

# Show number of results
st.sidebar.markdown(f"**Products after filter:** {filtered_df.shape[0]}")

# Main panel with tabs
tab1, tab2, tab3 = st.tabs(["📋 Data Overview", "📈 Visualizations", "📊 Summary Statistics"])

with tab1:
    st.subheader("Raw Data (First 100 Rows)")
    st.dataframe(filtered_df.head(100))
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Shape:**", filtered_df.shape)
    with col2:
        st.write("**Missing Values:**")
        st.write(filtered_df.isnull().sum())

with tab2:
    st.subheader("Distribution of Discounted Prices")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(filtered_df['discounted_price'], bins=30, edgecolor='k', alpha=0.7)
    ax.set_xlabel("Price ($)")
    ax.set_ylabel("Frequency")
    ax.set_title("Price Distribution")
    st.pyplot(fig)
    
    st.subheader("Distribution of Ratings")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(filtered_df['rating'], bins=20, edgecolor='k', alpha=0.7, color='orange')
    ax.set_xlabel("Rating")
    ax.set_ylabel("Frequency")
    ax.set_title("Rating Distribution")
    st.pyplot(fig)
    
    st.subheader("Number of Products per Category")
    cat_counts = filtered_df['category'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 5))
    cat_counts.plot(kind='bar', ax=ax, color='green', edgecolor='black')
    ax.set_xlabel("Category")
    ax.set_ylabel("Count")
    ax.set_title("Product Count by Category")
    st.pyplot(fig)
    
    st.subheader("Price vs. Rating (Scatter Plot)")
    fig, ax = plt.subplots(figsize=(8, 5))
    scatter = ax.scatter(
        filtered_df['discounted_price'], 
        filtered_df['rating'],
        c=filtered_df['rating_count'], 
        cmap='viridis', 
        alpha=0.6,
        edgecolors='w', 
        linewidth=0.5
    )
    ax.set_xlabel("Discounted Price ($)")
    ax.set_ylabel("Rating")
    ax.set_title("Price vs Rating (colored by number of reviews)")
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Rating Count')
    st.pyplot(fig)

with tab3:
    st.subheader("Summary Statistics (Numerical Columns)")
    st.dataframe(filtered_df.describe())
    
    st.subheader("Average Metrics by Category")
    category_stats = filtered_df.groupby('category').agg({
        'discounted_price': 'mean',
        'rating': 'mean',
        'rating_count': 'mean'
    }).round(2).rename(columns={
        'discounted_price': 'Avg Price',
        'rating': 'Avg Rating',
        'rating_count': 'Avg Reviews'
    })
    st.dataframe(category_stats)
    
    st.subheader("Top 10 Most Reviewed Products")
    top_reviewed = filtered_df.nlargest(10, 'rating_count')[['product_name', 'category', 'rating', 'rating_count']]
    st.dataframe(top_reviewed)