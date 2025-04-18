import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import gradio as gr
from core.stress_agent import analyze_stress
from core.sleep_agent import analyze_sleep
from core.activity_agent import analyze_activity
from core.nutrition_agent import analyze_nutrition
from core.health_summary_agent import summarize_health
from core.anomaly_agent import detect_anomalies
from report.generate_health_report import generate_health_report

from simulate.generate_stress_data import generate_stress_samples
from simulate.generate_sleep_data import generate_sleep_samples
from simulate.generate_activity_data import generate_activity_samples
from simulate.generate_nutrition_data import generate_nutrition_sample

DATA_PATH = "/mnt/data/health_agent_data.json"

def save_step_result(key, value):
    data = {}
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
    data[key] = value
    with open(DATA_PATH, "w") as f:
        json.dump(data, f)

def load_all_results():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return {}

# 每個 Agent 都回傳兩個欄位：結果與狀態提示
def run_stress():
    status = "⏳ Running Stress Analysis..."
    data = generate_stress_samples(1)[0]
    result = analyze_stress(data)
    save_step_result("stress", result)
    return result, "✅ Done"

def run_sleep():
    status = "⏳ Running Sleep Analysis..."
    data = generate_sleep_samples(1)[0]
    result = analyze_sleep(data)
    save_step_result("sleep", result)
    return result, "✅ Done"

def run_activity():
    status = "⏳ Running Activity Analysis..."
    data = generate_activity_samples(1)[0]
    result = analyze_activity(data)
    save_step_result("activity", result)
    return result, "✅ Done"

def run_nutrition():
    status = "⏳ Running Nutrition Analysis..."
    all_data = load_all_results()
    nutrition_data = generate_nutrition_sample()
    result = analyze_nutrition(
        nutrition_data,
        all_data.get("stress", ""),
        all_data.get("sleep", ""),
        all_data.get("activity", "")
    )
    save_step_result("nutrition", result)
    save_step_result("nutrition_raw", nutrition_data)
    return result, "✅ Done"

def run_report():
    all_data = load_all_results()
    if not all(k in all_data for k in ("stress", "sleep", "activity", "nutrition")):
        return "❌ Missing data. Please run all agents before generating report.", None

    summary = summarize_health(
        all_data["stress"],
        all_data["sleep"],
        all_data["activity"]
    )
    anomaly = detect_anomalies(
        all_data["stress"],
        all_data["sleep"],
        all_data["activity"]
    )

    macros = all_data.get("nutrition_raw", {})
    nutrition_macros = {
        "Protein": macros.get("protein", 0),
        "Carbs": macros.get("carbs", 0),
        "Fat": macros.get("fat", 0)
    }

    report_path = generate_health_report(
        stress_summary=all_data["stress"],
        sleep_summary=all_data["sleep"],
        activity_summary=all_data["activity"],
        nutrition_summary=all_data["nutrition"],
        nutrition_data=nutrition_macros
    )

    return summary + "\n" + anomaly, report_path

# UI
with gr.Blocks() as demo:
    gr.Markdown("# 🧠 Wearable AI Health Agent (With Progress Status)")

    with gr.Row():
        stress_btn = gr.Button("🧠 Run Stress Agent")
        sleep_btn = gr.Button("😴 Run Sleep Agent")
        activity_btn = gr.Button("🏃 Run Activity Agent")
        nutrition_btn = gr.Button("🍽 Run Nutrition Agent")
        report_btn = gr.Button("📝 Generate Report")

    with gr.Row():
        stress_output = gr.Textbox(label="🧠 Stress Result")
        stress_status = gr.Textbox(label="Status", interactive=False)

    with gr.Row():
        sleep_output = gr.Textbox(label="😴 Sleep Result")
        sleep_status = gr.Textbox(label="Status", interactive=False)

    with gr.Row():
        activity_output = gr.Textbox(label="🏃 Activity Result")
        activity_status = gr.Textbox(label="Status", interactive=False)

    with gr.Row():
        nutrition_output = gr.Textbox(label="🍽 Nutrition Result")
        nutrition_status = gr.Textbox(label="Status", interactive=False)

    summary_output = gr.Textbox(label="📋 Summary & Anomaly")
    report_file = gr.File(label="📄 Download PDF Report")

    stress_btn.click(fn=run_stress, outputs=[stress_output, stress_status])
    sleep_btn.click(fn=run_sleep, outputs=[sleep_output, sleep_status])
    activity_btn.click(fn=run_activity, outputs=[activity_output, activity_status])
    nutrition_btn.click(fn=run_nutrition, outputs=[nutrition_output, nutrition_status])
    report_btn.click(fn=run_report, outputs=[summary_output, report_file])

if __name__ == "__main__":
    demo.launch()
