import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/retail_sales_synthetic.csv", parse_dates=["order_date"])

# 1. Profit margin by category
cat = df.groupby("category")[["sales", "profit"]].sum()
cat["margin_pct"] = 100 * cat["profit"] / cat["sales"]
cat = cat.sort_values("margin_pct", ascending=False)

fig, ax = plt.subplots(figsize=(6.5, 4.2))
bars = ax.bar(cat.index, cat["margin_pct"], color=["#27ae60", "#2874a6", "#c0392b"])
ax.set_ylabel("Profit Margin (%)")
ax.set_title("Profit Margin by Category")
for b in bars:
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.3, f"{b.get_height():.1f}%", ha="center", fontsize=9)
plt.tight_layout()
plt.savefig("charts/margin_by_category.png", dpi=130)
plt.close()

# 2. Discount band vs margin
df["discount_band"] = pd.cut(df["discount"], [-0.01, 0, 0.15, 0.30, 1.0],
                              labels=["0%", "1-15%", "16-30%", "31%+"])
band = df.groupby("discount_band", observed=True)[["sales", "profit"]].sum()
band["margin_pct"] = 100 * band["profit"] / band["sales"]

fig, ax = plt.subplots(figsize=(6.5, 4.2))
colors = ["#27ae60" if v >= 0 else "#c0392b" for v in band["margin_pct"]]
bars = ax.bar(band.index.astype(str), band["margin_pct"], color=colors)
ax.axhline(0, color="black", linewidth=0.8)
ax.set_ylabel("Profit Margin (%)")
ax.set_title("Profit Margin by Discount Band")
for b in bars:
    y = b.get_height()
    ax.text(b.get_x()+b.get_width()/2, y + (0.5 if y>=0 else -1.5), f"{y:.1f}%", ha="center", fontsize=9)
plt.tight_layout()
plt.savefig("charts/margin_by_discount.png", dpi=130)
plt.close()

# 3. Monthly sales trend
monthly = df.groupby("month")["sales"].sum()
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(monthly.index, monthly.values, marker="o", markersize=3, color="#2874a6")
ax.set_ylabel("Monthly Sales ($)")
ax.set_title("Monthly Sales Trend (2024-2025)")
plt.xticks(rotation=75, fontsize=7)
plt.tight_layout()
plt.savefig("charts/monthly_sales_trend.png", dpi=130)
plt.close()

# 4. Sub-category profit (worst performers highlighted)
sub = df.groupby("sub_category")["profit"].sum().sort_values()
fig, ax = plt.subplots(figsize=(7, 5))
colors = ["#c0392b" if v < 0 else "#7f8c8d" if v < 50000 else "#27ae60" for v in sub.values]
ax.barh(sub.index, sub.values, color=colors)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_xlabel("Total Profit ($)")
ax.set_title("Profit by Sub-Category (Lowest to Highest)")
plt.tight_layout()
plt.savefig("charts/profit_by_subcategory.png", dpi=130)
plt.close()

print("Charts saved.")
print(cat)
print(band)
