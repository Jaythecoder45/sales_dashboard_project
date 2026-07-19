"""
Real SQL analysis on the synthetic retail sales dataset using sqlite3.
JOINs, GROUP BY/HAVING, CTEs, Window Functions -- run against actual data.
"""
import sqlite3
import pandas as pd

df = pd.read_csv("data/retail_sales_synthetic.csv", parse_dates=["order_date"])

conn = sqlite3.connect(":memory:")

# split into two tables to justify a real JOIN
orders = df[["order_id", "customer_id", "order_date", "month", "region", "segment",
             "ship_mode", "category", "sub_category", "quantity", "discount"]]
sales_fact = df[["order_id", "sales", "profit"]]

orders.to_sql("orders", conn, index=False, if_exists="replace")
sales_fact.to_sql("sales_fact", conn, index=False, if_exists="replace")

print("=" * 70)
print("QUERY 1: Total Sales & Profit by Category (JOIN + GROUP BY + HAVING)")
print("=" * 70)
q1 = """
SELECT
    o.category,
    ROUND(SUM(sf.sales), 0) AS total_sales,
    ROUND(SUM(sf.profit), 0) AS total_profit,
    ROUND(100.0 * SUM(sf.profit) / SUM(sf.sales), 1) AS profit_margin_pct
FROM orders o
JOIN sales_fact sf ON sf.order_id = o.order_id
GROUP BY o.category
HAVING SUM(sf.sales) > 0
ORDER BY total_profit DESC
"""
r1 = pd.read_sql(q1, conn)
print(r1.to_string(index=False))

print("\n" + "=" * 70)
print("QUERY 2: Discount band vs. profit margin")
print("=" * 70)
q2 = """
WITH banded AS (
    SELECT
        sf.order_id,
        sf.sales,
        sf.profit,
        CASE
            WHEN o.discount = 0 THEN '0% (no discount)'
            WHEN o.discount <= 0.15 THEN '1-15%'
            WHEN o.discount <= 0.30 THEN '16-30%'
            ELSE '31%+'
        END AS discount_band
    FROM orders o JOIN sales_fact sf ON sf.order_id = o.order_id
)
SELECT
    discount_band,
    COUNT(*) AS orders,
    ROUND(100.0 * SUM(profit) / SUM(sales), 1) AS profit_margin_pct
FROM banded
GROUP BY discount_band
ORDER BY profit_margin_pct DESC
"""
r2 = pd.read_sql(q2, conn)
print(r2.to_string(index=False))

print("\n" + "=" * 70)
print("QUERY 3: Monthly sales trend (Window Function - running total)")
print("=" * 70)
q3 = """
WITH monthly AS (
    SELECT o.month, SUM(sf.sales) AS monthly_sales
    FROM orders o JOIN sales_fact sf ON sf.order_id = o.order_id
    GROUP BY o.month
)
SELECT
    month,
    ROUND(monthly_sales, 0) AS monthly_sales,
    ROUND(SUM(monthly_sales) OVER (ORDER BY month), 0) AS running_total_sales
FROM monthly
ORDER BY month
"""
r3 = pd.read_sql(q3, conn)
print(r3.to_string(index=False))

print("\n" + "=" * 70)
print("QUERY 4: Region x Segment ranking by profit (Window Function - RANK)")
print("=" * 70)
q4 = """
WITH region_seg AS (
    SELECT o.region, o.segment, SUM(sf.profit) AS total_profit
    FROM orders o JOIN sales_fact sf ON sf.order_id = o.order_id
    GROUP BY o.region, o.segment
)
SELECT *, RANK() OVER (ORDER BY total_profit DESC) AS profit_rank
FROM region_seg
"""
r4 = pd.read_sql(q4, conn)
print(r4.to_string(index=False))

print("\n" + "=" * 70)
print("QUERY 5: Sub-category performance (top and bottom by profit)")
print("=" * 70)
q5 = """
SELECT
    o.sub_category,
    ROUND(SUM(sf.sales),0) AS total_sales,
    ROUND(SUM(sf.profit),0) AS total_profit
FROM orders o JOIN sales_fact sf ON sf.order_id = o.order_id
GROUP BY o.sub_category
ORDER BY total_profit DESC
"""
r5 = pd.read_sql(q5, conn)
print(r5.to_string(index=False))

with open("sql_findings.txt", "w") as f:
    f.write("CATEGORY:\n" + r1.to_string(index=False) + "\n\n")
    f.write("DISCOUNT BAND:\n" + r2.to_string(index=False) + "\n\n")
    f.write("MONTHLY TREND:\n" + r3.to_string(index=False) + "\n\n")
    f.write("REGION x SEGMENT RANKING:\n" + r4.to_string(index=False) + "\n\n")
    f.write("SUB-CATEGORY:\n" + r5.to_string(index=False) + "\n")

conn.close()
