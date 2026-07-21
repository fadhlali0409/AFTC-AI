class KeyLevels:
    def find_key_level(self, df_htf, bias):
        # تحديد مناطق الدعم/المقاومة أو الـ HTF Order Blocks / PD Arrays
        if df_htf.empty:
            return None
        return float(df_htf['High'].max() if bias == "BEARISH" else df_htf['Low'].min())
