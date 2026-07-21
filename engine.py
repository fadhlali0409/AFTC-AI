import logging
import yfinance as yf
import pandas as pd

from market_structure import MarketStructure
from key_levels import KeyLevels
from liquidity import LiquidityAnalyzer
from pda import PDAAnalyzer
from confirmation import ConfirmationAnalyzer
from risk_manager import RiskManager
from quality_score import QualityScoreCalculator

logger = logging.getLogger(__name__)

class Engine:
    def __init__(self):
        self.ms = MarketStructure()
        self.kl = KeyLevels()
        self.liq = LiquidityAnalyzer()
        self.pda = PDAAnalyzer()
        self.conf = ConfirmationAnalyzer()
        self.rm = RiskManager()
        self.qs = QualityScoreCalculator()

    def fetch_data(self, symbol, interval, period="5d"):
        for attempt in range(3):
            try:
                df = yf.download(symbol, period=period, interval=interval, progress=False)
                if not df.empty:
                    if isinstance(df.columns, pd.MultiIndex):
                        df.columns = df.columns.get_level_values(0)
                    return df
            except Exception as e:
                logger.warning(f"Data fetch attempt {attempt+1} failed for {symbol} ({interval}): {e}")
                import time; time.sleep(2)
        return pd.DataFrame()

    def process_symbol(self, symbol, htf="4h", ltf="15m"):
        # 1. جلب بيانات الإطار الزمني العالي HTF والإطار المنخفض LTF
        df_htf = self.fetch_data(symbol, htf, period="1mo")
        df_ltf = self.fetch_data(symbol, ltf, period="5d")

        if df_htf.empty or df_ltf.empty:
            return None

        # 2. تسلسل الاستراتيجية الحقيقي (Pipeline)
        
        # أ. HTF Bias
        bias = self.ms.get_htf_bias(df_htf)
        if not bias:
            return None

        # ب. Key Level
        key_level = self.kl.find_key_level(df_htf, bias)
        if not key_level:
            return None

        # ج. Liquidity Sweep
        sweep_detected = self.liq.detect_sweep(df_ltf, key_level)
        if not sweep_detected:
            return None

        # د. PDA & Return to Value
        pda_zone = self.pda.find_valid_pda(df_ltf, bias)
        if not pda_zone:
            return None

        # هـ. MSS أو CISD Confirmation
        confirmed, conf_type = self.conf.verify_confirmation(df_ltf, bias)
        if not confirmed:
            return None

        # و. Risk Manager (حساب الدخول، وقف الخسارة، والأهداف)
        risk_params = self.rm.calculate_risk(df_ltf, pda_zone, bias)
        if not risk_params:
            return None

        # ز. Quality Score (تقييم جودة الصفقة)
        score = self.qs.evaluate(bias, key_level, sweep_detected, pda_zone, conf_type)
        if score < 70: # حد أدنى للجودة لضمان قوة الإشارة
            return None

        return {
            "status": "READY",
            "symbol": symbol,
            "direction": bias,
            "htf_bias": bias,
            "key_level": key_level,
            "entry": risk_params["entry"],
            "sl": risk_params["sl"],
            "tp": risk_params["tp"],
            "score": score
        }
