# Retail Sales Analytics Dashboard

## Overview
An end-to-end sales analytics project covering data cleaning, SQL analysis, and
Power-BI-style KPI reporting on a retail sales dataset. The dataset is
**synthetically generated** to reflect realistic retail patterns (category mix,
discount structures, regional/segment split, seasonal ordering) — not scraped
or copied from any public dataset.

## Objective
Identify what actually drives (and erodes) profitability across categories,
discount levels, regions, and customer segments.

## Tech Stack
- **Python / Pandas** — data generation, cleaning, EDA
- **SQL (sqlite3)** — JOINs, GROUP BY/HAVING, CTEs, Window Functions (running totals, RANK)
- **Matplotlib** — visualization (stand-ins for Power BI KPI cards/charts)

## Key Findings
1. **Category profitability is wildly uneven**: Technology drives 16.3% margin,
   Office Supplies 10.0%, but Furniture nets only 0.3% margin despite being the
   second-largest category by sales ($20.8M) — it's carrying real revenue
   without real profit.
2. **Discounting past ~30% actively loses money**: orders with 0% discount run
   a 22.7% margin; orders discounted 31%+ run a **-17.0% margin** — a clear
   signal that the current discount policy needs a ceiling.
3. **Tables and Bookcases are effectively break-even or loss-making**
   sub-categories (Tables: -$432 total profit across the whole synthetic
   dataset), while Copiers, Machines, Accessories, and Phones each contribute
   $1.7M+ in profit.
4. **West region + Consumer segment is the single most profitable combination**
   ($960K profit), while Central region + Home Office segment is the weakest
   ($219K).
5. Monthly sales are relatively stable (~$2.7M-$3.3M/month) with no extreme
   seasonal spike in this simulation — a useful baseline finding in itself
   (not every retail story has a dramatic holiday spike).

## Files
- `sql_analysis.py` — SQL analysis (JOINs, CTEs, Window Functions)
- `eda_visualize.py` — Python EDA and chart generation
- `data/retail_sales_synthetic.csv` — the dataset (52,000 records)
- `charts/` — visualizations
- `sql_findings.txt` — raw SQL query outputs

## Note on data
This project uses a synthetic dataset built to reflect realistic retail sales
dynamics. All analysis, code, and findings are the author's own work.
