import time
import logging
import requests
from config import TELEGRAM_TOKEN, CHAT_ID, SYMBOLS, DEFAULT_HTF, DEFAULT_LTF
from engine import Engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TelegramNotifier:
    @staticmethod
    def send_message(message):
        if not TELEGRAM_TOKEN or not CHAT_ID:
            logger.error("Telegram credentials missing in config.")
            return
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        for attempt in range(3):
            try:
                response = requests.post(url, json=payload, timeout=10)
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                logger.warning(f"Telegram send attempt {attempt+1} failed: {e}")
                time.sleep(2)
        logger.error("Failed to send Telegram notification after retries.")

def run_bot():
    logger.info("AFTC AI Bot initializing...")
    TelegramNotifier.send_message("🦅 *AFTC AI Bot* يعمل الآن بكفاءة 24/7 ويراقب الأسواق باللغة العربية.")
    
    engine = Engine()

    while True:
        try:
            for symbol in SYMBOLS:
                logger.info(f"Processing symbol: {symbol}")
                
                # عزل كل رمز على حدة لضمان عدم توقف البوت لو فشل رمز واحد
                try:
                    signal = engine.process_symbol(symbol, DEFAULT_HTF, DEFAULT_LTF)
                    if signal and signal.get("status") == "READY":
                        message = format_signal_message(signal)
                        TelegramNotifier.send_message(message)
                except Exception as symbol_err:
                    logger.error(f"Error processing symbol {symbol}: {symbol_err}")
                
                time.sleep(3) # فترة راحة بين الرموز لحماية الـ API و الـ Rate Limits
                
        except Exception as e:
            logger.error(f"Watchdog caught a critical error in main loop: {e}")
            TelegramNotifier.send_message(f"⚠️ *تنبيه نظام الحماية*: حدث خطأ في الحلقة الرئيسية: {e}")
            time.sleep(15)
        
        time.sleep(300) # دورة الفحص الكاملة للسوق

def format_signal_message(signal):
    direction_ar = "شراء (صاعد)" if signal['direction'] == "BULLISH" else "بيع (هابط)"
    bias_ar = "صاعد" if signal['htf_bias'] == "BULLISH" else "هابط"
    
    return (
        f"🚨 *تنبيه - تم رصد فرصة استراتيجية CRT* 🚨\n\n"
        f"• *الزوج / الأداة*: `{signal['symbol']}`\n"
        f"• *الجهة*: `{direction_ar}`\n"
        f"• *الاتجاه العام (HTF Bias)*: `{bias_ar}`\n"
        f"• *المستوى الرئيسي*: `{signal['key_level']}`\n"
        f"• *تقييم الجودة*: `{signal['score']}/100`\n"
        f"• *سعر الدخول*: `{signal['entry']}`\n"
        f"• *وقف الخسارة*: `{signal['sl']}`\n"
        f"• *هدف الربح*: `{signal['tp']}`\n"
    )

if __name__ == "__main__":
    run_bot()
