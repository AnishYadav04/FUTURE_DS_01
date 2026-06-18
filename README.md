# 📊 Superstore Sales Analytics Dashboard

> **A client-ready, interactive Python dashboard for retail sales intelligence.**  
> Built for real-world business analysis — suitable for presenting to business owners, startup founders, and analytics clients.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?style=flat-square&logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-5.22-purple?style=flat-square&logo=plotly)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/superstore-analytics.git
cd superstore-analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the dashboard
streamlit run dashboard/app.py
```

The dashboard will open at **http://localhost:8501** in your browser.

> **No data download needed.** The app auto-downloads the dataset on first run. If the download fails, a high-quality synthetic dataset is generated automatically.

---

## 📁 Project Structure

```
superstore-analytics/
│
├── data/
│   └── superstore.csv              # Dataset (auto-downloaded on first run)
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py              # Load, clean & engineer features
│   ├── analysis.py                 # Business analysis aggregations
│   └── charts.py                  # Plotly chart factory (14 chart types)
│
├── dashboard/
│   └── app.py                      # Streamlit multi-tab dashboard
│
├── reports/
│   └── insights_report.md          # Full business insights & recommendations
│
├── notebooks/                      # Jupyter notebooks (optional EDA)
│
├── requirements.txt
└── README.md
```

---

## 🎯 Dashboard Tabs

| Tab | What It Shows |
|-----|--------------|
| 📊 **Executive Summary** | 8 KPI cards, revenue trend, category & region overview |
| 📈 **Sales Trends** | Monthly/Quarterly/Yearly revenue & profit time series, YoY growth |
| 🏆 **Top Products** | Top & bottom 10 products by sales and profit |
| 🗺️ **Regional View** | US choropleth map by state, region comparison table |
| 📦 **Category Analysis** | Treemap, category donuts, sub-category bars, margin chart |
| 👥 **Customer Segments** | Consumer / Corporate / Home Office revenue & profit split |
| 💸 **Discount Analysis** | Scatter plot, discount bucket impact, margin erosion analysis |
| 🚚 **Shipping** | Mode distribution, avg shipping days, profitability by mode |
| 💡 **Insights & Recommendations** | 10 data-driven findings + 7 actionable business recommendations |

---

## 🔍 Key Business Findings

1. **Discounts >20% destroy profitability** — over 1,800 loss-making orders traced to heavy discounting
2. **Office Supplies has the best margins** (~22%) despite not being the top revenue category
3. **Tables (Furniture) are consistently loss-making** — a major profitability drag
4. **West region leads**; South is underperforming despite comparable customer density
5. **Corporate segment** has 30–40% higher average order values than Consumer
6. **Q4 revenue spikes** are predictable and can be planned for each year

---

## 💡 Top Recommendations

| Priority | Action | Est. Impact |
|----------|--------|------------|
| 🔴 URGENT | Cap discounts at 20% | +$60–100K profit/year |
| 🔴 URGENT | Reprice / discontinue Tables | +$20–40K profit/year |
| 🟡 MEDIUM | Launch Corporate B2B programme | +$150K revenue/year |
| 🟡 MEDIUM | Expand Office Supplies range | +$80K revenue/year |
| 🟢 LOW | South region marketing push | +$50K revenue/year |

---

## 📊 Dataset

**Source:** [Kaggle — Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)

| Field | Description |
|-------|-------------|
| Order Date / Ship Date | Transaction and fulfilment dates |
| Category / Sub-Category | Product hierarchy |
| Sales / Profit | Revenue and net profit per line item |
| Discount | Discount applied (0.0 – 1.0) |
| Region / State | US geographic location |
| Segment | Customer type: Consumer, Corporate, Home Office |
| Ship Mode | Standard Class, Second Class, First Class, Same Day |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.9+** | Core language |
| **Pandas** | Data manipulation & cleaning |
| **NumPy** | Numerical operations |
| **Plotly** | Interactive charts (14 chart types) |
| **Streamlit** | Dashboard framework |
| **Scikit-learn** | Trendline calculation |

---

## 📦 Installation (Detailed)

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Step-by-step

```bash
# Create and activate a virtual environment (recommended)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# Verify data pipeline works
python src/data_loader.py

# Verify analysis layer works
python src/analysis.py

# Launch the dashboard
streamlit run dashboard/app.py
```

---

## 🌐 Deploying to Streamlit Cloud (Free Dashboard Link)

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → Select your repo
4. Set **Main file path:** `dashboard/app.py`
5. Click **Deploy**

Your dashboard will be live at `https://YOUR-APP-NAME.streamlit.app` — ready to share with clients!

---

## 📄 Reports

- **[Business Insights Report](reports/insights_report.md)** — Full analysis with findings and recommendations

---

## 🤝 Use Cases

This project is suitable for:
- 📋 **Internship portfolio projects**
- 💼 **Freelance data analytics proposals**
- 🏢 **Business intelligence presentations**
- 🎓 **Learning data analysis with Python**

---

## 📝 License

MIT License — free to use, modify, and share.

---

*Built with ❤️ using Python · Pandas · Plotly · Streamlit*
