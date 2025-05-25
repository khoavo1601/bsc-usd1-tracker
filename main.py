import requests
import time
import os

# 🔐 Lấy thông tin từ biến môi trường
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': False
    }
    requests.post(url, data=data)

def fetch_bsc_pairs():
    url = "https://api.dexscreener.com/latest/dex/pairs/bsc"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json().get('pairs', [])
    except Exception as e:
        print(f"Error fetching pairs: {e}")
    return []

known_pairs = set()

# Gửi thông báo test để biết bot đã chạy
send_telegram_message("✅ Bot theo dõi USD1 trên BSC đã khởi động!")

while True:
    pairs = fetch_bsc_pairs()
    for pair in pairs:
        pair_id = pair.get("pairAddress")
        base = pair.get("baseToken", {})
        quote = pair.get("quoteToken", {})
        quote_symbol = quote.get("symbol", "").lower()

        if pair_id and pair_id not in known_pairs:
            if quote_symbol == 'usd1':
                msg = (
                    f"🚀 *New Token Listed on BSC!*\n\n"
                    f"🪙 *Name:* {base.get('name')} ({base.get('symbol')})\n"
                    f"💵 *Pair:* {quote.get('symbol')}\n"
                    f"🔗 [View on Dexscreener]({pair.get('url')})"
                )
                send_telegram_message(msg)
                known_pairs.add(pair_id)

    time.sleep(60)
