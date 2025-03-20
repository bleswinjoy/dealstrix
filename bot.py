import os
import requests
from telegram import Bot
from dotenv import load_dotenv
import schedule
import time
import threading

load_dotenv()

TOKEN = os.getenv("7525660684:AAG2fNbxDteJl7Z6HXmv4sUo2IjDxU-hPuU")
CHANNEL_ID = os.getenv("@Dealstrix")
AFFILIATE_ID = os.getenv("AMAZON_AFFILIATE_ID")

# Example: Store the last product ID to avoid reposting
LAST_POSTED_PRODUCT = None

def fetch_latest_deals():
    global LAST_POSTED_PRODUCT

    # Replace this with your actual API/scraping logic to get NEW products
    # For testing, return dummy data
    dummy_products = [{
        "id": "123",
        "title": "Wireless Headphones",
        "price": "$49.99",
        "image_url": "https://example.com/image.jpg",
        "product_url": f"https://amazon.com/dp/XYZ?tag={AFFILIATE_ID}"
    }]

    new_products = []
    for product in dummy_products:
        if product["id"] != LAST_POSTED_PRODUCT:
            new_products.append(product)
            LAST_POSTED_PRODUCT = product["id"]  # Update last posted product

    return new_products

def post_to_channel():
    new_products = fetch_latest_deals()
    bot = Bot(token=TOKEN)
    for product in new_products:
        message = f"🔥 {product['title']}\nPrice: {product['price']}\n{product['product_url']}"
        bot.send_photo(chat_id=CHANNEL_ID, photo=product['image_url'], caption=message)

# Schedule to check for new deals every 1 hour (adjust as needed)
schedule.every(1).hours.do(post_to_channel)

# Run the scheduler in a background thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every 60 seconds

# Start the scheduler thread
threading.Thread(target=run_scheduler, daemon=True).start()

# Keep the script running forever
while True:
    time.sleep(1)
