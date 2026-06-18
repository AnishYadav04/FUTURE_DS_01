"""
data_loader.py
--------------
Loads, cleans, and engineers features from the Superstore dataset.
Run standalone to verify the data pipeline:
    python src/data_loader.py
"""

import os
import io
import requests
import pandas as pd
import numpy as np

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR   = os.path.join(ROOT_DIR, "data")
DATA_PATH  = os.path.join(DATA_DIR, "superstore.csv")

# ── Public mirror of the Superstore dataset ────────────────────────────────────
DATA_URL = (
    "https://raw.githubusercontent.com/dsrscientist/"
    "dataset1/master/salesdata.csv"
)

# ── Fallback: generate a realistic synthetic dataset ──────────────────────────
def _generate_synthetic_data() -> pd.DataFrame:
    """
    Generates ~10 000 rows of synthetic Superstore-style data so the dashboard
    always has something to display even if the remote file is unavailable.
    """
    np.random.seed(42)
    n = 9994

    categories = {
        "Furniture":      ["Chairs", "Tables", "Bookcases", "Furnishings"],
        "Office Supplies": ["Binders", "Paper", "Storage", "Art",
                            "Appliances", "Envelopes", "Labels", "Fasteners"],
        "Technology":     ["Phones", "Accessories", "Machines", "Copiers"],
    }
    regions   = ["West", "East", "Central", "South"]
    segments  = ["Consumer", "Corporate", "Home Office"]
    ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]
    states_by_region = {
        "West":    ["California", "Washington", "Oregon", "Nevada", "Arizona",
                    "Colorado", "Utah", "Montana", "Idaho"],
        "East":    ["New York", "Pennsylvania", "Ohio", "Virginia",
                    "Massachusetts", "Connecticut", "New Jersey", "Maryland"],
        "Central": ["Texas", "Illinois", "Michigan", "Missouri", "Wisconsin",
                    "Minnesota", "Indiana", "Kansas", "Nebraska"],
        "South":   ["Florida", "North Carolina", "Georgia", "Tennessee",
                    "Alabama", "Louisiana", "Mississippi", "Arkansas"],
    }

    rows = []
    order_id = 10000
    for i in range(n):
        region   = np.random.choice(regions)
        state    = np.random.choice(states_by_region[region])
        cat      = np.random.choice(list(categories.keys()))
        sub_cat  = np.random.choice(categories[cat])
        segment  = np.random.choice(segments)
        ship_mode = np.random.choice(
            ship_modes, p=[0.60, 0.20, 0.15, 0.05]
        )

        order_date = pd.Timestamp("2019-01-01") + pd.to_timedelta(
            np.random.randint(0, 365 * 4), unit="D"
        )
        ship_lag   = {"Standard Class": 5, "Second Class": 3,
                      "First Class": 2, "Same Day": 1}[ship_mode]
        ship_date  = order_date + pd.Timedelta(days=ship_lag +
                                               np.random.randint(0, 2))

        # Pricing model
        base_price = {
            "Furniture": np.random.uniform(80, 1500),
            "Office Supplies": np.random.uniform(5, 300),
            "Technology": np.random.uniform(50, 3000),
        }[cat]
        quantity  = np.random.randint(1, 14)
        discount  = np.random.choice([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
                                     p=[0.40, 0.20, 0.18, 0.10, 0.05,
                                        0.04, 0.02, 0.01])
        sales     = round(base_price * quantity * (1 - discount), 2)

        # Profit margin varies by category and discount
        base_margin = {
            "Furniture": 0.10, "Office Supplies": 0.25, "Technology": 0.20
        }[cat]
        margin     = base_margin - (discount * 1.5) + np.random.normal(0, 0.05)
        profit     = round(sales * margin, 2)

        rows.append({
            "Row ID":        i + 1,
            "Order ID":      f"CA-{order_id + i}-{i:04d}",
            "Order Date":    order_date,
            "Ship Date":     ship_date,
            "Ship Mode":     ship_mode,
            "Customer ID":   f"CG-{np.random.randint(10000, 99999)}",
            "Customer Name": f"Customer {i % 800}",
            "Segment":       segment,
            "Country":       "United States",
            "City":          state + " City",
            "State":         state,
            "Postal Code":   np.random.randint(10000, 99999),
            "Region":        region,
            "Product ID":    f"OFF-{np.random.randint(1000, 9999)}",
            "Category":      cat,
            "Sub-Category":  sub_cat,
            "Product Name":  f"{sub_cat} Item {np.random.randint(1, 50)}",
            "Sales":         sales,
            "Quantity":      quantity,
            "Discount":      discount,
            "Profit":        profit,
        })

    return pd.DataFrame(rows)


# ── Loader ─────────────────────────────────────────────────────────────────────
def load_raw_data() -> pd.DataFrame:
    """
    Priority order:
      1. Local CSV  → c:/anni/superstore-analytics/data/superstore.csv
      2. Remote URL → GitHub mirror
      3. Synthetic  → procedurally generated fallback
    """
    os.makedirs(DATA_DIR, exist_ok=True)

    # 1. Local file
    if os.path.exists(DATA_PATH):
        print(f"[data_loader] Loading local file: {DATA_PATH}")
        df = pd.read_csv(DATA_PATH, encoding="latin-1")
        return df

    # 2. Remote fetch
    print(f"[data_loader] Fetching remote dataset …")
    try:
        r = requests.get(DATA_URL, timeout=15)
        r.raise_for_status()
        df = pd.read_csv(io.StringIO(r.text), encoding="latin-1")
        df.to_csv(DATA_PATH, index=False)
        print(f"[data_loader] Saved to {DATA_PATH}")
        return df
    except Exception as e:
        print(f"[data_loader] Remote fetch failed: {e}")

    # 3. Synthetic fallback
    print("[data_loader] Using synthetic dataset.")
    df = _generate_synthetic_data()
    df.to_csv(DATA_PATH, index=False)
    return df


# ── Cleaner ────────────────────────────────────────────────────────────────────
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardises column names, parses dates, drops duplicates,
    and engineers all derived features needed by the analysis layer.
    """
    # ── Column name normalisation ──────────────────────────────────────────────
    df.columns = df.columns.str.strip()

    # Map common alternate column names to the canonical schema
    rename_map = {
        "order_date": "Order Date", "orderdate": "Order Date",
        "ship_date":  "Ship Date",  "shipdate":  "Ship Date",
        "order_id":   "Order ID",   "orderid":   "Order ID",
        "customer_id":"Customer ID",
        "customer_name": "Customer Name",
        "ship_mode":  "Ship Mode",
        "product_id": "Product ID",
        "product_name": "Product Name",
        "sub_category": "Sub-Category", "subcategory": "Sub-Category",
    }
    df = df.rename(columns={c: rename_map.get(c.lower(), c) for c in df.columns})

    # ── Drop exact duplicate rows ──────────────────────────────────────────────
    df = df.drop_duplicates()

    # ── Date parsing ──────────────────────────────────────────────────────────
    for col in ["Order Date", "Ship Date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # ── Numeric coercion ──────────────────────────────────────────────────────
    for col in ["Sales", "Quantity", "Discount", "Profit"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Sales", "Profit", "Order Date"])

    # ── Derived time columns ───────────────────────────────────────────────────
    df["Year"]       = df["Order Date"].dt.year
    df["Month"]      = df["Order Date"].dt.month
    df["Quarter"]    = df["Order Date"].dt.quarter
    df["YearMonth"]  = df["Order Date"].dt.to_period("M").astype(str)
    df["YearQuarter"]= (df["Year"].astype(str) + " Q"
                        + df["Quarter"].astype(str))

    # ── Shipping days ──────────────────────────────────────────────────────────
    if "Ship Date" in df.columns:
        df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
        df["Shipping Days"] = df["Shipping Days"].clip(lower=0)

    # ── Derived financial columns ──────────────────────────────────────────────
    df["Profit Margin %"] = np.where(
        df["Sales"] != 0,
        (df["Profit"] / df["Sales"] * 100).round(2),
        0.0
    )
    df["Revenue per Unit"] = np.where(
        df.get("Quantity", pd.Series(dtype=float)).fillna(0) != 0,
        df["Sales"] / df["Quantity"],
        df["Sales"]
    )
    df["Is Loss"] = df["Profit"] < 0

    return df


# ── Public API ─────────────────────────────────────────────────────────────────
def get_data() -> pd.DataFrame:
    """One-call convenience: load + clean. Memoised at module level."""
    raw = load_raw_data()
    return clean_data(raw)


# ── Standalone test ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import io, sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    df = get_data()
    print("\n-- Shape -------------------------------------")
    print(df.shape)
    print("\n-- Columns -----------------------------------")
    print(df.dtypes)
    print("\n-- Sales / Profit summary --------------------")
    print(df[["Sales", "Profit", "Profit Margin %"]].describe().round(2))
    print("\n-- Year distribution -------------------------")
    print(df["Year"].value_counts().sort_index())
