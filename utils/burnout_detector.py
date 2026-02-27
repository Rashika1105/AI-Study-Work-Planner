class BurnoutDetector:
    @staticmethod
    def detect(avg_hours, sleep_hours, task_completion_rate, stress_level):
        """
        Logic:
        High hours (>10 hrs daily)
        Low sleep (<5 hrs)
        Low task completion rate (<60%)
        High stress input (>7)
        """
        risk_score = 0
        
        if avg_hours > 10:
            risk_score += 3
        elif avg_hours > 8:
            risk_score += 1
            
        if sleep_hours < 5:
            risk_score += 3
        elif sleep_hours < 7:
            risk_score += 1
            
        if task_completion_rate < 0.6:
            risk_score += 2
            
        if stress_level > 7:
            risk_score += 2
            
        if risk_score >= 6:
            return "High", "Your burnout risk is critical. Please take immediate rest and reduce your workload."
        elif risk_score >= 3:
            return "Medium", "You are at moderate risk of burnout. Consider taking more breaks and improving sleep."
        else:
            return "Low", "You are managing your workload well. Keep maintaining a healthy balance."
