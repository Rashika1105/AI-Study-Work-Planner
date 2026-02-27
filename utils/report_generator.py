from fpdf import FPDF
import os

class ReportGenerator:
    @staticmethod
    def generate_pdf(user, tasks, pred_score, burnout_risk, suggestions):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        
        # Header
        pdf.cell(190, 10, "AI Study & Work Planner - Performance Report", 0, 1, 'C')
        pdf.ln(10)
        
        # User Info
        pdf.set_font("Arial", size=12)
        pdf.cell(190, 10, f"User: {user.username}", 0, 1)
        pdf.cell(190, 10, f"Date: {os.popen('date /t').read().strip()}", 0, 1)
        pdf.ln(5)
        
        # Performance Summary
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, "Performance Summary", 0, 1)
        pdf.set_font("Arial", size=12)
        pdf.cell(190, 10, f"Predicted Performance Score: {pred_score}%", 0, 1)
        pdf.cell(190, 10, f"Burnout Risk Level: {burnout_risk}", 0, 1)
        pdf.ln(5)
        
        # Task Summary
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, "Recent Tasks", 0, 1)
        pdf.set_font("Arial", size=10)
        for task in tasks[-5:]: # Last 5 tasks
            status = "Completed" if task.completed else "Pending"
            pdf.cell(190, 8, f"- {task.title} ({task.category}) | Status: {status}", 0, 1)
        pdf.ln(5)
        
        # Suggestions
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, "AI Suggestions", 0, 1)
        pdf.set_font("Arial", size=12)
        for sug in suggestions:
            pdf.multi_cell(190, 8, f"* {sug}")
            
        reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'reports')
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
            
        filename = f"report_{user.id}.pdf"
        filepath = os.path.join(reports_dir, filename)
        pdf.output(filepath)
        return filename
