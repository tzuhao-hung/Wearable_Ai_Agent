# Wearable Multi-Agent Health Analysis System

This project is a lightweight backend system that processes wearable sensor data and gives helpful health feedback.  
We use OpenAI’s AutoGen to create different agents that each handle a specific part of health analysis — like activity, sleep, and stress. Then we bring everything together into one simple daily health summary.

---

## What This Project Does

- Takes in physiological data from wearable devices
- Uses multiple agents (Activity, Sleep, Stress, etc.) to analyze the data
- Runs a conversation between agents to detect abnormalities and suggest meals
- Outputs a user-friendly daily health report with insights and tips

---

## Agent Breakdown

Here’s what each agent does:

- **Activity Agent**  
  Looks at motion data (acceleration) to figure out if the user was sedentary, walking, running, or had an abnormal event. It also estimates steps and calories.

- **Sleep Agent**  
  Uses heart rate, movement, temperature, and GSR to estimate sleep stages and quality.

- **Stress Agent**  
  Analyzes stress based on HRV, temperature, and electrodermal activity.

- **Abnormal Agent**  
  Checks for unusual health signs or events by reviewing all the sensor data and earlier agent outputs.

- **Nutrition Agent**  
  Suggests meal options based on the user's physical and mental condition, with detailed nutrition info.

- **Health Summary Agent**  
  Wraps everything up into a daily summary with one clear recommendation.

---

## How GroupChat Works

After the activity, sleep, and stress agents finish, they all talk in a shared **GroupChat** (AutoGen feature).  
This helps combine their findings into a more complete picture. The abnormal detection and nutrition agents join in after that.  
At the end, the health summary agent creates the final report.

---

## How the Backend Works

The whole backend is written in Python. We use:

- **Flask** to handle API requests
- **AutoGen agents** that get loaded once and reused
- **Custom tools** for data handling and formatting
- A clear pipeline where agents work individually, then share results in GroupChat

You can connect this backend to a frontend or use it as-is for analysis.

---

## Demo
▶️ [Watch the simulation demo on YouTube] https://youtu.be/xsnx0qr09eI
