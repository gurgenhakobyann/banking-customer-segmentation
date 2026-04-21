import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Evocabank Customer Intelligence", layout="wide")

@st.cache_data
def load_data():
    # Loading the results from Jupyter Notebook
    df = pd.read_csv('client_segmentation_results.csv')
    return df

df = load_data()

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 Customer Segmentation Intelligence")
st.sidebar.title("Dashboard Settings")
st.sidebar.info("Use the tabs to explore segment distributions, behavioral DNA, and individual client profiles.")

# Defining 4 Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Segment Overview", 
    "🗺️ Market Geographics", 
    "🧬 Cluster DNA", 
    "🔍 Customer Lookup"
])


# TAB 1: segment overview
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Clients", f"{len(df):,}")
    col2.metric("Avg Monthly Salary", f"{df['monthly_salary_amd'].mean():,.0f} AMD")
    col3.metric("Avg Deposit", f"{df['total_deposit_balance'].mean():,.0f} AMD")
    col4.metric("Avg Loan", f"{df['total_loan_amount'].mean():,.0f} AMD")

    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("PCA Cluster Visualization")
        fig_pca = px.scatter(df, x='pca_1', y='pca_2', color='cluster', 
                             hover_data=['age', 'monthly_salary_amd', 'product_breadth'],
                             title="Segments in 2D PCA Space",
                             color_discrete_sequence=px.colors.qualitative.Vivid)
        st.plotly_chart(fig_pca, use_container_width=True)

    with c2:
        st.subheader("Salary Distribution by Cluster")
        fig_box = px.box(df, x='cluster', y='monthly_salary_amd', color='cluster',
                         title="Monthly Salary Range per Segment",
                         labels={'monthly_salary_amd': 'Salary (AMD)', 'cluster': 'Segment'})
        st.plotly_chart(fig_box, use_container_width=True)

# TAB 2: market geographics
with tab2:
    st.subheader("Regional Market Share")
    # Stacked bar chart showing which regions have which clusters
    reg_data = pd.crosstab(df['region'], df['cluster'], normalize='index').reset_index()
    reg_data_melted = reg_data.melt(id_vars='region', var_name='Cluster', value_name='Percentage')
    fig_reg = px.bar(reg_data_melted, x='region', y='Percentage', color='Cluster', 
                     title="Cluster Distribution by Region (%)", barmode='stack')
    st.plotly_chart(fig_reg, use_container_width=True)

    st.divider()
    
    st.subheader("Product Breadth per Segment")
    fig_breadth = px.histogram(df, x='cluster', color='product_breadth', barmode='group',
                               title="Number of Products Held by Segment Size")
    st.plotly_chart(fig_breadth, use_container_width=True)


# TAB 3: cluster dna
with tab3:
    st.subheader("Behavioral Profile (Radar Chart)")
    
    # Features for the radar comparison
    features = ['age', 'monthly_salary_amd', 'tx_total_amount', 'total_deposit_balance', 'total_loan_amount', 'product_breadth']
    
    # Calculate means 
    cluster_means = df.groupby('cluster')[features].mean(numeric_only=True).reset_index()
    
    # normalization so different scales fit on one chart
    cluster_means_norm = cluster_means.copy()
    for col in features:
        cluster_means_norm[col] = cluster_means[col] / (cluster_means[col].max() + 1e-6)

    fig_radar = go.Figure()
    for i in df['cluster'].unique():
        row = cluster_means_norm[cluster_means_norm['cluster'] == i].iloc[0]
        fig_radar.add_trace(go.Scatterpolar(
            r=[row[f] for f in features],
            theta=features,
            fill='toself',
            name=f'Segment {i}'
        ))
    
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), 
                            showlegend=True, title="Segment Behavioral DNA")
    st.plotly_chart(fig_radar, use_container_width=True)

    st.subheader("Spending vs. Wealth")
    fig_scatter = px.scatter(df, x='monthly_salary_amd', y='tx_total_amount', color='cluster', 
                             opacity=0.5, size='product_breadth',
                             title="Transaction Spend vs. Monthly Salary",
                             labels={'monthly_salary_amd': 'Salary', 'tx_total_amount': 'Card Spend'})
    st.plotly_chart(fig_scatter, use_container_width=True)


# TAB 4: customer lookup
with tab4:
    st.subheader("Client Intelligence Search")
    search_id = st.text_input("Enter Client ID (e.g., C00001):")
    
    if search_id:
        customer = df[df['client_id'] == search_id]
        if not customer.empty:
            cust = customer.iloc[0]
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.info(f"**Assigned Segment:** Cluster {cust['cluster']}")
                st.write(f"**Gender:** {cust['gender']}")
                st.write(f"**Age:** {cust['age']}")
            with c2:
                st.success(f"**Income:** {cust['monthly_salary_amd']:,.0f} AMD")
                st.write(f"**Region:** {cust['region']}")
                st.write(f"**Product Breadth:** {cust['product_breadth']}")
            with c3:
                st.warning(f"**Tenure:** {cust['tenure_days']} days")
                st.write(f"**Employment:** {cust['employment_status']}")
                st.write(f"**Education:** {cust['education_level']}")
            
            st.divider()
            st.subheader("💡 Strategic Action for this Client")
            # Custom recommendations based on cluster meanings
            if cust['cluster'] == 1:
                st.write("📈 **Priority:** High-Value Saver. Offer Premium Term Deposits and Investment Portfolio consultations.")
            elif cust['cluster'] == 2:
                st.write("🛒 **Priority:** Active Transactor. Offer a higher Credit Card limit or Dining/Electronics Cashback rewards.")
            else:
                st.write("🎯 **Priority:** Growth Opportunity. Cross-sell a Savings account or a small pre-approved Consumer Loan.")
        else:
            st.error("Client ID not found. Please verify the ID.")
    else:
        st.write("Please enter a Client ID to view the detailed financial profile.")

# Raw Data Table Footer
if st.checkbox("Show Cluster Averages Table"):
    st.dataframe(df.groupby('cluster').mean(numeric_only=True).round(2))
