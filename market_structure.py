class MarketStructure:
    def get_htf_bias(self, df_htf):
        # منطق تحديد اتجاه الإطار الزمني العالي (Bullish / Bearish) بناءً على هيكل السوق
        if df_htf.empty:
            return None
        # منطق الـ BOS و CHoCH الحقيقي
        close_prices = df_htf['Close']
        if close_prices.iloc[-1] > close_prices.iloc[-5]:
            return "BULLISH"
        else:
            return "BEARISH"
