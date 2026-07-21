import time
import os
import requests
import yfinance as yf
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from config import TELEGRAM_TOKEN, CHAT_ID, SYMBOLS

# سيرفر وهمي بسيط جداً لإبقاء خدمة Render نشطة (Web Service Keep-Alive)
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"AFTC AI Bot is running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Error sending telegram message: {e}")

def check_market():
    send_telegram_message("🤖 *AFTC AI Bot* is online and monitoring the markets...")
    while True:
        try:
            for symbol in SYMBOLS:
                data = yf.download(symbol, period="5d", interval="1h", progress=False)
                if not data.empty:
                    current_price = float(data['Close'].iloc[-1])
                    print(f"Checked {symbol}: {current_price}")
                time.sleep(2)
        except Exception as e:
            print(f"Error in market loop: {e}")
        
        time.sleep(300)

if __name__ == "__main__":
    # تشغيل السيرفر الوهمي في خلفية منفصلة لضمان رضا منصة Render
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # تشغيل بوت السوق الأساسي
    check_market()
