# 🧠 Wearable Multi-Agent Health Analysis System

![image alt][https://github.com/tzuhao-hung/Wearable_Ai_Agent/blob/eeda7b08113bec0ecf94704820202c4b3733cae3/image.png]

## 🎯 Problem & Motivation

With an increasing number of young people choosing not to marry, the demand for independent living and long-term care solutions will grow. WearableAgent is designed to meet this demand, providing real-time health monitoring and personalized care, making it an essential tool for those living alone in the future.

WearableAgent addresses this by integrating wearable data tracking with AI technology, offering customized health recommendations and care, especially for individuals living alone.

## Project Overview

**WearableAgent** is a lightweight backend system designed to help users better understand their physical and mental health using data collected from wearable sensors. By analyzing movement, heart rate variability (HRV), skin temperature, and electrodermal activity (EDA), the system classifies activity levels, evaluates sleep quality, and assesses stress states.

The core of the system is a modular **multi-agent architecture** built with OpenAI’s **AutoGen**. Each agent focuses on a specific domain — such as activity recognition, sleep analysis, or stress evaluation — and processes data independently. These agents then collaborate via a **GroupChat framework** to share insights and reason together.

After this discussion:
- An **Abnormal Agent** detects any unusual or critical patterns in the data.
- A **Nutrition Agent** generates personalized meal suggestions.
- A **Health Summary Agent** compiles all outputs into a clear, actionable daily health report.

This project was built to address a common gap in wearable tech: while devices collect a lot of raw data, they often fail to provide meaningful, personalized feedback. WearableAgent helps bridge that gap.

---
## 📽️ Demo

▶️ [Watch the simulation demo on YouTube](https://youtu.be/xsnx0qr09eI)
---

## What This Project Does

- Processes wearable sensor data (acceleration, HRV, temperature, GSR)
- Uses dedicated agents to analyze activity, sleep, and stress
- Runs a GroupChat to detect anomalies and generate nutrition advice
- Outputs a clear, structured daily health summary

---

## Frontend Module

**Functionality**
The frontend module, built with the Streamlit framework, is the primary interface for user interaction. It allows users to input health-related data and visualize analytical results in an intuitive format. Key features include:

- **User Profile Management**: Users can register new profiles or select existing ones.

- **Data Entry**: Users can input activity, sleep, and stress-related data.

- **Results Visualization**: Analytical outcomes are displayed using charts and textual summaries.

- **Personalized Menu Suggestions**: Tailored dietary plans are generated and presented based on the user's physiological state.

**Key Code Components**

- **app/frontend/app.py**:

  - Implements the main interface, allowing user selection, data input, and analysis triggers.
  - Sends API requests to the backend for activity, sleep, and stress analysis (e.g., /analyze_activity, /analyze_sleep).

- **app/frontend/app_func.py**:

  - Contains functions for generating charts, such as draw_consumption_intake_chart and draw_sleep_chart.
  - Implements the render_menu function to display dietary suggestions.
---
## Backend Structure

The backend is implemented in Python using:

- **Flask** for handling API requests
- **AutoGen agents** that are initialized once and reused
- **Custom tools** for data processing and formatting
- A modular pipeline where each agent performs its own task before syncing through GroupChat

This structure is easy to scale and extend with new agents or sensor types.

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
## System Integration Workflow

The interaction between frontend and backend follows a clear pipeline:

1. User Input: Users enter physiological and behavioral data through the Streamlit frontend.
2. Data Transmission: The frontend sends structured data to the backend via RESTful API calls.
3. Agent Collaboration: Each backend agent processes its assigned data. Results are shared through a GroupChat-like system where agents exchange and refine interpretations.
4. Report Compilation: The Health Summary Agent gathers all insights and presents them as a holistic report.
5. Result Display: The final report and visualizations are rendered back on the frontend for user review.

---
## Future Work and Product Potential
WearableAgent has strong potential for further expansion:

  -**Smart Home Integration**: The system can connect with smart appliances (e.g., lighting, air conditioning) to create a responsive, health-optimized living environment.

  -**Support for Independent Living**: Especially beneficial for elderly individuals living alone, the system can monitor health trends and alert caregivers or emergency contacts in case of anomalies.

  -**Scalable Health Solutions**: With its modular design, the system can be adapted for corporate wellness programs, assisted living, or even broader public health applications.

By aligning with trends in smart living and long-term care, WearableAgent offers a promising path toward more proactive, personalized, and connected health management.

---

## Meet the Team
| 👤 Name | 🧠 Role | 💬 GitHub | 💬 More Info |
|--------|---------|------------|------------|
| 🧑‍💻 Howard | Backend Agent Developer | @tzuhao-huang |linkedin.com/in/tzuhaohung1
| 🧑‍💻 Chia | Backend Agent Developer  | @Lin8823 |c.m.peng23@gmail.com
| 🧑‍💻 Jess | Full Stack Developer | @dsjes |linkedin.com/in/jess-hsieh
| 🧑‍💻 Yung | Full Stack Developer  | @Chiang0111 |linkedin.com/in/yung-chun-chiang-76841222a
