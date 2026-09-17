import json
from datetime import datetime, timedelta


# ==========================================
# DEMO PRICE HISTORY
# ==========================================

demo_history = [
    {
        "date": "2026-08-20 10:00:00",
        "product": "Samsung Galaxy S26 Ultra",
        "current_price": 135999,
        "target_price": 131000,
        "mrp": 139999
    },
    {
        "date": "2026-08-27 10:00:00",
        "product": "Samsung Galaxy S26 Ultra",
        "current_price": 133999,
        "target_price": 131000,
        "mrp": 139999
    },
    {
        "date": "2026-09-03 10:00:00",
        "product": "Samsung Galaxy S26 Ultra",
        "current_price": 132499,
        "target_price": 131000,
        "mrp": 139999
    },
    {
        "date": "2026-09-10 10:00:00",
        "product": "Samsung Galaxy S26 Ultra",
        "current_price": 131999,
        "target_price": 131000,
        "mrp": 139999
    },
    {
        "date": "2026-09-16 10:00:00",
        "product": "Samsung Galaxy S26 Ultra",
        "current_price": 130999,
        "target_price": 131000,
        "mrp": 139999
    },

    {
        "date": "2026-08-20 10:00:00",
        "product": "Apple iPhone 17 Pro 256GB Cosmic Orange",
        "current_price": 139900,
        "target_price": 134000,
        "mrp": 149900
    },
    {
        "date": "2026-08-27 10:00:00",
        "product": "Apple iPhone 17 Pro 256GB Cosmic Orange",
        "current_price": 138500,
        "target_price": 134000,
        "mrp": 149900
    },
    {
        "date": "2026-09-03 10:00:00",
        "product": "Apple iPhone 17 Pro 256GB Cosmic Orange",
        "current_price": 136999,
        "target_price": 134000,
        "mrp": 149900
    },
    {
        "date": "2026-09-10 10:00:00",
        "product": "Apple iPhone 17 Pro 256GB Cosmic Orange",
        "current_price": 135499,
        "target_price": 134000,
        "mrp": 149900
    },
    {
        "date": "2026-09-16 10:00:00",
        "product": "Apple iPhone 17 Pro 256GB Cosmic Orange",
        "current_price": 134900,
        "target_price": 134000,
        "mrp": 149900
    }
]


# ==========================================
# SAVE DEMO DATA
# ==========================================

with open(
    "demo_price_history.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        demo_history,
        file,
        indent=4,
        ensure_ascii=False
    )


print("✅ Demo price history created!")

print(
    "📁 File: demo_price_history.json"
)

print(
    "📊 5 weeks of sample data created "
    "for 2 products."
)