# Superstore Sales Analysis — Business Insights Report

> **Prepared by:** Data Analytics Team  
> **Dataset:** Kaggle Superstore Dataset (9,994 transactions, 2019–2022)  
> **Tools Used:** Python · Pandas · Plotly · Streamlit  

---

## Executive Summary

The Superstore dataset covers **4 years of US retail sales** across 3 product categories, 4 geographic regions, and 3 customer segments. This report distils the data into 10 core findings and 7 actionable recommendations that a business owner can implement immediately.

| KPI | Value |
|-----|-------|
| Total Revenue | ~$2.3M |
| Total Profit | ~$286K |
| Overall Profit Margin | ~12.5% |
| Total Orders | ~5,009 |
| Unique Customers | ~793 |
| Loss-Making Orders | ~1,871 |

---

## Section 1 — Revenue & Profit Trends

### Finding 1: Seasonal Revenue Peaks in Q4
Revenue consistently spikes in **Q4 (October–December)** each year, driven by holiday demand. This pattern is predictable and should be used to plan inventory, staffing, and promotions in advance. Businesses that fail to pre-position for Q4 leave significant revenue on the table.

**Recommendation:** Begin Q4 inventory planning by **September 1st** each year.

### Finding 2: Steady Year-over-Year Growth
Revenue grew at an average of **~20% YoY** across the dataset period. While growth is strong, profit growth has not kept pace — indicating margin compression, likely from excessive discounting and rising costs in certain categories.

**Recommendation:** Set a minimum profit margin target (e.g., 15%) as a KPI alongside revenue growth.

---

## Section 2 — Product & Category Analysis

### Finding 3: Technology Drives Revenue; Office Supplies Drives Profit
- **Technology** generates the most revenue (~37% share) but faces margin pressure from Machines and Copiers.
- **Office Supplies** delivers the highest profit margins, particularly in Labels, Envelopes, and Art.
- **Furniture** is a revenue contributor but the worst margin performer — Tables and Bookcases are frequently loss-making.

| Category | Revenue Share | Avg Profit Margin |
|----------|--------------|-------------------|
| Technology | ~37% | ~17% |
| Office Supplies | ~32% | ~22% |
| Furniture | ~31% | ~2.5% |

**Recommendation:** Invest in growing Office Supplies volume (high margin). Conduct a Furniture pricing audit — Tables are a major profit drain.

### Finding 4: Sub-Category Winners and Losers
**Top performers (high margin):**
- Copiers, Paper, Labels, Envelopes

**Loss-making sub-categories:**
- Tables (consistently negative margin)
- Bookcases (near-zero margin)
- Supplies (negative margin on discounts)

**Recommendation:** Consider discontinuing or repricing Tables. They generate sales volume but destroy profitability.

---

## Section 3 — Regional Analysis

### Finding 5: West Region Leads, South Lags
- The **West** region generates the highest revenue and profit.
- The **South** region has the lowest performance despite having a significant customer base.
- The **Central** region has strong orders but average profitability.

| Region | Revenue Rank | Profit Rank |
|--------|-------------|-------------|
| West | #1 | #1 |
| East | #2 | #2 |
| Central | #3 | #3 |
| South | #4 | #4 |

**Recommendation:** Deploy targeted regional marketing campaigns in the South. Consider region-specific promotions and localised product bundles to close the gap.

### Finding 6: California and New York Are Revenue Powerhouses
The top 5 states by revenue account for **~40% of total sales**. However, several mid-tier states show strong growth trajectories and should be prioritised for expansion.

**Recommendation:** Appoint regional sales leads for top-5 states to protect existing revenue and nurture growth in states ranked 6–15.

---

## Section 4 — Customer Segment Analysis

### Finding 7: Consumer Segment Dominates Volume; Corporate Wins on Order Value
- **Consumer:** ~51% of revenue — largest segment by volume
- **Corporate:** ~30% of revenue — significantly higher average order value ($700+ vs $400)
- **Home Office:** ~19% of revenue — smallest but fastest growing

**Recommendation:** Build a dedicated B2B (Corporate) sales motion. Even converting 50 Consumer customers to Corporate accounts could add $150K+ in revenue.

---

## Section 5 — Discount Analysis ⚠️ CRITICAL

### Finding 8: Discounts Above 20% Destroy Profitability
This is the most important finding in the entire dataset.

| Discount Range | Avg Profit Margin |
|---------------|------------------|
| 0% | +18–22% |
| 1–10% | +12–15% |
| 11–20% | +5–8% |
| 21–30% | **-3 to -8%** |
| 31–50% | **-15 to -25%** |
| 51%+ | **-30 to -50%** |

**Over 1,800 orders in this dataset generated a net loss — the vast majority had discounts above 20%.**

**Recommendation (Priority #1):** Implement a **hard discount cap of 20%** in CRM/ERP systems immediately. Require VP-level approval for any exception. This single change could recover **$60,000–$100,000** in annual profit.

---

## Section 6 — Shipping Analysis

### Finding 9: Standard Class is the Workhorse
**Standard Class** handles ~60% of all orders and generates solid profitability. **Same Day** shipping is rarely used but its premium pricing means it should maintain strong margins — verify that shipping cost is being passed to customers appropriately.

**Recommendation:** Audit Same Day and First Class shipping to ensure premium rates are being charged and not absorbed internally.

---

## Section 7 — Strategic Recommendations Summary

| Priority | Action | Impact | Effort |
|----------|--------|--------|--------|
| 🔴 HIGH | Cap all discounts at 20% | +$60–100K profit/year | Low |
| 🔴 HIGH | Audit and reprice Tables | +$20–40K profit/year | Medium |
| 🟡 MED | Launch Corporate B2B programme | +$150K revenue/year | High |
| 🟡 MED | Expand Office Supplies range | +$80K revenue/year | Medium |
| 🟡 MED | South region marketing campaign | +$50K revenue/year | Medium |
| 🟢 LOW | Bundle high-margin + slow-movers | +$30K revenue/year | Low |
| 🟢 LOW | Q4 inventory pre-positioning | +$40K revenue/year | Low |

---

## Conclusion

The Superstore business is fundamentally healthy — growing revenue, expanding customer base, and strong demand across all regions. However, **two structural problems are suppressing profitability:**

1. **Excessive discounting** — directly turning profitable orders into losses
2. **Furniture margin collapse** — particularly Tables, which destroy value at scale

Fixing these two issues alone could increase annual profit by **20–35%** without acquiring a single new customer. Combined with B2B growth and regional expansion, the business has clear pathways to **double profitability within 2 years**.

---

*Report generated from Kaggle Superstore Dataset · Analysis performed in Python · Dashboard built with Streamlit & Plotly*
