import matplotlib.pyplot as plt
from fpdf import FPDF
import os


def generate_nutrition_chart(data, save_path):
    import os
    os.makedirs(os.path.dirname(save_path), exist_ok=True)  
    labels = list(data.keys())
    values = list(data.values())
    plt.figure(figsize=(4, 4))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.title("Macronutrient Breakdown")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

class HealthPDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Daily Health Report", ln=True, align="C")
        self.ln(5)

    def section_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_text_color(0)
        self.cell(0, 10, title, ln=True)

    def section_body(self, text):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 10, text)
        self.ln()

def generate_health_report(
    stress_summary: str,
    sleep_summary: str,
    activity_summary: str,
    nutrition_summary: str,
    nutrition_data: dict,
    output_path: str = "/mnt/data/health_report.pdf"
):
    chart_path = "/mnt/data/temp_nutrition_chart.png"
    generate_nutrition_chart(nutrition_data, chart_path)

    pdf = HealthPDFReport()
    pdf.add_page()

    pdf.section_title("Stress Analysis")
    pdf.section_body(stress_summary)

    pdf.section_title("Sleep Analysis")
    pdf.section_body(sleep_summary)

    pdf.section_title("Activity Analysis")
    pdf.section_body(activity_summary)

    pdf.section_title("Nutrition Summary")
    pdf.section_body(nutrition_summary)

    if os.path.exists(chart_path):
        pdf.image(chart_path, w=80, h=80, x=65)

    pdf.output(output_path)
    return output_path
