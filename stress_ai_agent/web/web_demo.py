# web/web_demo.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import gradio as gr
from core.stress_agent import analyze_stress

def analyze_ui(hr, temp, eda, acc):
    data = {
        "HR": hr,
        "TEMP": temp,
        "EDA": eda,
        "acc_magnitude": acc
    }
    result = analyze_stress(data)
    return result

iface = gr.Interface(
    fn=analyze_ui,
    inputs=[
        gr.Slider(50, 150, value=80, label="Heart Rate (bpm)"),
        gr.Slider(30, 40, value=36.5, label="Temperature (°C)"),
        gr.Slider(0, 10, value=2.5, label="EDA (µS)"),
        gr.Slider(0, 100, value=50, label="acc_magnitude")
    ],
    outputs="text",
    title="🧠 Stress AI Agent",
    description="輸入一筆生理數據，讓 AI 幫你分析當前壓力程度與建議。"
)

if __name__ == "__main__":
    iface.launch()
