import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="KPI Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 KPI Analysis Dashboard")

# File Upload
uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Numeric columns
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if not numeric_cols:
        st.warning("No numeric columns found for KPI analysis.")
        st.stop()

    # KPI Selection
    selected_kpi = st.selectbox(
        "Select KPI Metric",
        numeric_cols
    )

    # KPI Calculations
    total_value = df[selected_kpi].sum()
    avg_value = df[selected_kpi].mean()
    max_value = df[selected_kpi].max()
    min_value = df[selected_kpi].min()

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        label="Total",
        value=f"{total_value:,.2f}"
    )

    col2.metric(
        label="Average",
        value=f"{avg_value:,.2f}"
    )

    col3.metric(
        label="Maximum",
        value=f"{max_value:,.2f}"
    )

    col4.metric(
        label="Minimum",
        value=f"{min_value:,.2f}"
    )

    st.markdown("---")

    # Trend Analysis
    st.subheader("Trend Analysis")

    x_axis = st.selectbox(
        "Select Dimension",
        df.columns
    )

    fig = px.line(
        df,
        x=x_axis,
        y=selected_kpi,
        markers=True,
        title=f"{selected_kpi} Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Distribution
    st.subheader("Distribution")

    hist_fig = px.histogram(
        df,
        x=selected_kpi,
        nbins=30,
        title=f"{selected_kpi} Distribution"
    )

    st.plotly_chart(hist_fig, use_container_width=True)

    # Summary Statistics
    st.subheader("Statistical Summary")
    st.dataframe(df[numeric_cols].describe())

else:
    st.info("Upload a CSV file to begin KPI analysis.")