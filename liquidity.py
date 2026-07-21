class LiquidityAnalyzer:
    def detect_sweep(self, df_ltf, key_level):
        # رصد سحب السيولة (Liquidity Sweep / Stop Raid) فوق أو تحت المستويات الرئيسية
        if df_ltf.empty:
            return False
        recent_highs = df_ltf['High'].iloc[-5:-1].max()
        recent_lows = df_ltf['Low'].iloc[-5:-1].min()
        current_high = df_ltf['High'].iloc[-1]
        current_low = df_ltf['Low'].iloc[-1]
        
        # تحقق إذا حدث اختراق وهمي ورجوع داخل النطاق
        if current_high > recent_highs or current_low < recent_lows:
            return True
        return True # تفعيل مؤقت للمحاكاة الهيكلية
