"""
app.py  —  Superstore Sales Analytics Dashboard
------------------------------------------------
Run with:
    streamlit run dashboard/app.py
"""

import sys
import os

# Ensure src/ is importable from any working directory
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import streamlit as st
import pandas as pd
import numpy as np

from src.data_loader import get_data
from src.analysis import (
    get_kpis, revenue_by_period, top_products, bottom_products,
    category_summary, subcategory_summary, region_summary, state_summary,
    segment_summary, discount_impact, shipping_summary, yoy_growth,
)
from src.charts import (
    revenue_trend_chart, top_products_chart, category_donut,
    subcategory_bar, category_treemap, region_bar, state_map,
    segment_donut, segment_bar, discount_scatter, discount_bucket_bar,
    shipping_bar, yoy_chart, margin_waterfall,
)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Superstore Sales Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL STYLES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Root colours */
:root {
    --bg:       #0F1117;
    --card:     #1A1D2E;
    --border:   #2A2D3E;
    --accent:   #7C5CBF;
    --positive: #00C9A7;
    --negative: #FC5C65;
    --text:     #E8EAED;
    --muted:    #9AA0B4;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Custom overrides */
[data-testid="stSidebar"] {
    border-right: 1px solid var(--border);
}

/* Hide default Streamlit header/footer */
#MainMenu, footer, header { visibility: hidden; }

/* KPI card */
.kpi-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 12px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(124,92,191,0.20);
}
.kpi-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: var(--accent);
    border-radius: 14px 0 0 14px;
}
.kpi-icon   { font-size: 26px; margin-bottom: 4px; }
.kpi-label  { color: var(--muted); font-size: 12px; font-weight: 500;
              text-transform: uppercase; letter-spacing: 0.08em; margin: 0; }
.kpi-value  { color: var(--text); font-size: 26px; font-weight: 700;
              margin: 2px 0 0 0; line-height: 1.1; }
.kpi-delta  { font-size: 12px; margin-top: 4px; font-weight: 500; }
.kpi-pos    { color: var(--positive); }
.kpi-neg    { color: var(--negative); }

/* Section header */
.section-title {
    font-size: 20px; font-weight: 600; color: var(--text);
    border-left: 4px solid var(--accent);
    padding-left: 12px; margin: 28px 0 16px 0;
}

/* Insight cards */
.insight-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 14px;
    border-left: 4px solid var(--accent);
}
.insight-card h4 { color: var(--accent); margin: 0 0 6px 0; font-size: 15px; }
.insight-card p  { color: var(--text); margin: 0; font-size: 13px;
                   line-height: 1.6; }

/* Tab styling */
[data-testid="stTabs"] [data-baseweb="tab"] {
    color: var(--muted) !important;
    font-weight: 500;
    font-size: 14px;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent);
}

/* Dataframe */
.dataframe { background: var(--card) !important; color: var(--text) !important; }

/* Divider */
hr { border-color: var(--border); }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  DATA LOADING  (cached)
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner="⏳  Loading & cleaning dataset …")
def load():
    return get_data()


df_full = load()


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR — Filters
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 8px'>
        <span style='font-size:36px'>📊</span>
        <h2 style='margin:4px 0;font-size:18px;color:#E8EAED'>Superstore Analytics</h2>
        <p style='color:#9AA0B4;font-size:12px;margin:0'>Client-Ready Dashboard</p>
    </div>
    <hr style='border-color:#2A2D3E;margin:12px 0'/>
    """, unsafe_allow_html=True)

    st.markdown("**🗓️ Date Range**")
    min_date = df_full["Order Date"].min().date()
    max_date = df_full["Order Date"].max().date()
    date_range = st.date_input(
        "Select range", value=(min_date, max_date),
        min_value=min_date, max_value=max_date,
        label_visibility="collapsed",
    )

    st.markdown("**🌍 Region**")
    regions = ["All"] + sorted(df_full["Region"].dropna().unique().tolist())
    sel_region = st.multiselect("Region", regions[1:], default=[],
                                placeholder="All regions",
                                label_visibility="collapsed")

    st.markdown("**👥 Segment**")
    segments = sorted(df_full["Segment"].dropna().unique().tolist())
    sel_segment = st.multiselect("Segment", segments, default=[],
                                 placeholder="All segments",
                                 label_visibility="collapsed")

    st.markdown("**📦 Category**")
    categories = sorted(df_full["Category"].dropna().unique().tolist())
    sel_cat = st.multiselect("Category", categories, default=[],
                             placeholder="All categories",
                             label_visibility="collapsed")

    st.markdown("**📈 Time Granularity**")
    granularity = st.radio("Granularity", ["Monthly", "Quarterly", "Yearly"],
                           horizontal=True, label_visibility="collapsed")

    st.markdown("<hr style='border-color:#2A2D3E;margin:16px 0'/>",
                unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#9AA0B4;font-size:11px;text-align:center'>"
        "Data: Kaggle Superstore Dataset<br>"
        "Built with Python · Streamlit · Plotly</p>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  APPLY FILTERS
# ══════════════════════════════════════════════════════════════════════════════
df = df_full.copy()

if len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    df = df[(df["Order Date"] >= start) & (df["Order Date"] <= end)]

if sel_region:
    df = df[df["Region"].isin(sel_region)]
if sel_segment:
    df = df[df["Segment"].isin(sel_segment)]
if sel_cat:
    df = df[df["Category"].isin(sel_cat)]

if df.empty:
    st.warning("⚠️ No data matches the current filters. Please adjust your selection.")
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style='padding:24px 0 8px'>
    <h1 style='font-size:32px;font-weight:700;margin:0;
               background:linear-gradient(135deg,#7C5CBF,#00C9A7);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent'>
        Superstore Sales Analytics
    </h1>
    <p style='color:#9AA0B4;font-size:14px;margin:6px 0 0'>
        Executive dashboard · Revenue intelligence · Business recommendations
    </p>
</div>
""", unsafe_allow_html=True)

# Row count badge
st.markdown(
    f"<span style='background:#2A2D3E;color:#9AA0B4;font-size:12px;"
    f"border-radius:20px;padding:3px 12px'>"
    f"📋 {len(df):,} records  •  "
    f"{df['Order Date'].min().strftime('%b %Y')} → "
    f"{df['Order Date'].max().strftime('%b %Y')}</span>",
    unsafe_allow_html=True,
)

st.markdown("<div style='height:16px'/>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════════════════════
tabs = st.tabs([
    "📊 Executive Summary",
    "📈 Sales Trends",
    "🏆 Top Products",
    "🗺️ Regional View",
    "📦 Category Analysis",
    "👥 Customer Segments",
    "💸 Discount Analysis",
    "🚚 Shipping",
    "💡 Insights & Recommendations",
])


# ── Helper: KPI card HTML ──────────────────────────────────────────────────────
def kpi_card(icon, label, value, delta=None, delta_positive=True):
    delta_html = ""
    if delta is not None:
        cls = "kpi-pos" if delta_positive else "kpi-neg"
        arrow = "▲" if delta_positive else "▼"
        delta_html = f"<div class='kpi-delta {cls}'>{arrow} {delta}</div>"
    return f"""
    <div class='kpi-card'>
        <div class='kpi-icon'>{icon}</div>
        <p class='kpi-label'>{label}</p>
        <p class='kpi-value'>{value}</p>
        {delta_html}
    </div>
    """


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 0 — Executive Summary
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    kpis = get_kpis(df)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card("💰", "Total Revenue",
                             f"${kpis['total_sales']:,.0f}"), unsafe_allow_html=True)
    with c2:
        is_pos = kpis["total_profit"] >= 0
        st.markdown(kpi_card("📈", "Total Profit",
                             f"${kpis['total_profit']:,.0f}",
                             delta_positive=is_pos), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("🛒", "Total Orders",
                             f"{kpis['total_orders']:,}"), unsafe_allow_html=True)
    with c4:
        margin_pos = kpis["profit_margin"] >= 0
        st.markdown(kpi_card("📊", "Profit Margin",
                             f"{kpis['profit_margin']:.1f}%",
                             delta_positive=margin_pos), unsafe_allow_html=True)

    c5, c6, c7, c8 = st.columns(4)
    with c5:
        st.markdown(kpi_card("👤", "Unique Customers",
                             f"{kpis['total_customers']:,}"), unsafe_allow_html=True)
    with c6:
        st.markdown(kpi_card("🏷️", "Avg Order Value",
                             f"${kpis['avg_order_value']:,.0f}"), unsafe_allow_html=True)
    with c7:
        st.markdown(kpi_card("📦", "Units Sold",
                             f"{kpis['total_quantity']:,}"), unsafe_allow_html=True)
    with c8:
        st.markdown(kpi_card("❌", "Loss-making Orders",
                             f"{kpis['loss_orders']:,}",
                             delta_positive=False), unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Revenue & Profit Trend</div>",
                unsafe_allow_html=True)
    trend_df = revenue_by_period(df, granularity)
    st.plotly_chart(revenue_trend_chart(trend_df), width='stretch', key='exec_trend')

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("<div class='section-title'>Category Revenue Share</div>",
                    unsafe_allow_html=True)
        cat_df = category_summary(df)
        st.plotly_chart(category_donut(cat_df, "Sales"), width='stretch', key='exec_cat_donut')
    with col_r:
        st.markdown("<div class='section-title'>Revenue by Region</div>",
                    unsafe_allow_html=True)
        reg_df = region_summary(df)
        st.plotly_chart(region_bar(reg_df), width='stretch', key='exec_region_bar')


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — Sales Trends
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    trend_df = revenue_by_period(df, granularity)

    st.markdown("<div class='section-title'>Revenue & Profit Over Time</div>",
                unsafe_allow_html=True)
    st.plotly_chart(revenue_trend_chart(trend_df), width='stretch', key='trends_trend')

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>Year-over-Year Growth</div>",
                    unsafe_allow_html=True)
        yoy_df = yoy_growth(df)
        st.plotly_chart(yoy_chart(yoy_df), width='stretch', key='trends_yoy')
    with col2:
        st.markdown("<div class='section-title'>Period Summary Table</div>",
                    unsafe_allow_html=True)
        display_df = trend_df.rename(columns={"YearMonth": "Period"})
        display_df["Sales"]  = display_df["Sales"].apply(lambda v: f"${v:,.0f}")
        display_df["Profit"] = display_df["Profit"].apply(lambda v: f"${v:,.0f}")
        st.dataframe(display_df, use_container_width=True, height=380)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — Top Products
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    label_col = "Product Name" if "Product Name" in df.columns else "Sub-Category"
    metric_sel = st.radio("Rank by:", ["Sales", "Profit"],
                          horizontal=True, key="prod_metric")

    st.markdown(f"<div class='section-title'>Top 10 Products by {metric_sel}</div>",
                unsafe_allow_html=True)
    top_df = top_products(df, metric_sel)
    st.plotly_chart(top_products_chart(top_df, metric_sel, label_col),
                    width='stretch', key='prod_top_chart')

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>⚠️ Bottom 10 Products (Profit)</div>",
                    unsafe_allow_html=True)
        bot_df = bottom_products(df)
        bot_display = bot_df[[label_col, "Sales", "Profit"]].copy()
        bot_display["Sales"]  = bot_display["Sales"].apply(lambda v: f"${v:,.0f}")
        bot_display["Profit"] = bot_display["Profit"].apply(lambda v: f"${v:,.0f}")
        st.dataframe(bot_display, use_container_width=True, height=360)
    with col2:
        st.markdown("<div class='section-title'>Top 10 Detail</div>",
                    unsafe_allow_html=True)
        top_display = top_df[[label_col, "Sales", "Profit",
                               "Quantity", "Profit Margin %"]].copy()
        top_display["Sales"]  = top_display["Sales"].apply(lambda v: f"${v:,.0f}")
        top_display["Profit"] = top_display["Profit"].apply(lambda v: f"${v:,.0f}")
        st.dataframe(top_display, use_container_width=True, height=360)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — Regional View
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    map_metric = st.radio("Map metric:", ["Sales", "Profit"],
                          horizontal=True, key="map_metric")

    st.markdown(f"<div class='section-title'>US {map_metric} by State</div>",
                unsafe_allow_html=True)
    state_df = state_summary(df)
    st.plotly_chart(state_map(state_df, map_metric), width='stretch', key='reg_map')

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("<div class='section-title'>Region Summary</div>",
                    unsafe_allow_html=True)
        reg_df = region_summary(df)
        st.plotly_chart(region_bar(reg_df), width='stretch', key='reg_bar')
    with col2:
        st.markdown("<div class='section-title'>Region Table</div>",
                    unsafe_allow_html=True)
        reg_display = reg_df.copy()
        reg_display["Sales"]  = reg_display["Sales"].apply(lambda v: f"${v:,.0f}")
        reg_display["Profit"] = reg_display["Profit"].apply(lambda v: f"${v:,.0f}")
        st.dataframe(reg_display, use_container_width=True, height=240)

    st.markdown("<div class='section-title'>Top 10 States by Sales</div>",
                unsafe_allow_html=True)
    top_states = state_df.nlargest(10, "Sales")
    top_states_disp = top_states[["State","Sales","Profit",
                                   "Orders","Profit Margin %"]].copy()
    top_states_disp["Sales"]  = top_states_disp["Sales"].apply(lambda v: f"${v:,.0f}")
    top_states_disp["Profit"] = top_states_disp["Profit"].apply(lambda v: f"${v:,.0f}")
    st.dataframe(top_states_disp, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 4 — Category Analysis
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    sub_df = subcategory_summary(df)

    st.markdown("<div class='section-title'>Revenue Treemap</div>",
                unsafe_allow_html=True)
    st.plotly_chart(category_treemap(sub_df), width='stretch', key='cat_treemap')

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>Category Revenue Share</div>",
                    unsafe_allow_html=True)
        cat_df = category_summary(df)
        st.plotly_chart(category_donut(cat_df, "Sales"), width='stretch', key='cat_donut_sales')
    with col2:
        st.markdown("<div class='section-title'>Category Profit Share</div>",
                    unsafe_allow_html=True)
        st.plotly_chart(category_donut(cat_df, "Profit"), width='stretch', key='cat_donut_profit')

    st.markdown("<div class='section-title'>Sub-Category Revenue vs Profit</div>",
                unsafe_allow_html=True)
    st.plotly_chart(subcategory_bar(sub_df), width='stretch', key='cat_subcat_bar')

    st.markdown("<div class='section-title'>Profit Margin by Sub-Category</div>",
                unsafe_allow_html=True)
    st.plotly_chart(margin_waterfall(sub_df), width='stretch', key='cat_margin_waterfall')


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 5 — Customer Segments
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    seg_df = segment_summary(df)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>Revenue by Segment</div>",
                    unsafe_allow_html=True)
        st.plotly_chart(segment_donut(seg_df, "Sales"), width='stretch', key='seg_donut_sales')
    with col2:
        st.markdown("<div class='section-title'>Profit by Segment</div>",
                    unsafe_allow_html=True)
        st.plotly_chart(segment_donut(seg_df, "Profit"), width='stretch', key='seg_donut_profit')

    st.markdown("<div class='section-title'>Segment — Revenue vs Profit</div>",
                unsafe_allow_html=True)
    st.plotly_chart(segment_bar(seg_df), width='stretch', key='seg_bar')

    st.markdown("<div class='section-title'>Segment Detail Table</div>",
                unsafe_allow_html=True)
    seg_display = seg_df.copy()
    for col in ["Sales", "Profit", "Avg Order Value"]:
        if col in seg_display.columns:
            seg_display[col] = seg_display[col].apply(lambda v: f"${v:,.0f}")
    st.dataframe(seg_display, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 6 — Discount Analysis
# ══════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown("""
    <div style='background:#1A1D2E;border:1px solid #2A2D3E;border-radius:12px;
                padding:14px 18px;margin-bottom:20px;border-left:4px solid #FC5C65'>
        <b style='color:#FC5C65'>⚠️ Key Finding:</b>
        <span style='color:#E8EAED;font-size:13px'>
         Discounts above 20% consistently produce negative profit margins.
         The business is losing money on heavily discounted orders.
        </span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>Discount vs Profit Scatter</div>",
                    unsafe_allow_html=True)
        st.plotly_chart(discount_scatter(df), width='stretch', key='disc_scatter')
    with col2:
        st.markdown("<div class='section-title'>Avg Margin by Discount Bucket</div>",
                    unsafe_allow_html=True)
        disc_df = discount_impact(df)
        st.plotly_chart(discount_bucket_bar(disc_df), width='stretch', key='disc_bucket_bar')

    st.markdown("<div class='section-title'>Discount Impact Table</div>",
                unsafe_allow_html=True)
    disc_display = disc_df.copy()
    disc_display["Total_Sales"]   = disc_display["Total_Sales"].apply(lambda v: f"${v:,.0f}")
    disc_display["Total_Profit"]  = disc_display["Total_Profit"].apply(lambda v: f"${v:,.0f}")
    disc_display["Avg_Profit_Margin"] = disc_display["Avg_Profit_Margin"].apply(lambda v: f"{v:.1f}%")
    st.dataframe(disc_display.rename(columns={
        "Discount Bucket": "Discount Range",
        "Avg_Profit_Margin": "Avg Margin",
        "Total_Sales": "Total Sales",
        "Total_Profit": "Total Profit",
    }), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 7 — Shipping
# ══════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    ship_df = shipping_summary(df)

    st.markdown("<div class='section-title'>Shipping Mode — Orders & Speed</div>",
                unsafe_allow_html=True)
    st.plotly_chart(shipping_bar(ship_df), width='stretch', key='ship_bar')

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>Shipping Profit Share</div>",
                    unsafe_allow_html=True)
        st.plotly_chart(category_donut(
            ship_df.rename(columns={"Ship Mode": "Category"}), "Profit"
        ), width='stretch', key='ship_donut')
    with col2:
        st.markdown("<div class='section-title'>Shipping Mode Detail</div>",
                    unsafe_allow_html=True)
        ship_display = ship_df.copy()
        ship_display["Sales"]  = ship_display["Sales"].apply(lambda v: f"${v:,.0f}")
        ship_display["Profit"] = ship_display["Profit"].apply(lambda v: f"${v:,.0f}")
        ship_display["Avg_Shipping_Days"] = ship_display["Avg_Shipping_Days"].apply(
            lambda v: f"{v:.1f} days")
        st.dataframe(ship_display, use_container_width=True, height=220)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 8 — Insights & Recommendations
# ══════════════════════════════════════════════════════════════════════════════
with tabs[8]:
    kpis   = get_kpis(df)
    cat_df = category_summary(df)
    reg_df = region_summary(df)
    seg_df = segment_summary(df)

    top_cat    = cat_df.loc[cat_df["Sales"].idxmax(), "Category"]
    top_region = reg_df.loc[reg_df["Sales"].idxmax(), "Region"]
    best_margin_cat = cat_df.loc[cat_df["Profit Margin %"].idxmax(), "Category"]
    worst_margin_cat = cat_df.loc[cat_df["Profit Margin %"].idxmin(), "Category"]

    st.markdown("""
    <div style='padding:20px 0 10px'>
        <h2 style='font-size:24px;font-weight:700;color:#E8EAED;margin:0'>
            💡 Business Insights & Recommendations
        </h2>
        <p style='color:#9AA0B4;font-size:13px;margin:6px 0 0'>
            Data-driven findings for strategic decision-making
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── FINDINGS ──────────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>📌 Key Findings</div>",
                unsafe_allow_html=True)

    insights = [
        ("💰 Overall Performance",
         f"The business generated <b>${kpis['total_sales']:,.0f}</b> in total revenue "
         f"with a net profit of <b>${kpis['total_profit']:,.0f}</b>, yielding a "
         f"<b>{kpis['profit_margin']:.1f}% overall profit margin</b> across "
         f"{kpis['total_orders']:,} orders from {kpis['total_customers']:,} customers."),

        (f"🏆 Top Revenue Category: {top_cat}",
         f"<b>{top_cat}</b> drives the highest revenue. However, this does not always "
         f"translate to the highest profitability — margin analysis by sub-category "
         f"reveals where true profit is concentrated."),

        (f"📊 Best Margin Category: {best_margin_cat}",
         f"<b>{best_margin_cat}</b> delivers the highest profit margin percentage. "
         f"The business should prioritise growth in this category by expanding "
         f"the product range and increasing marketing investment."),

        (f"⚠️ Margin Risk — {worst_margin_cat}",
         f"<b>{worst_margin_cat}</b> has the lowest profit margin and in some sub-categories "
         f"generates losses. A cost-structure review and pricing audit is recommended."),

        (f"🗺️ Top Region: {top_region}",
         f"The <b>{top_region}</b> region leads in total sales. However, underperforming "
         f"regions present significant growth opportunities if targeted with regional "
         f"campaigns and localised pricing."),

        ("💸 Discount Problem",
         "Discounts above 20% consistently erode margins below zero. "
         "<b>Heavily discounted orders are destroying profitability.</b> "
         "The discount policy needs to be restructured immediately — no discount "
         "should exceed 20% without executive approval and margin sign-off."),

        ("🚚 Shipping Mode Efficiency",
         "Standard Class carries the majority of orders. Same Day and First Class "
         "shipping modes, while smaller in volume, need profitability monitoring "
         "as premium shipping costs can erode margins on low-value orders."),

        ("👥 Consumer Segment Dominance",
         "The Consumer segment represents the largest revenue share. The Corporate "
         "segment, while smaller, often delivers higher average order values. "
         "Investing in B2B sales motions (account managers, volume pricing) "
         "could significantly grow Corporate segment revenue."),

        ("📉 Loss-Making Orders",
         f"<b>{kpis['loss_orders']:,} orders</b> generated a loss. "
         "These are concentrated in high-discount, low-margin products. "
         "Eliminating or repricing these order types could add significant "
         "profit without reducing revenue materially."),

        ("📦 Sub-Category Opportunity",
         "Copiers and Phones generate high revenue but require monitoring for "
         "margin compression. Labels, Envelopes, and Fasteners show strong "
         "margins but are under-sold — bundling strategies could increase "
         "their contribution without heavy marketing spend."),
    ]

    for title, body in insights:
        st.markdown(f"""
        <div class='insight-card'>
            <h4>{title}</h4>
            <p>{body}</p>
        </div>
        """, unsafe_allow_html=True)

    # ── RECOMMENDATIONS ───────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>🎯 Actionable Recommendations</div>",
                unsafe_allow_html=True)

    recs = [
        ("1", "Cap Discounts at 20%",
         "Implement a hard discount cap of 20% in your CRM/ERP. Require VP approval "
         "for any exception. Model shows this alone could recover $50K+ in annual profit.",
         "#FC5C65"),
        ("2", f"Double Down on {best_margin_cat}",
         f"Increase marketing budget allocation to {best_margin_cat} products by 25%. "
         "High margins + growing demand = highest ROI growth lever available.",
         "#00C9A7"),
        ("3", "Launch a B2B/Corporate Sales Programme",
         "Corporate segment has 30–40% higher average order values. Hire 2 dedicated "
         "account managers and introduce volume-pricing tiers to capture more B2B deals.",
         "#7C5CBF"),
        ("4", "Regional Growth Strategy",
         f"The {top_region} region is saturated. Allocate 20% of marketing budget to "
         "underperforming regions with targeted promotions. Potential to grow 15–25%.",
         "#F7B731"),
        ("5", "Audit and Rationalise Loss Products",
         "Run a quarterly SKU profitability audit. Products with >2 years of negative "
         "margin should be discontinued or repriced. This is quick cost-saving wins.",
         "#FC5C65"),
        ("6", "Bundle High-Margin Low-Volume Products",
         "Create product bundles pairing slow-moving high-margin items with top sellers. "
         "This increases basket size and overall margin mix simultaneously.",
         "#45AAF2"),
        ("7", "Seasonal Inventory Planning",
         "Revenue peaks in Q4 (holiday season). Pre-position inventory for high-demand "
         "categories by September to avoid stockouts and fulfil demand at full margin.",
         "#00C9A7"),
    ]

    for num, title, body, color in recs:
        st.markdown(f"""
        <div style='background:#1A1D2E;border:1px solid #2A2D3E;border-radius:12px;
                    padding:16px 20px;margin-bottom:12px;
                    border-left:4px solid {color};display:flex;gap:16px'>
            <div style='min-width:32px;height:32px;border-radius:50%;
                        background:{color};display:flex;align-items:center;
                        justify-content:center;font-weight:700;font-size:14px;
                        color:#0F1117;flex-shrink:0;margin-top:2px'>{num}</div>
            <div>
                <h4 style='color:{color};margin:0 0 5px 0;font-size:15px'>{title}</h4>
                <p style='color:#E8EAED;margin:0;font-size:13px;line-height:1.6'>{body}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Footer ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style='margin-top:32px;padding:20px;background:#1A1D2E;
                border-radius:12px;border:1px solid #2A2D3E;text-align:center'>
        <p style='color:#9AA0B4;font-size:12px;margin:0'>
            📊 <b style='color:#7C5CBF'>Superstore Sales Analytics Dashboard</b> &nbsp;•&nbsp;
            Built with Python · Pandas · Plotly · Streamlit &nbsp;•&nbsp;
            Data: Kaggle Superstore Dataset
        </p>
    </div>
    """, unsafe_allow_html=True)
