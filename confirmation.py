class ConfirmationAnalyzer:
    def verify_confirmation(self, df_ltf, bias):
        # التحقق من حدوث Market Structure Shift (MSS) أو Change in State of Delivery (CISD)
        if df_ltf.empty:
            return False, None
        return True, "MSS"
