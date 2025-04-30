# 🧠 Wearable Multi-Agent Health Analysis System

## Project Overview

**WearableAgent** is a lightweight backend system designed to help users better understand their physical and mental health using data collected from wearable sensors. By analyzing movement, heart rate variability (HRV), skin temperature, and electrodermal activity (EDA), the system classifies activity levels, evaluates sleep quality, and assesses stress states.

The core of the system is a modular **multi-agent architecture** built with OpenAI’s **AutoGen**. Each agent focuses on a specific domain — such as activity recognition, sleep analysis, or stress evaluation — and processes data independently. These agents then collaborate via a **GroupChat framework** to share insights and reason together.

After this discussion:
- An **Abnormal Agent** detects any unusual or critical patterns in the data.
- A **Nutrition Agent** generates personalized meal suggestions.
- A **Health Summary Agent** compiles all outputs into a clear, actionable daily health report.

This project was built to address a common gap in wearable tech: while devices collect a lot of raw data, they often fail to provide meaningful, personalized feedback. WearableAgent helps bridge that gap.

---

## What This Project Does

- Processes wearable sensor data (acceleration, HRV, temperature, GSR)
- Uses dedicated agents to analyze activity, sleep, and stress
- Runs a GroupChat to detect anomalies and generate nutrition advice
- Outputs a clear, structured daily health summary

---

## Agent Overview

Each agent is responsible for one specific aspect of health:

- **Activity Agent**  
  Detects whether the user is sedentary, walking, running, or experiencing abnormal movement. Estimates step count and calories burned.

- **Sleep Agent**  
  Analyzes HR, HRV, temperature, and movement to estimate sleep stages (Light, Deep, REM) and overall quality.

- **Stress Agent**  
  Assesses stress levels based on HRV, temperature, and EDA signals.

- **Abnormal Agent**  
  Reviews all sensor data and agent outputs to flag any critical health anomalies.

- **Nutrition Agent**  
  Suggests meals based on the user’s current physical and emotional condition, with full macronutrient breakdown.

- **Health Summary Agent**  
  Produces a friendly, final report summarizing all results with one suggestion for improvement.

---

## GroupChat Integration

After the Activity, Sleep, and Stress agents finish their analysis, a **GroupChat session** is triggered:

1. Each agent shares its result.
2. The **Abnormal Agent** reviews the findings for any critical issues.
3. The **Nutrition Agent** follows with tailored dietary suggestions.
4. The **Health Summary Agent** then wraps everything into a daily report.

This agent-to-agent collaboration mimics expert reasoning across multiple health domains.

---

## Backend Structure

The backend is implemented in Python using:

- **Flask** for handling API requests
- **AutoGen agents** that are initialized once and reused
- **Custom tools** for data processing and formatting
- A modular pipeline where each agent performs its own task before syncing through GroupChat

This structure is easy to scale and extend with new agents or sensor types.

---

## 📽️ Demo

▶️ [Watch the simulation demo on YouTube](https://youtu.be/xsnx0qr09eI)

---

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
