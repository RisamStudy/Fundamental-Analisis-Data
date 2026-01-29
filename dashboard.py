import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style="dark")

def get_top_total_item_revenue_categories(df, top_n=10):
    """
    Get the top N categories by total total_item_revenue.

    Parameters:
    df (pd.DataFrame): DataFrame containing 'product_category_name_english' and 'total_item_revenue' columns.
    top_n (int): Number of top categories to return.

    Returns:
    pd.DataFrame: DataFrame with top N categories and their total total_item_revenue.
    """
    top_categories = (
        df.groupby('product_category_name_english')['total_item_revenue']
        .sum()
        .reset_index()
        .sort_values(by='total_item_revenue', ascending=False)
        .head(top_n)
    )
    return top_categories

def analyze_delivery_and_review(df):
    """
    Analyze delivery times and review scores.

    Parameters:
    df (pd.DataFrame): DataFrame containing 'estimated_delivery_time' and 'review_score' columns.

    Returns:
    pd.DataFrame: DataFrame with average delivery time and review score.
    """
    analysis = df[['estimated_delivery_time', 'review_score']].mean().reset_index()
    analysis.columns = ['metric', 'average_value']
    return analysis

def plot_top_categories_total_item_revenue(total_item_revenue_data):
    """
    Plot the top categories by total_item_revenue.

    Parameters:
    total_item_revenue_data (pd.DataFrame): DataFrame with 'product_category_name_english' and 'total_item_revenue' columns.
    """
    plt.figure(figsize=(10, 6))
    sns.barplot(x='total_item_revenue', y='product_category_name_english', data=total_item_revenue_data, palette='viridis')
    plt.title('Top Categories by total_item_revenue')
    plt.xlabel('Total total_item_revenue')
    plt.ylabel('product_category_name_english')
    st.pyplot(plt)

def plot_delivery_duration_by_review(delivery_review_df):
    """
    Plot delivery duration against review scores.

    Parameters:
    delivery_review_df (pd.DataFrame): DataFrame with 'estimated_delivery_time' and 'review_score' columns.
    """
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='review_score', y='estimated_delivery_time', data=delivery_review_df, hue='review_score', palette='coolwarm', s=100)
    plt.title('Delivery Duration vs Review Score')
    plt.xlabel('Review Score')
    plt.ylabel('Delivery Time (minutes)')
    st.pyplot(plt)

def plot_delivery_performance_by_review(delivery_performance_df):
    """
    Plot delivery performance by review scores.

    Parameters:
    delivery_performance_df (pd.DataFrame): DataFrame with 'review_score' and 'delivery_performance' columns.
    """
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='review_score', y='delivery_performance', data=delivery_performance_df, marker='o')
    plt.title('Delivery Performance by Review Score')
    plt.xlabel('Review Score')
    plt.ylabel('Delivery Performance (%)')
    st.pyplot(plt)

def display_kpis(df):
    """
    Display key performance indicators (KPIs) in Streamlit.

    Parameters:
    df (pd.DataFrame): DataFrame containing 'total_item_revenue', 'order_item_id', and 'customer_id' columns.
    """
    total_total_item_revenue = df['total_item_revenue'].sum()
    total_order_item_id = df['order_item_id'].sum()
    total_customer_id = df['customer_id'].nunique()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total total_item_revenue", format_currency(total_total_item_revenue, 'USD', locale='en_US'))

    with col2:
        st.metric("Total order_item_id", f"{total_order_item_id:,}")

    with col3:
        st.metric("Total customer_id", f"{total_customer_id:,}")

def main_dashboard(df):
    """
    Main function to render the dashboard.

    Parameters:
    df (pd.DataFrame): DataFrame containing the necessary data.
    """
    st.title("E-commerce Dashboard")

    # Display KPIs
    display_kpis(df)

    # Top Categories by total_item_revenue
    top_total_item_revenue_categories = get_top_total_item_revenue_categories(df)
    plot_top_categories_total_item_revenue(top_total_item_revenue_categories)

    # Delivery and Review Analysis
    delivery_review_analysis = analyze_delivery_and_review(df)
    st.subheader("Average Delivery Time and Review Score")
    st.dataframe(delivery_review_analysis)

    # Plot Delivery Duration by Review Score
    plot_delivery_duration_by_review(df)

    # Plot Delivery Performance by Review Score
    plot_delivery_performance_by_review(df)


df = pd.read_csv("main_data.csv")

datetime_columns = ["order_delivered_customer_date", "order_delivered_customer_date"]
df.sort_values(by=datetime_columns, inplace=True)
for col in datetime_columns:
    df[col] = pd.to_datetime(df[col])
main_dashboard(df)

# Membuat komponen filter
min_date = df['order_delivered_customer_date'].min()
max_date = df['order_delivered_customer_date'].max()

with st.sidebar:
    st.header("Filters")

    # Menambahkan Logo Perusahaan
    st.image("https://img.freepik.com/vektor-premium/vektor-desain-logo-minimalis-abstrak-yang-kreatif-dan-elegan-untuk-semua-perusahaan-merek_1253202-136614.jpg")

    #
    date_range = st.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df['order_delivered_customer_date'] >= pd.to_datetime(start_date)) & (df['order_delivered_customer_date'] <= pd.to_datetime(end_date))]
        st.success(f"Filtered data from {start_date} to {end_date}")
    else:
        st.error("Please select a valid date range.")
