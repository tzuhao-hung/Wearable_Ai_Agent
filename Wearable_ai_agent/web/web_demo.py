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
        gr.Slider(0, 100, value=50, label="Movement Acceleration (acc_magnitude)")
    ],
    outputs="text",
    title="🧠 Stress AI Agent",
    description="Input physiological data to let the AI analyze your current stress level and provide recommendations."
)

if __name__ == "__main__":
    iface.launch()