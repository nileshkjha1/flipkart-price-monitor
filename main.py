import os
import json
import time
import smtplib
import requests

from email.message import EmailMessage


# ==========================================
# SETTINGS
# ==========================================

# Load monitoring interval from config.json
try:
    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)

    check_interval_minutes = float(
        config.get("check_interval_minutes", 10080)
    )

    if check_interval_minutes <= 0:
        raise ValueError("Check interval must be greater than 0.")

    CHECK_INTERVAL = int(check_interval_minutes * 60)

except FileNotFoundError:
    print("❌ config.json not found.")
    exit()

except (json.JSONDecodeError, ValueError, TypeError) as error:
    print("❌ Invalid config.json:")
    print(error)
    exit()

SENDER_EMAIL = "nileshkjha2000@gmail.com"


# ==========================================
# LOAD PRODUCTS
# ==========================================

try:

    with open(
        "products.json",
        "r",
        encoding="utf-8"
    ) as file:

        products = json.load(file)

except FileNotFoundError:

    print("❌ products.json not found.")

    exit()

except json.JSONDecodeError:

    print("❌ products.json contains invalid JSON.")

    exit()


# ==========================================
# API KEY
# ==========================================

reef_key = os.environ.get("REEF_KEY")

if not reef_key:

    print("❌ REEF_KEY not found.")

    exit()


# ==========================================
# EMAIL PASSWORD
# ==========================================

email_password = os.environ.get(
    "PRICE_MONITOR_EMAIL_PASSWORD"
)

if not email_password:

    print(
        "❌ Gmail App Password not found."
    )

    exit()

email_password = email_password.replace(
    " ",
    ""
)


# ==========================================
# ALERT STATUS
# ==========================================

alert_sent = {}

for product in products:

    alert_sent[product["name"]] = False


# ==========================================
# GET FLIPKART PRICE
# ==========================================

def get_flipkart_price(product_url):

    api_url = (
        "https://api.reefapi.com/"
        "flipkart/v1/product"
    )

    try:

        response = requests.post(

            api_url,

            headers={
                "x-api-key": reef_key,
                "content-type": "application/json"
            },

            json={
                "url": product_url
            },

            # Don't wait forever
            timeout=30
        )


    except requests.exceptions.Timeout:

        print(
            "⚠️ API request timed out."
        )

        return None, None, None


    except requests.exceptions.ConnectionError:

        print(
            "⚠️ Internet connection error."
        )

        return None, None, None


    except requests.exceptions.RequestException as error:

        print(
            "⚠️ API request error:"
        )

        print(error)

        return None, None, None


    # ======================================
    # CHECK STATUS CODE
    # ======================================

    if response.status_code != 200:

        print(
            "⚠️ API returned status:",
            response.status_code
        )

        return None, None, None


    # ======================================
    # READ JSON
    # ======================================

    try:

        data = response.json()

    except ValueError:

        print(
            "⚠️ API returned invalid JSON."
        )

        return None, None, None


    # ======================================
    # CHECK API SUCCESS
    # ======================================

    if not data.get("ok"):

        print(
            "⚠️ ReefAPI returned an error."
        )

        error_info = data.get(
            "error",
            "Unknown API error"
        )

        print(
            error_info
        )

        return None, None, None


    # ======================================
    # GET PRODUCT DATA
    # ======================================

    product_data = data.get(
        "data",
        {}
    )


    if "product" in product_data:

        product_data = (
            product_data["product"]
        )


    name = product_data.get(
        "title"
    )

    price = product_data.get(
        "price"
    )

    mrp = product_data.get(
        "mrp"
    )


    # ======================================
    # CHECK PRICE
    # ======================================

    if price is None:

        print(
            "⚠️ Product price not found."
        )

        return None, None, None


    return name, price, mrp


# ==========================================
# SEND EMAIL
# ==========================================

def send_email(
    product_name,
    current_price,
    target_price,
    mrp,
    receiver_email
):

    try:

        message = EmailMessage()


        message["Subject"] = (
            "🎉 Flipkart Price Alert!"
        )


        message["From"] = SENDER_EMAIL


        message["To"] = receiver_email


        message.set_content(
            f"""
Good news!

Your Flipkart product has reached
your target price.

Product:
{product_name}

Current price:
₹{current_price:,.0f}

Target price:
₹{target_price:,.0f}

MRP:
₹{mrp:,.0f}

Price Monitor 🚀
"""
        )


        print(
            "Connecting to Gmail..."
        )


        with smtplib.SMTP(
            "smtp.gmail.com",
            587,
            timeout=30
        ) as server:

            server.starttls()

            server.login(
                SENDER_EMAIL,
                email_password
            )

            server.send_message(
                message
            )


        print(
            "✅ Price alert email sent!"
        )

        return True


    except smtplib.SMTPException as error:

        print(
            "⚠️ Gmail error:"
        )

        print(error)

        return False


    except Exception as error:

        print(
            "⚠️ Email error:"
        )

        print(error)

        return False


# ==========================================
# CHECK ALL PRODUCTS
# ==========================================

def check_products():

    for product in products:

        try:

            product_name = product["name"]

            product_url = product["url"]

            target_price = float(
                product["target_price"]
            )

            receiver_email = product.get(
                "email",
                SENDER_EMAIL
            )


        except (KeyError, ValueError, TypeError):

            print(
                "⚠️ Invalid product configuration."
            )

            continue


        print()

        print(
            "=" * 50
        )

        print(
            f"🔎 Checking: {product_name}"
        )


        # ==================================
        # GET PRICE
        # ==================================

        name, current_price, mrp = (
            get_flipkart_price(
                product_url
            )
        )


        # ==================================
        # API FAILED
        # ==================================

        if current_price is None:

            print(
                f"⚠️ Skipping {product_name}."
            )

            print(
                "🔄 It will be checked again "
                "next week."
            )

            continue


        # ==================================
        # DISPLAY
        # ==================================

        print(
            "Product:",
            name
        )

        print(
            f"Current price: "
            f"₹{current_price:,.0f}"
        )

        print(
            f"Target price: "
            f"₹{target_price:,.0f}"
        )


        if mrp:

            print(
                f"MRP: "
                f"₹{mrp:,.0f}"
            )


        # ==================================
        # TARGET REACHED
        # ==================================

        if current_price <= target_price:

            print(
                "🎉 TARGET PRICE REACHED!"
            )


            if not alert_sent[product_name]:

                email_sent = send_email(

                    name,

                    current_price,

                    target_price,

                    mrp,

                    receiver_email
                )


                if email_sent:

                    alert_sent[
                        product_name
                    ] = True

                else:

                    print(
                        "⚠️ Email was not sent."
                    )


            else:

                print(
                    "📧 Alert already sent."
                )


        # ==================================
        # TARGET NOT REACHED
        # ==================================

        else:

            difference = (
                current_price -
                target_price
            )


            print(
                "❌ Target price not reached."
            )


            print(
                f"₹{difference:,.0f} "
                f"above target."
            )


            # Reset alert

            alert_sent[
                product_name
            ] = False


# ==========================================
# START MONITOR
# ==========================================

print()

print(
    "🚀 Flipkart Price Monitor Started!"
)

print(
    f"📦 Products being monitored: "
    f"{len(products)}"
)

print(
    f"⏱️ Check interval: "
    f"{check_interval_minutes:g} minutes"
)


print()


# ==========================================
# CONTINUOUS MONITORING
# ==========================================

while True:

    try:

        check_products()

    except Exception as error:

        print()

        print(
            "⚠️ Unexpected error:"
        )

        print(error)

        print(
            "🔄 Monitor will continue."
        )


    print()

    print(
    f"⏳ Waiting {check_interval_minutes:g} "
    f"minutes for the next check..."
    )
    


    time.sleep(
        CHECK_INTERVAL
    )