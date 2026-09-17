import json
import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# 1. LOAD DEMO PRICE HISTORY
# ==========================================

with open(
    "demo_price_history.json",
    "r",
    encoding="utf-8"
) as file:

    history = json.load(file)


# ==========================================
# 2. CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(history)

df["date"] = pd.to_datetime(df["date"])


# ==========================================
# 3. CREATE CSV
# ==========================================

df.to_csv(
    "demo_price_history.csv",
    index=False
)

print("✅ CSV report created:")
print("demo_price_history.csv")


# ==========================================
# 4. GENERATE REPORT FOR EACH PRODUCT
# ==========================================

for product_name in df["product"].unique():

    product_data = df[
        df["product"] == product_name
    ].copy()

    product_data = product_data.sort_values(
        "date"
    )


    # ======================================
    # PRICE INFORMATION
    # ======================================

    current_price = product_data[
        "current_price"
    ].iloc[-1]

    highest_price = product_data[
        "current_price"
    ].max()

    lowest_price = product_data[
        "current_price"
    ].min()

    target_price = product_data[
        "target_price"
    ].iloc[-1]

    first_price = product_data[
        "current_price"
    ].iloc[0]


    # ======================================
    # PRICE CHANGE
    # ======================================

    price_change = (
        current_price - first_price
    )


    # ======================================
    # DISPLAY REPORT
    # ======================================

    print()
    print("=" * 60)

    print(
        "📱 Product:",
        product_name
    )

    print("=" * 60)

    print(
        f"💰 Current price : ₹{current_price:,.0f}"
    )

    print(
        f"🔺 Highest price : ₹{highest_price:,.0f}"
    )

    print(
        f"🔻 Lowest price  : ₹{lowest_price:,.0f}"
    )

    print(
        f"🎯 Target price  : ₹{target_price:,.0f}"
    )


    # ======================================
    # TARGET CHECK
    # ======================================

    if current_price <= target_price:

        saving = (
            target_price - current_price
        )

        print(
            "🎉 Target price has been reached!"
        )

        print(
            f"💚 Below target by: "
            f"₹{saving:,.0f}"
        )

    else:

        difference = (
            current_price - target_price
        )

        print(
            "❌ Target price not reached."
        )

        print(
            f"🔴 Above target by: "
            f"₹{difference:,.0f}"
        )


    # ======================================
    # PRICE TREND
    # ======================================

    if price_change < 0:

        print(
            f"📉 Price decreased by: "
            f"₹{abs(price_change):,.0f}"
        )

    elif price_change > 0:

        print(
            f"📈 Price increased by: "
            f"₹{price_change:,.0f}"
        )

    else:

        print(
            "➡️ Price has not changed."
        )


    # ======================================
    # CREATE GRAPH
    # ======================================

    plt.figure(
        figsize=(10, 5)
    )


    # Current price

    plt.plot(
        product_data["date"],
        product_data["current_price"],
        marker="o",
        label="Current Price"
    )


    # Target price

    plt.plot(
        product_data["date"],
        product_data["target_price"],
        marker="o",
        linestyle="--",
        label="Target Price"
    )


    plt.title(
        f"Price History - {product_name}"
    )

    plt.xlabel(
        "Date"
    )

    plt.ylabel(
        "Price (₹)"
    )

    plt.legend()

    plt.grid(True)

    plt.gcf().autofmt_xdate()

    plt.tight_layout()


    # ======================================
    # SAVE GRAPH
    # ======================================

    safe_name = (
        product_name
        .replace(" ", "_")
        .replace("/", "_")
        .replace("&", "and")
        .replace(",", "")
    )


    filename = (
        f"{safe_name}_price_graph.png"
    )


    plt.savefig(
        filename,
        dpi=150
    )


    print(
        f"📊 Graph created: {filename}"
    )


    # Close graph

    plt.close()


# ==========================================
# FINISHED
# ==========================================

print()
print("=" * 60)

print(
    "✅ PRICE REPORT COMPLETED!"
)

print(
    "📊 Reports generated for all products."
)

print("=" * 60)