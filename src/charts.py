"""
charts.py
---------
All Plotly chart factory functions used by the Streamlit dashboard.
Each function returns a go.Figure ready to pass to st.plotly_chart().
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ── Design tokens ──────────────────────────────────────────────────────────────
PALETTE      = ["#7C5CBF", "#00C9A7", "#F7B731", "#FC5C65",
                "#45AAF2", "#FD9644", "#26DE81", "#A29BFE"]
BG_COLOR     = "#0F1117"
CARD_BG      = "#1A1D2E"
GRID_COLOR   = "#2A2D3E"
TEXT_COLOR   = "#E8EAED"
ACCENT       = "#7C5CBF"
POSITIVE     = "#00C9A7"
NEGATIVE     = "#FC5C65"

LAYOUT_BASE = dict(
    paper_bgcolor=BG_COLOR,
    plot_bgcolor=CARD_BG,
    font=dict(color=TEXT_COLOR, family="Inter, sans-serif", size=13),
    margin=dict(l=40, r=30, t=50, b=40),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=GRID_COLOR),
    colorway=PALETTE,
)


def _apply_base(fig: go.Figure, title: str = "") -> go.Figure:
    fig.update_layout(title=dict(text=title, font=dict(size=16, color=TEXT_COLOR)),
                      **LAYOUT_BASE)
    fig.update_xaxes(showgrid=True, gridcolor=GRID_COLOR, zeroline=False,
                     tickfont=dict(color=TEXT_COLOR))
    fig.update_yaxes(showgrid=True, gridcolor=GRID_COLOR, zeroline=False,
                     tickfont=dict(color=TEXT_COLOR))
    return fig


# ── 1. Revenue & Profit Time Series ───────────────────────────────────────────
def revenue_trend_chart(df: pd.DataFrame, period_col: str = "YearMonth") -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[period_col], y=df["Sales"],
        name="Revenue", mode="lines+markers",
        line=dict(color=ACCENT, width=2.5),
        marker=dict(size=5),
        fill="tozeroy", fillcolor="rgba(124,92,191,0.10)",
    ))
    fig.add_trace(go.Scatter(
        x=df[period_col], y=df["Profit"],
        name="Profit", mode="lines+markers",
        line=dict(color=POSITIVE, width=2.5),
        marker=dict(size=5),
    ))
    _apply_base(fig, "📈 Revenue & Profit Trend")
    fig.update_layout(hovermode="x unified", xaxis_tickangle=-45)
    return fig


# ── 2. Top Products Bar Chart ─────────────────────────────────────────────────
def top_products_chart(df: pd.DataFrame, metric: str = "Sales",
                       label_col: str = "Product Name") -> go.Figure:
    df = df.sort_values(metric, ascending=True).tail(10)
    color = ACCENT if metric == "Sales" else POSITIVE
    fig = go.Figure(go.Bar(
        x=df[metric], y=df[label_col],
        orientation="h",
        marker=dict(
            color=df[metric],
            colorscale=[[0, "#2A2D3E"], [1, color]],
            showscale=False,
        ),
        text=df[metric].apply(lambda v: f"${v:,.0f}"),
        textposition="outside",
        textfont=dict(color=TEXT_COLOR, size=11),
    ))
    _apply_base(fig, f"🏆 Top 10 Products by {metric}")
    fig.update_layout(height=420, xaxis_title=metric, yaxis_title="")
    return fig


# ── 3. Category Donut Chart ───────────────────────────────────────────────────
def category_donut(df: pd.DataFrame, metric: str = "Sales") -> go.Figure:
    fig = go.Figure(go.Pie(
        labels=df["Category"],
        values=df[metric],
        hole=0.55,
        marker=dict(colors=PALETTE[:3],
                    line=dict(color=BG_COLOR, width=3)),
        textinfo="label+percent",
        textfont=dict(color=TEXT_COLOR, size=13),
        hovertemplate="<b>%{label}</b><br>%{value:$,.0f}<extra></extra>",
    ))
    _apply_base(fig, f"Category Split — {metric}")
    fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=50, b=10))
    return fig


# ── 4. Sub-Category Grouped Bar ───────────────────────────────────────────────
def subcategory_bar(df: pd.DataFrame) -> go.Figure:
    df = df.sort_values("Sales", ascending=False)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Sales", x=df["Sub-Category"], y=df["Sales"],
        marker_color=ACCENT,
        hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Profit", x=df["Sub-Category"], y=df["Profit"],
        marker_color=POSITIVE,
        hovertemplate="<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>",
    ))
    _apply_base(fig, "📦 Sales & Profit by Sub-Category")
    fig.update_layout(barmode="group", xaxis_tickangle=-40, height=420)
    return fig


# ── 5. Treemap ────────────────────────────────────────────────────────────────
def category_treemap(df: pd.DataFrame) -> go.Figure:
    fig = px.treemap(
        df,
        path=["Category", "Sub-Category"],
        values="Sales",
        color="Profit Margin %",
        color_continuous_scale=[[0, "#FC5C65"], [0.5, "#F7B731"], [1, "#00C9A7"]],
        color_continuous_midpoint=0,
        hover_data={"Profit": ":$,.0f", "Sales": ":$,.0f"},
    )
    fig.update_traces(textfont=dict(size=14, color="white"))
    _apply_base(fig, "🌳 Revenue Treemap (colour = Profit Margin)")
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10), height=420,
                      coloraxis_colorbar=dict(
                          title="Margin %", tickfont=dict(color=TEXT_COLOR)))
    return fig


# ── 6. Region Bar Chart ───────────────────────────────────────────────────────
def region_bar(df: pd.DataFrame) -> go.Figure:
    df = df.sort_values("Sales", ascending=False)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Sales", x=df["Region"], y=df["Sales"],
        marker_color=ACCENT, text=df["Sales"].apply(lambda v: f"${v/1e3:.0f}K"),
        textposition="outside", textfont=dict(color=TEXT_COLOR),
    ))
    fig.add_trace(go.Bar(
        name="Profit", x=df["Region"], y=df["Profit"],
        marker_color=POSITIVE, text=df["Profit"].apply(lambda v: f"${v/1e3:.0f}K"),
        textposition="outside", textfont=dict(color=TEXT_COLOR),
    ))
    _apply_base(fig, "🗺️ Sales & Profit by Region")
    fig.update_layout(barmode="group", height=380)
    return fig


# ── 7. US Choropleth Map ──────────────────────────────────────────────────────
def state_map(df: pd.DataFrame, metric: str = "Sales") -> go.Figure:
    # State name → abbreviation mapping
    state_abbrev = {
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
        "California": "CA", "Colorado": "CO", "Connecticut": "CT",
        "Delaware": "DE", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI",
        "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
        "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME",
        "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI",
        "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
        "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
        "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
        "New York": "NY", "North Carolina": "NC", "North Dakota": "ND",
        "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
        "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
        "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
        "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
        "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC",
    }
    df = df.copy()
    df["State Code"] = df["State"].map(state_abbrev)
    df = df.dropna(subset=["State Code"])

    fig = px.choropleth(
        df,
        locations="State Code",
        locationmode="USA-states",
        color=metric,
        scope="usa",
        color_continuous_scale=[[0, "#1A1D2E"], [0.5, "#7C5CBF"], [1, "#00C9A7"]],
        hover_name="State",
        hover_data={metric: ":$,.0f", "Orders": True},
        labels={metric: metric},
    )
    fig.update_geos(bgcolor=BG_COLOR, lakecolor=BG_COLOR,
                    landcolor="#1A1D2E", showframe=False)
    _apply_base(fig, f"🗺️ {metric} by State")
    fig.update_layout(
        geo=dict(bgcolor=BG_COLOR),
        coloraxis_colorbar=dict(title=metric, tickfont=dict(color=TEXT_COLOR)),
        height=440,
    )
    return fig


# ── 8. Segment Donut ──────────────────────────────────────────────────────────
def segment_donut(df: pd.DataFrame, metric: str = "Sales") -> go.Figure:
    fig = go.Figure(go.Pie(
        labels=df["Segment"], values=df[metric],
        hole=0.55,
        marker=dict(colors=[ACCENT, POSITIVE, "#F7B731"],
                    line=dict(color=BG_COLOR, width=3)),
        textinfo="label+percent",
        textfont=dict(color=TEXT_COLOR, size=13),
        hovertemplate="<b>%{label}</b><br>%{value:$,.0f}<extra></extra>",
    ))
    _apply_base(fig, f"👥 Segment Split — {metric}")
    fig.update_layout(showlegend=True, margin=dict(l=10, r=10, t=50, b=10))
    return fig


# ── 9. Segment Grouped Bar ────────────────────────────────────────────────────
def segment_bar(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Sales", x=df["Segment"], y=df["Sales"],
        marker_color=ACCENT,
        text=df["Sales"].apply(lambda v: f"${v/1e3:.0f}K"),
        textposition="outside", textfont=dict(color=TEXT_COLOR),
    ))
    fig.add_trace(go.Bar(
        name="Profit", x=df["Segment"], y=df["Profit"],
        marker_color=POSITIVE,
        text=df["Profit"].apply(lambda v: f"${v/1e3:.0f}K"),
        textposition="outside", textfont=dict(color=TEXT_COLOR),
    ))
    _apply_base(fig, "Customer Segment — Revenue vs Profit")
    fig.update_layout(barmode="group", height=360)
    return fig


# ── 10. Discount vs Profit Scatter ────────────────────────────────────────────
def discount_scatter(df: pd.DataFrame) -> go.Figure:
    sample = df.sample(min(2000, len(df)), random_state=42).copy()

    # Manual linear trendline via numpy polyfit (no statsmodels needed)
    x_vals = sample["Discount"].values
    y_vals = sample["Profit"].values
    mask = np.isfinite(x_vals) & np.isfinite(y_vals)
    m, b = np.polyfit(x_vals[mask], y_vals[mask], 1)
    x_line = np.linspace(x_vals.min(), x_vals.max(), 100)
    y_line = m * x_line + b

    cats = sample["Category"].unique()
    color_map = {c: PALETTE[i % len(PALETTE)] for i, c in enumerate(cats)}

    fig = go.Figure()
    for cat in cats:
        sub = sample[sample["Category"] == cat]
        fig.add_trace(go.Scatter(
            x=sub["Discount"], y=sub["Profit"],
            mode="markers", name=cat,
            marker=dict(color=color_map[cat], size=6, opacity=0.55),
            hovertemplate=(
                f"<b>{cat}</b><br>"
                "Discount: %{x:.0%}<br>"
                "Profit: $%{y:,.0f}<extra></extra>"
            ),
        ))

    # Trendline
    fig.add_trace(go.Scatter(
        x=x_line, y=y_line,
        mode="lines", name="Trend",
        line=dict(color="#F7B731", width=2.5, dash="dash"),
        hoverinfo="skip",
    ))

    _apply_base(fig, "💸 Discount vs Profit (scatter + trend)")
    fig.update_layout(height=400,
                      xaxis=dict(tickformat=".0%", title="Discount Applied"),
                      yaxis_title="Profit ($)")
    return fig



# ── 11. Discount Bucket Bar ───────────────────────────────────────────────────
def discount_bucket_bar(df: pd.DataFrame) -> go.Figure:
    colors = [POSITIVE if v >= 0 else NEGATIVE
              for v in df["Avg_Profit_Margin"]]
    fig = go.Figure(go.Bar(
        x=df["Discount Bucket"].astype(str),
        y=df["Avg_Profit_Margin"],
        marker_color=colors,
        text=df["Avg_Profit_Margin"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside",
        textfont=dict(color=TEXT_COLOR),
    ))
    fig.add_hline(y=0, line_dash="dash", line_color=NEGATIVE, line_width=1.5)
    _apply_base(fig, "Avg Profit Margin by Discount Bucket")
    fig.update_layout(height=360, xaxis_title="Discount Range",
                      yaxis_title="Avg Profit Margin %")
    return fig


# ── 12. Shipping Mode Bar ─────────────────────────────────────────────────────
def shipping_bar(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Orders", x=df["Ship Mode"], y=df["Orders"],
        marker_color=ACCENT, yaxis="y1",
        text=df["Orders"], textposition="outside",
        textfont=dict(color=TEXT_COLOR),
    ))
    fig.add_trace(go.Scatter(
        name="Avg Ship Days", x=df["Ship Mode"],
        y=df["Avg_Shipping_Days"],
        mode="lines+markers+text",
        marker=dict(color=POSITIVE, size=10),
        line=dict(color=POSITIVE, width=2.5),
        text=df["Avg_Shipping_Days"].apply(lambda v: f"{v:.1f}d"),
        textposition="top center",
        textfont=dict(color=POSITIVE),
        yaxis="y2",
    ))
    _apply_base(fig, "🚚 Shipping Mode — Orders & Avg Shipping Days")
    fig.update_layout(
        yaxis=dict(title="Order Count", showgrid=False),
        yaxis2=dict(title="Avg Days", overlaying="y", side="right",
                    showgrid=False, tickfont=dict(color=POSITIVE)),
        barmode="group", height=380,
    )
    return fig


# ── 13. YoY Growth ───────────────────────────────────────────────────────────
def yoy_chart(df: pd.DataFrame) -> go.Figure:
    df = df.dropna(subset=["Sales Growth %"])
    colors = [POSITIVE if v >= 0 else NEGATIVE for v in df["Sales Growth %"]]
    fig = go.Figure(go.Bar(
        x=df["Year"].astype(str),
        y=df["Sales Growth %"],
        marker_color=colors,
        text=df["Sales Growth %"].apply(lambda v: f"{v:+.1f}%"),
        textposition="outside",
        textfont=dict(color=TEXT_COLOR),
    ))
    _apply_base(fig, "📊 Year-over-Year Sales Growth")
    fig.update_layout(height=340, xaxis_title="Year",
                      yaxis_title="Sales Growth %")
    return fig


# ── 14. Profit Margin Waterfall by Sub-Category ───────────────────────────────
def margin_waterfall(df: pd.DataFrame) -> go.Figure:
    df = df.sort_values("Profit Margin %", ascending=False).head(15)
    colors = [POSITIVE if v >= 0 else NEGATIVE
              for v in df["Profit Margin %"]]
    fig = go.Figure(go.Bar(
        x=df["Sub-Category"],
        y=df["Profit Margin %"],
        marker_color=colors,
        text=df["Profit Margin %"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside",
        textfont=dict(color=TEXT_COLOR),
    ))
    fig.add_hline(y=0, line_dash="dash", line_color=NEGATIVE, line_width=1.5)
    _apply_base(fig, "Profit Margin % by Sub-Category")
    fig.update_layout(height=380, xaxis_tickangle=-35)
    return fig
