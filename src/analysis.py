"""
analysis.py
-----------
All business analysis functions that power the dashboard.
Each function accepts a cleaned DataFrame and returns an aggregated DataFrame
ready for charting.

Run standalone to verify outputs:
    python src/analysis.py
"""

import pandas as pd
import numpy as np


# ── KPI Summary ───────────────────────────────────────────────────────────────
def get_kpis(df: pd.DataFrame) -> dict:
    """Return top-level KPI metrics."""
    total_sales     = df["Sales"].sum()
    total_profit    = df["Profit"].sum()
    total_orders    = df["Order ID"].nunique()
    total_customers = df["Customer ID"].nunique() if "Customer ID" in df else 0
    avg_order_value = total_sales / total_orders if total_orders else 0
    profit_margin   = (total_profit / total_sales * 100) if total_sales else 0
    total_quantity  = df["Quantity"].sum() if "Quantity" in df else 0
    loss_orders     = df[df["Profit"] < 0]["Order ID"].nunique()

    return {
        "total_sales":      round(total_sales, 2),
        "total_profit":     round(total_profit, 2),
        "total_orders":     int(total_orders),
        "total_customers":  int(total_customers),
        "avg_order_value":  round(avg_order_value, 2),
        "profit_margin":    round(profit_margin, 2),
        "total_quantity":   int(total_quantity),
        "loss_orders":      int(loss_orders),
    }


# ── Time Series ───────────────────────────────────────────────────────────────
def revenue_by_period(df: pd.DataFrame, granularity: str = "Monthly") -> pd.DataFrame:
    """
    Aggregate Sales and Profit by time period.
    granularity: 'Monthly' | 'Quarterly' | 'Yearly'
    """
    if granularity == "Monthly":
        group_col = "YearMonth"
        df = df.sort_values("Order Date")
        agg = (df.groupby("YearMonth", sort=False)
                 .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
                      Orders=("Order ID", "nunique"))
                 .reset_index())
        # Preserve chronological order
        agg["_sort"] = pd.to_datetime(agg["YearMonth"])
        agg = agg.sort_values("_sort").drop(columns="_sort")
    elif granularity == "Quarterly":
        agg = (df.groupby("YearQuarter")
                 .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
                      Orders=("Order ID", "nunique"))
                 .reset_index()
                 .rename(columns={"YearQuarter": "YearMonth"}))
        agg["_sort"] = agg["YearMonth"].apply(
            lambda x: (int(x[:4]), int(x[-1]))
        )
        agg = agg.sort_values("_sort").drop(columns="_sort")
    else:  # Yearly
        agg = (df.groupby("Year")
                 .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
                      Orders=("Order ID", "nunique"))
                 .reset_index()
                 .rename(columns={"Year": "YearMonth"})
                 .sort_values("YearMonth"))
        agg["YearMonth"] = agg["YearMonth"].astype(str)

    agg["Profit Margin %"] = (agg["Profit"] / agg["Sales"] * 100).round(2)
    agg["Sales"]  = agg["Sales"].round(2)
    agg["Profit"] = agg["Profit"].round(2)
    return agg


# ── Top Products ──────────────────────────────────────────────────────────────
def top_products(df: pd.DataFrame, metric: str = "Sales",
                 n: int = 10) -> pd.DataFrame:
    """Return top-n products by the chosen metric (Sales or Profit)."""
    col = "Product Name" if "Product Name" in df.columns else "Sub-Category"
    agg = (df.groupby(col)
             .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
                  Quantity=("Quantity", "sum"),
                  Orders=("Order ID", "nunique"))
             .reset_index())
    agg["Profit Margin %"] = (agg["Profit"] / agg["Sales"] * 100).round(2)
    return (agg.sort_values(metric, ascending=False)
               .head(n)
               .round(2))


# ── Bottom Products (Worst performers by profit) ───────────────────────────────
def bottom_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    col = "Product Name" if "Product Name" in df.columns else "Sub-Category"
    agg = (df.groupby(col)
             .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
                  Quantity=("Quantity", "sum"))
             .reset_index()
             .sort_values("Profit", ascending=True)
             .head(n)
             .round(2))
    return agg


# ── Category & Sub-Category ───────────────────────────────────────────────────
def category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Sales, Profit, and Margin by Category."""
    agg = (df.groupby("Category")
             .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
                  Quantity=("Quantity", "sum"),
                  Orders=("Order ID", "nunique"))
             .reset_index())
    agg["Profit Margin %"] = (agg["Profit"] / agg["Sales"] * 100).round(2)
    return agg.round(2)


def subcategory_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Sales, Profit, and Margin by Sub-Category."""
    agg = (df.groupby(["Category", "Sub-Category"])
             .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
                  Quantity=("Quantity", "sum"),
                  Orders=("Order ID", "nunique"))
             .reset_index())
    agg["Profit Margin %"] = (agg["Profit"] / agg["Sales"] * 100).round(2)
    return agg.sort_values("Sales", ascending=False).round(2)


# ── Regional Analysis ─────────────────────────────────────────────────────────
def region_summary(df: pd.DataFrame) -> pd.DataFrame:
    agg = (df.groupby("Region")
             .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
                  Orders=("Order ID", "nunique"),
                  Customers=("Customer ID", "nunique"))
             .reset_index())
    agg["Profit Margin %"] = (agg["Profit"] / agg["Sales"] * 100).round(2)
    return agg.round(2)


def state_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Sales and Profit by US State — used for choropleth map."""
    agg = (df.groupby("State")
             .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
                  Orders=("Order ID", "nunique"))
             .reset_index())
    agg["Profit Margin %"] = (agg["Profit"] / agg["Sales"] * 100).round(2)
    return agg.round(2)


# ── Customer Segment ──────────────────────────────────────────────────────────
def segment_summary(df: pd.DataFrame) -> pd.DataFrame:
    agg = (df.groupby("Segment")
             .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
                  Orders=("Order ID", "nunique"),
                  Customers=("Customer ID", "nunique"))
             .reset_index())
    agg["Profit Margin %"] = (agg["Profit"] / agg["Sales"] * 100).round(2)
    agg["Avg Order Value"]  = (agg["Sales"] / agg["Orders"]).round(2)
    return agg.round(2)


# ── Discount Impact ───────────────────────────────────────────────────────────
def discount_impact(df: pd.DataFrame) -> pd.DataFrame:
    """
    Buckets discount ranges and shows average profit margin per bucket.
    Useful for revealing the discount 'cliff'.
    """
    df = df.copy()
    bins   = [-0.001, 0.001, 0.101, 0.201, 0.301, 0.401, 0.701, 1.01]
    labels = ["0%", "1–10%", "11–20%", "21–30%", "31–40%", "41–70%", ">70%"]
    df["Discount Bucket"] = pd.cut(df["Discount"], bins=bins, labels=labels)
    agg = (df.groupby("Discount Bucket", observed=True)
             .agg(Avg_Profit_Margin=("Profit Margin %", "mean"),
                  Total_Sales=("Sales", "sum"),
                  Total_Profit=("Profit", "sum"),
                  Orders=("Order ID", "nunique"))
             .reset_index()
             .round(2))
    return agg


# ── Shipping Mode ─────────────────────────────────────────────────────────────
def shipping_summary(df: pd.DataFrame) -> pd.DataFrame:
    agg = (df.groupby("Ship Mode")
             .agg(Orders=("Order ID", "nunique"),
                  Sales=("Sales", "sum"),
                  Profit=("Profit", "sum"),
                  Avg_Shipping_Days=("Shipping Days", "mean"))
             .reset_index())
    agg["Profit Margin %"] = (agg["Profit"] / agg["Sales"] * 100).round(2)
    return agg.round(2)


# ── YoY Growth ────────────────────────────────────────────────────────────────
def yoy_growth(df: pd.DataFrame) -> pd.DataFrame:
    """Year-over-year sales and profit growth rates."""
    yr = (df.groupby("Year")
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
            .reset_index()
            .sort_values("Year"))
    yr["Sales Growth %"]  = yr["Sales"].pct_change() * 100
    yr["Profit Growth %"] = yr["Profit"].pct_change() * 100
    return yr.round(2)


# ── Standalone test ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys, os, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.data_loader import get_data

    df = get_data()
    print("\n-- KPIs -------------------------------------------")
    for k, v in get_kpis(df).items():
        print(f"  {k:<22}: {v:,.2f}" if isinstance(v, float) else f"  {k:<22}: {v:,}")

    print("\n-- Revenue by Month (first 5) ---------------------")
    print(revenue_by_period(df, "Monthly").head(5).to_string(index=False))

    print("\n-- Category Summary --------------------------------")
    print(category_summary(df).to_string(index=False))

    print("\n-- Region Summary ----------------------------------")
    print(region_summary(df).to_string(index=False))
