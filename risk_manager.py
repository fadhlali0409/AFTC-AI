class RiskManager:
    def calculate_risk(self, df_ltf, pda_zone, bias):
        # إدارة المخاطر، حساب وقف الخسارة الحقيقي (SL) وأهداف الربح (TP) بناءً على بنية الشموع
        if df_ltf.empty:
            return None
        current_close = float(df_ltf['Close'].iloc[-1])
        atr_proxy = float(df_ltf['High'].iloc[-1] - df_ltf['Low'].iloc[-1])
        
        if bias == "BULLISH":
            sl = current_close - (atr_proxy * 1.5)
            tp = current_close + (atr_proxy * 3.0)
        else:
            sl = current_close + (atr_proxy * 1.5)
            tp = current_close - (atr_proxy * 3.0)
            
        return {
            "entry": current_close,
            "sl": round(sl, 4),
            "tp": round(tp, 4)
        }
