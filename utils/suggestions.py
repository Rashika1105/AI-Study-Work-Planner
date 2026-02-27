class SuggestionEngine:
    @staticmethod
    def get_suggestions(consistency, hours, tasks_missed_rate, burnout_risk):
        suggestions = []
        
        if consistency < 0.6:
            suggestions.append("Consistency is key. Try to stick to a fixed schedule for at least 5 days a week.")
            
        if hours > 10:
            suggestions.append("You're working long hours. Schedule 15-minute breaks every 2 hours to maintain focus.")
        elif hours < 3:
            suggestions.append("Consider increasing your daily focus time to reach your goals faster.")
            
        if tasks_missed_rate > 0.3:
            suggestions.append("Your deadline miss rate is high. Try splitting large tasks into smaller, manageable sub-tasks.")
            
        if burnout_risk == "High":
            suggestions.append("Priority: Rest. A tired mind is less productive. Take a full day off if possible.")
            
        if not suggestions:
            suggestions.append("You're doing great! Keep up the excellent work and maintain your current pace.")
            
        return suggestions
