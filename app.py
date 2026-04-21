import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Banking Customer Segmentation", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('client_segmentation_results.csv')
    return df

df = load_data()

st.title("🏦 Banking Customer Segmentation Dashboard")
st.markdown("This dashboard presents customer segments derived from behavioral and demographic banking data.")

# SIDEBAR FILTERS
st.sidebar.header("Filters")
selected_cluster = st.sidebar.multiselect("Select Clusters", options=df['cluster'].unique(), default=df['cluster'].unique())
filtered_df = df[df['cluster'].isin(selected_cluster)]

# ROW 1: Key Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Clients", len(filtered_df))
col2.metric("Avg Salary", f"{filtered_df['monthly_salary_amd'].mean():,.0f} AMD")
col3.metric("Avg Deposit", f"{filtered_df['total_deposit_balance'].mean():,.0f} AMD")
col4.metric("Avg Loan", f"{filtered_df['total_loan_amount'].mean():,.0f} AMD")

# ROW 2: Visualization
st.divider()
c1, c2 = st.columns(2)

with c1:
    st.subheader("Segment Visualization (PCA Space)")
    fig = px.scatter(filtered_df, x='pca_1', y='pca_2', color='cluster', 
                     hover_data=['age', 'monthly_salary_amd', 'product_breadth'],
                     title="Clusters Visualized in 2D PCA Space")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Salary vs. Spending by Cluster")
    fig2 = px.box(filtered_df, x='cluster', y='monthly_salary_amd', color='cluster',
                  title="Salary Distribution per Cluster")
    st.plotly_chart(fig2, use_container_width=True)

# ROW 3: Feature Importance 
st.subheader("Cluster Behavioral Comparison")
features_to_plot = ['age', 'monthly_salary_amd', 'tx_total_amount', 'total_deposit_balance', 'total_loan_amount']
cluster_means = df.groupby('cluster')[features_to_plot].mean(numeric_only=True).reset_index()

# Normalize for comparison
cluster_means_norm = cluster_means.copy()
for col in features_to_plot:
    cluster_means_norm[col] = cluster_means[col] / cluster_means[col].max()

fig3 = px.line_polar(cluster_means_norm.melt(id_vars='cluster'), r='value', theta='variable', 
                     color='cluster', line_close=True, title="Cluster DNA (Normalized)")
st.plotly_chart(fig3)

st.write("### Raw Cluster Data")
st.dataframe(df.groupby('cluster').mean(numeric_only=True).round(2))
