class PDAAnalyzer:
    def find_valid_pda(self, df_ltf, bias):
        # تحديد مناطق اهتمام السعر (Premium / Discount و Order Blocks / FVG)
        if df_ltf.empty:
            return None
        return float(df_ltf['Close'].iloc[-1])
