class QualityScoreCalculator:
    def evaluate(self, bias, key_level, sweep, pda, confirmation):
        # نظام تقييم الجودة بناءً على الوزن النسبي للشروط المتحققة
        score = 0
        if bias: score += 20
        if key_level: score += 20
        if sweep: score += 20
        if pda: score += 20
        if confirmation: score += 20
        return score
