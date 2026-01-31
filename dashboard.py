import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style="dark")

# =========================================================
# DATA PROCESSING FUNCTIONS
# =========================================================

def get_top_total_item_revenue_categories(df, top_n=10):
    top_categories = (
        df.groupby('product_category_name_english')['total_item_revenue']
        .sum()
        .reset_index()
        .sort_values(by='total_item_revenue', ascending=False)
        .head(top_n)
    )
    return top_categories


def analyze_delivery_and_review(df):
    analysis = df[['delivery_duration', 'review_score']].mean().reset_index()
    analysis.columns = ['metric', 'average_value']
    return analysis


# =========================================================
# VISUALIZATION FUNCTIONS
# =========================================================

def plot_top_categories_total_item_revenue(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x='total_item_revenue',
        y='product_category_name_english',
        data=data,
        palette='viridis',
        ax=ax
    )
    ax.set_title('Top Categories by Total Revenue', fontsize=14, fontweight='bold')
    ax.set_xlabel('Total Revenue')
    ax.set_ylabel('Product Category')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


def plot_delivery_duration_by_review(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        x='review_score',
        y='delivery_duration',
        data=df,
        hue='review_score',
        palette='coolwarm',
        s=80,
        ax=ax
    )
    ax.set_title('Delivery Duration vs Review Score', fontsize=14, fontweight='bold')
    ax.set_xlabel('Review Score')
    ax.set_ylabel('Delivery Duration (days)')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


def plot_delivery_performance_by_review(df):
    performance_data = (
        df.groupby('review_score')['delivery_duration']
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        x='review_score',
        y='delivery_duration',
        data=performance_data,
        marker='o',
        linewidth=2,
        markersize=8,
        ax=ax
    )
    ax.set_title('Average Delivery Duration by Review Score', fontsize=14, fontweight='bold')
    ax.set_xlabel('Review Score')
    ax.set_ylabel('Average Delivery Duration (days)')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


# =========================================================
# KPI FUNCTION
# =========================================================

def display_kpis(df):
    total_revenue = df['total_item_revenue'].sum()
    total_orders = df['order_id'].nunique()
    total_customers = df['customer_id'].nunique()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Revenue", format_currency(total_revenue, 'USD', locale='en_US'))

    with col2:
        st.metric("Total Orders", f"{total_orders:,}")

    with col3:
        st.metric("Total Customers", f"{total_customers:,}")


# =========================================================
# MAIN DASHBOARD
# =========================================================

def main_dashboard(df):
    st.title("📊 E-commerce Dashboard")
    st.markdown("---")

    st.subheader("Key Performance Indicators")
    display_kpis(df)

    st.markdown("---")
    st.subheader("Top 10 Categories by Revenue")
    top_categories = get_top_total_item_revenue_categories(df)
    plot_top_categories_total_item_revenue(top_categories)

    st.markdown("---")
    st.subheader("Delivery & Review Analysis")

    col1, col2 = st.columns(2)

    with col1:
        delivery_review_analysis = analyze_delivery_and_review(df)
        st.dataframe(delivery_review_analysis, use_container_width=True)

    with col2:
        avg_delivery = df['delivery_duration'].mean()
        avg_review = df['review_score'].mean()
        st.metric("Average Delivery Time", f"{avg_delivery:.2f} days")
        st.metric("Average Review Score", f"{avg_review:.2f} / 5.0")

    st.markdown("---")
    st.subheader("Delivery Duration vs Review Score")
    plot_delivery_duration_by_review(df)

    st.markdown("---")
    st.subheader("Average Delivery Time by Review Score")
    plot_delivery_performance_by_review(df)


# =========================================================
# MAIN EXECUTION
# =========================================================

df = pd.read_csv("https://github.com/RisamStudy/Fundamental-Analisis-Data/releases/download/v1.1/main_data.csv")

# Convert datetime
df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])

# CREATE REVENUE COLUMN (FIX UTAMA)
df['total_item_revenue'] = df['price'] + df['freight_value']

df.sort_values(by="order_delivered_customer_date", inplace=True)

# Sidebar filter
min_date = df['order_delivered_customer_date'].min()
max_date = df['order_delivered_customer_date'].max()

with st.sidebar:
    st.header("🔍 Filters")
    st.image(
        "https://img.freepik.com/vektor-premium/vektor-desain-logo-minimalis-abstrak-yang-kreatif-dan-elegan-untuk-semua-perusahaan-merek_1253202-136614.jpg"
    )
    st.markdown("---")

    date_range = st.date_input(
        "Select Date Range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Apply filter
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = df[
        (df['order_delivered_customer_date'] >= pd.to_datetime(start_date)) &
        (df['order_delivered_customer_date'] <= pd.to_datetime(end_date))
    ]

    with st.sidebar:
        st.success(f"✅ Filtered: {start_date} to {end_date}")
        st.info(f"📊 Total records: {len(filtered_df):,}")
else:
    filtered_df = df

main_dashboard(filtered_df)

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>E-commerce Analytics Dashboard | Data Analysis Project</p>
        <p style='font-size: 12px; color: gray;'>Made with ❤️ using Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)
