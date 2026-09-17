import os
import requests


def get_flipkart_price(product_url):

    # Get API key
    api_key = os.environ.get("REEF_KEY")

    if not api_key:
        print("❌ REEF_KEY not found.")
        return None

    # ReefAPI endpoint
    api_url = "https://api.reefapi.com/flipkart/v1/product"

    # Send request
    response = requests.post(
        api_url,
        headers={
            "x-api-key": api_key,
            "content-type": "application/json"
        },
        json={
            "url": product_url
        }
    )

    print("Status code:", response.status_code)

    # Check HTTP response
    if response.status_code != 200:
        print("❌ API request failed.")
        print(response.text)
        return None

    # Convert response to JSON
    data = response.json()

    # DEBUG: show the response
    print("\nAPI response:")
    print(data)

    # Check API success
    if not data.get("ok"):
        print("❌ API returned an error.")
        return None

    # Product data
    product = data.get("data", {})

    # Try different possible locations
    if "product" in product:
        product = product["product"]

    product_name = product.get("title")
    current_price = product.get("price")
    mrp = product.get("mrp")

    print()
    print("Product:", product_name)
    print("Current price: ₹", current_price)
    print("MRP: ₹", mrp)

    return current_price


# --------------------------------
# Flipkart product
# --------------------------------

product_url = "https://www.flipkart.com/samsung-galaxy-s26-ultra-5g-cobalt-violet-256-gb/p/itmf4799d3841c43"

get_flipkart_price(product_url)