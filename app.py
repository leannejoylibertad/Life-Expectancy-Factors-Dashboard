import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image

# Load the Hypothetical Data
df = pd.read_excel("Hypothetical_Data.xlsx")


# Streamlit Layout
st.set_page_config(page_title="SDG Dashboard", layout="wide")

# Insert Image/ Icon here
# Could remove caption
image = Image.open ("icon.png")
st.image (image, caption= "", width=1900)


# To make prettier font style and personalize it
st.markdown(
    f"""
    <p style='
        font-size:65px;
        color:black;
        font-weight:bold;
        text-align:center;
        margin:0;
    '>
        Drivers of Life Expectancy ❤️
    </p>
    """,
    unsafe_allow_html=True
)

# Slider (Time Filter) 
# 2010 shows if diin ginpinpoint ang year by default
# set minimum and maximum year for slider
selected_year = st.slider(
    "Select Year",
    int(df["Year"].min()),
    int(df["Year"].max()),
    2010
)
# Stores the year chosen in the slider
filtered_df = df[df["Year"] == selected_year]


# KPI Section
st.markdown(
    f"""
    <p style="
        font-size:45px;
        color:#00000;
        font-weight:bold;
        text-align:center;
        margin-bottom:10px;
    ">
        Key Indicators by Country ({selected_year})
    </p>
    """,
    unsafe_allow_html=True
)

avg_life = filtered_df["Life Expectancy"].mean()
avg_gdp = filtered_df["GDP per Capita"].mean()
avg_edu = filtered_df["Education Index"].mean()
avg_hea = filtered_df["Health Index"].mean()

# Presenting the KPIs withouth Loop
st.markdown("""
<style>
div[data-testid="stMetric"] {
    border: 1px solid navy !important;
    border-radius: 12px;
    padding: 15px;
    background-color: #001f3f;   /* navy blue */
    color: white !important;
}

div[data-testid="stMetric"] label {
    color: white !important;
    font-weight: bold;
}

div[data-testid="stMetricValue"] {
    color: white !important;
    font-size:65px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"### Average KPIs for {selected_year}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Avg Life Expectancy", f"{avg_life:.2f}", border=True)

with col2:
    st.metric("Avg GDP per Capita", f"{avg_gdp:.0f}", border=True)

with col3:
    st.metric("Avg Education Index", f"{avg_edu:.2f}", border=True)

with col4:
    st.metric("Avg Health Index", f"{avg_hea:.2f}", border=True)

# Presenting the KPIs with Loop
st.markdown("""
<style>
.kpi-box{
    border:1px solid navy;
    border-radius:12px;
    padding:15px;
    text-align:center;
    margin-bottom:10px;
}
.kpi-title{
    font-size:22px;
    font-weight:bold;
    color:navy;
    margin-bottom:8px;
}
</style>
""", unsafe_allow_html=True)

# Presenting the KPIs with Loop
for _, row in filtered_df.iterrows():

    st.markdown(f"## {row['Country']}")

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-title">Life Expectancy</div>
            <p style='font-size:28px; color:#E9B8C9; font-weight:bold; margin:0;'>
                {row['Life Expectancy']:.2f}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-title">GDP Per Capita</div>
            <p style='font-size:28px; color:#93C193; font-weight:bold; margin:0;'>
                {row['GDP per Capita']:.2f}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col7:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-title">Education Index</div>
            <p style='font-size:28px; color:#F5CD6A; font-weight:bold; margin:0;'>
                {row['Education Index']:.2f}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col8:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-title">Health Index</div>
            <p style='font-size:28px; color:#EB8F48; font-weight:bold; margin:0;'>
                {row['Health Index']:.2f}
            </p>
        </div>
        """, unsafe_allow_html=True)
# Add Spacing
st.text("")

# Two Charts Side by Side
chart_col1, chart_col2 = st.columns(2)

# Line Chart Data
trend = df.groupby("Year", as_index=False)["Life Expectancy"].mean()

with chart_col1:
    st.markdown(
        """
        <p style='font-size:35px; color:#5992C6; font-weight:bold; text-align:center;'>
            Life Expectancy Trend Over Time
        </p>
        """,
        unsafe_allow_html=True
    )

    fig_line = px.line(
        trend,
        x="Year",
        y="Life Expectancy",
        title="Global Trend"
    )

    st.plotly_chart(fig_line, use_container_width=True)


with chart_col2:
    st.markdown(
        f"""
        <p style='font-size:35px; color:#5992C6; font-weight:bold; text-align:center;'>
            Life Expectancy Comparison for {selected_year}
        </p>
        """,
        unsafe_allow_html=True
    )

    fig_bar = px.bar(
        filtered_df,
        x="Country",
        y="Life Expectancy",
        color="Country",
        title="Life Expectancy by Country"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

# Two Charts Side by Side
chart_col3, chart_col4 = st.columns(2)

# LEFT COLUMN - Scatter Plot
with chart_col3:
    st.markdown(
        """
        <p style='font-size:35px; color:#5992C6; font-weight:bold; text-align:center;'>
            Relationship: GDP vs Life Expectancy
        </p>
        """,
        unsafe_allow_html=True
    )

    fig_scatter = px.scatter(
        df,
        x="GDP per Capita",
        y="Life Expectancy",
        color="Country",
        trendline="ols",
        title="GDP vs Life Expectancy"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

# RIGHT COLUMN - Bubble Chart
with chart_col4:
    st.markdown(
        """
        <p style='font-size:35px; color:#5992C6; font-weight:bold; text-align:center;'>
            Multi-variable View
        </p>
        """,
        unsafe_allow_html=True
    )

    fig_bubble = px.scatter(
        filtered_df,
        x="GDP per Capita",
        y="Life Expectancy",
        size="Education Index",
        color="Country",
        hover_name="Country",
        title="GDP, Education, and Life Expectancy"
    )

    st.plotly_chart(fig_bubble, use_container_width=True)

st.text("")


# Footer Insight Section
st.markdown("""
<style>
.insight-box {
    border: 2px solid navy;
    border-radius: 14px;
    padding: 25px;
    width: 100%;
    background-color: #f8fbff;
    margin-top: 20px;
}

.insight-title {
    font-size: 34px;
    font-weight: bold;
    color: navy;
    margin-bottom: 12px;
}

.insight-text {
    font-size: 22px;
    color: #1f1f1f;
    line-height: 1.8;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
    <div class="insight-title">💡 Key Insight</div>
    <div class="insight-text">
        The analysis indicates that countries with stronger economies and higher education levels generally
        experience longer life expectancy. This finding is supported by Preston (1975), who identified a strong
        positive relationship between national income and life expectancy, showing that wealthier nations tend
        to achieve better health outcomes. Similarly, Cutler and Lleras-Muney (2006) found that education is
        closely associated with healthier behaviors, improved decision-making, and greater use of healthcare
        services. Higher income often enables better access to nutrition, sanitation, and medical treatment,
        while education increases health awareness and disease prevention practices. However, life expectancy
        is also shaped by healthcare quality, environmental conditions, government policies, and levels of
        social equality, meaning economic growth alone does not fully determine population health.
        <br><br>
        <b>References:</b><br>
        Preston, S. H. (1975). The changing relation between mortality and level of economic development.<br>
        Cutler, D. M., &amp; Lleras-Muney, A. (2006). Education and health: Evaluating theories and evidence.
    </div>
</div>
""", unsafe_allow_html=True)