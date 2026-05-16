import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# ── Load Data ─────────────────────────────────────────────────────────────────
df = pd.read_excel("Hypothetical_Data.xlsx")

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Life Expectancy Dashboard", layout="wide")

# ── Global Styles ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #F7F4EF;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1B4F72, #117A65);
    border-radius: 16px;
    padding: 20px 16px;
    color: white !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    transition: transform 0.2s ease;
}
div[data-testid="stMetric"]:hover { transform: translateY(-3px); }
div[data-testid="stMetric"] label { color: #A9CCE3 !important; font-size: 14px !important; font-weight: 600 !important; letter-spacing: 0.05em; }
div[data-testid="stMetricValue"] { color: #FDFEFE !important; font-size: 2rem !important; font-weight: 700 !important; }

/* Country KPI boxes */
.kpi-box {
    border-radius: 14px;
    padding: 18px 12px;
    text-align: center;
    margin-bottom: 12px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    transition: transform 0.15s ease;
}
.kpi-box:hover { transform: translateY(-2px); }
.kpi-title {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    margin-bottom: 8px;
}

/* Section headers */
.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #1B4F72;
    text-align: center;
    margin: 24px 0 8px;
}

/* Credits ribbon */
.credits-ribbon {
    background: linear-gradient(90deg, #1B4F72 0%, #117A65 100%);
    color: white;
    text-align: center;
    padding: 10px 0;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.04em;
    border-radius: 0 0 10px 10px;
    margin-bottom: 20px;
}

/* Insight box */
.insight-box {
    background: linear-gradient(135deg, #EAF2F8 0%, #E8F8F5 100%);
    border-left: 6px solid #1B4F72;
    border-radius: 16px;
    padding: 30px 36px;
    margin-top: 30px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.07);
}
.insight-title {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 700;
    color: #1B4F72;
    margin-bottom: 14px;
}
.insight-text {
    font-size: 16px;
    color: #2C3E50;
    line-height: 1.9;
}

/* Slider label */
.slider-label {
    font-size: 18px;
    font-weight: 600;
    color: #117A65;
    margin-bottom: 4px;
}

/* Divider */
.fancy-divider {
    border: none;
    height: 3px;
    background: linear-gradient(90deg, #1B4F72, #117A65, #F39C12);
    border-radius: 2px;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# ── Banner ─────────────────────────────────────────────────────────────────────
banner = Image.open("banner.png")
st.image(banner, use_column_width=True)

# ── Credits Ribbon ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="credits-ribbon">
    📊 Dashboard guided by <b>Paolo G. Hilado, MSc.</b> &nbsp;|&nbsp; ⚠️ This dashboard is for Training Purposes Only.
</div>
""", unsafe_allow_html=True)

# ── Title ──────────────────────────────────────────────────────────────────────
st.markdown("""
<p style='
    font-family: "Playfair Display", serif;
    font-size: 58px;
    color: #1B4F72;
    font-weight: 700;
    text-align: center;
    margin: 10px 0 4px;
    line-height: 1.2;
'>
    Drivers of Life Expectancy
</p>
<p style='text-align:center; font-size:18px; color:#6c757d; margin-bottom:20px;'>
    Exploring how economy, education, and health shape how long we live.
</p>
""", unsafe_allow_html=True)

st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

# ── Year Slider ────────────────────────────────────────────────────────────────
st.markdown("<div class='slider-label'>🗓️ Select a Year to Explore</div>", unsafe_allow_html=True)
selected_year = st.slider(
    "",
    int(df["Year"].min()),
    int(df["Year"].max()),
    2010,
    label_visibility="collapsed"
)
filtered_df = df[df["Year"] == selected_year]

st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

# ── Average KPIs ───────────────────────────────────────────────────────────────
st.markdown(f"<div class='section-header'>🌍 Global Snapshot — {selected_year}</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#6c757d; margin-bottom:18px;'>Cross-country averages for the selected year</p>", unsafe_allow_html=True)

avg_life = filtered_df["Life Expectancy"].mean()
avg_gdp  = filtered_df["GDP per Capita"].mean()
avg_edu  = filtered_df["Education Index"].mean()
avg_hea  = filtered_df["Health Index"].mean()

col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("🫀 Avg Life Expectancy", f"{avg_life:.2f} yrs")
with col2: st.metric("💰 Avg GDP per Capita",   f"${avg_gdp:,.0f}")
with col3: st.metric("📚 Avg Education Index",  f"{avg_edu:.2f}")
with col4: st.metric("🏥 Avg Health Index",      f"{avg_hea:.2f}")

st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

# ── Per-Country KPIs ───────────────────────────────────────────────────────────
st.markdown(f"<div class='section-header'>🗺️ Country Breakdown — {selected_year}</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#6c757d; margin-bottom:18px;'>Detailed indicators per country</p>", unsafe_allow_html=True)

CARD_COLORS = [
    ("#1B4F72", "#AED6F1"),  # blue
    ("#117A65", "#A9DFBF"),  # green
    ("#7D6608", "#F9E79F"),  # yellow
    ("#6E2F1A", "#F5CBA7"),  # orange
]

for _, row in filtered_df.iterrows():
    st.markdown(f"""
    <p style='font-family:"Playfair Display",serif; font-size:26px; color:#1B4F72;
              font-weight:700; margin: 20px 0 6px;'>
        📍 {row['Country']}
    </p>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    labels  = ["Life Expectancy", "GDP Per Capita", "Education Index", "Health Index"]
    values  = [
        f"{row['Life Expectancy']:.2f} yrs",
        f"${row['GDP per Capita']:,.2f}",
        f"{row['Education Index']:.2f}",
        f"{row['Health Index']:.2f}",
    ]

    for i, (col, label, val) in enumerate(zip(cols, labels, values)):
        bg, fg = CARD_COLORS[i]
        with col:
            st.markdown(f"""
            <div class="kpi-box" style="background:{bg};">
                <div class="kpi-title" style="color:{fg};">{label}</div>
                <p style="font-size:26px; color:{fg}; font-weight:700; margin:0;">{val}</p>
            </div>
            """, unsafe_allow_html=True)

st.text("")
st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

# ── Charts Row 1 ───────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>📈 Trends & Comparisons</div>", unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2)
trend = df.groupby("Year", as_index=False)["Life Expectancy"].mean()

with chart_col1:
    fig_line = px.line(
        trend, x="Year", y="Life Expectancy",
        title=f"Global Average Life Expectancy Over Time",
        color_discrete_sequence=["#117A65"],
        template="plotly_white"
    )
    fig_line.update_traces(line=dict(width=3))
    fig_line.update_layout(
        title_font=dict(family="Playfair Display", size=18, color="#1B4F72"),
        plot_bgcolor="#FAFAFA", paper_bgcolor="#F7F4EF"
    )
    st.plotly_chart(fig_line, use_container_width=True)

with chart_col2:
    fig_bar = px.bar(
        filtered_df, x="Country", y="Life Expectancy",
        color="Country",
        title=f"Life Expectancy by Country ({selected_year})",
        color_discrete_sequence=px.colors.qualitative.Safe,
        template="plotly_white"
    )
    fig_bar.update_layout(
        title_font=dict(family="Playfair Display", size=18, color="#1B4F72"),
        plot_bgcolor="#FAFAFA", paper_bgcolor="#F7F4EF",
        showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Charts Row 2 ───────────────────────────────────────────────────────────────
chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    fig_scatter = px.scatter(
        df, x="GDP per Capita", y="Life Expectancy",
        color="Country", trendline="ols",
        title="Does Wealth Buy Longer Life?",
        color_discrete_sequence=px.colors.qualitative.Safe,
        template="plotly_white"
    )
    fig_scatter.update_layout(
        title_font=dict(family="Playfair Display", size=18, color="#1B4F72"),
        plot_bgcolor="#FAFAFA", paper_bgcolor="#F7F4EF"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with chart_col4:
    fig_bubble = px.scatter(
        filtered_df,
        x="GDP per Capita", y="Life Expectancy",
        size="Education Index",
        color="Country",
        hover_name="Country",
        title=f"Wealth × Education × Longevity ({selected_year})",
        color_discrete_sequence=px.colors.qualitative.Safe,
        template="plotly_white"
    )
    fig_bubble.update_layout(
        title_font=dict(family="Playfair Display", size=18, color="#1B4F72"),
        plot_bgcolor="#FAFAFA", paper_bgcolor="#F7F4EF"
    )
    st.plotly_chart(fig_bubble, use_container_width=True)

st.text("")

# ── Insights ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="insight-box">
    <div class="insight-title">💡 What the Data Is Telling Us</div>
    <div class="insight-text">
        Life expectancy is not shaped by a single factor — it emerges from the complex interplay
        of a nation's economic strength, educational attainment, and healthcare quality. Countries
        with higher GDP per capita tend to invest more in public health infrastructure, nutrition
        programs, and disease prevention, all of which translate into longer, healthier lives.
        <br><br>
        Education plays an equally vital role. When people have greater access to quality schooling,
        they are more likely to adopt health-protective behaviors, seek medical care early, and
        understand the risks associated with lifestyle choices. This relationship, observed across
        multiple studies, demonstrates that investment in human capital yields compounding returns
        in population health over time.
        <br><br>
        The health index captures a country's overall healthcare access and outcomes — and its
        strong correlation with life expectancy underscores a clear message: <b>health systems save
        lives.</b> Yet even in high-income nations, inequalities in education and healthcare access
        can significantly dampen life expectancy gains, reminding us that growth alone is not enough
        without equity.
        <br><br>
        Together, these three drivers — <b>economy, education, and health</b> — form the foundation
        of a long and thriving life. Policy interventions that simultaneously address all three are
        most likely to produce meaningful and lasting improvements in population health outcomes.
        <br><br>
        <b>References:</b><br>
        Preston, S. H. (1975). The changing relation between mortality and level of economic development.
        <em>Population Studies, 29</em>(2), 231–248.<br>
        Cutler, D. M., &amp; Lleras-Muney, A. (2006). Education and health: Evaluating theories and evidence.
        <em>NBER Working Paper No. 12352.</em><br>
        Lochner, L. et al. (2024). Effects of education on adult mortality: a global systematic review and meta-analysis.
        <em>The Lancet Public Health.</em> https://doi.org/10.1016/S2468-2667(23)00306-7<br>
        Farahani, M. et al. (2020). The influence of education on health: an empirical assessment of OECD countries
        for the period 1995–2015. <em>Archives of Public Health.</em> https://doi.org/10.1186/s13690-020-00402-5
    </div>
</div>
""", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-top:40px; font-size:13px; color:#aaa; padding-bottom:20px;">
    Dashboard created for academic training purposes only. &nbsp;|&nbsp;
    Guided by <b>Paolo G. Hilado, MSc.</b>
</div>
""", unsafe_allow_html=True)
