# autogen_demo.py (enhanced with NutritionAgent)

import sys
import os

# Add parent directory to import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from autogen import UserProxyAgent, AssistantAgent
from core.stress_agent import analyze_stress
from core.sleep_agent import analyze_sleep
from simulate.generate_stress_data import generate_stress_samples
from simulate.generate_sleep_data import generate_sleep_samples
from core.health_summary_agent import summarize_health
from core.activity_agent import analyze_activity
from simulate.generate_activity_data import generate_activity_samples
from core.anomaly_agent import detect_anomalies
from core.nutrition_agent import analyze_nutrition
from simulate.generate_nutrition_data import generate_nutrition_sample

# 🧠 Define agents using AssistantAgent wrapper
user = UserProxyAgent(name="User", code_execution_config=False)

stress_agent = AssistantAgent(
    name="StressAgent",
    system_message="You are a stress analysis expert.",
    llm_config=False,
    function_map={"analyze_stress": analyze_stress}
)

sleep_agent = AssistantAgent(
    name="SleepAgent",
    system_message="You are a sleep analysis expert.",
    llm_config=False,
    function_map={"analyze_sleep": analyze_sleep}
)

activity_agent = AssistantAgent(
    name="ActivityAgent",
    system_message="You are a physical activity expert.",
    llm_config=False,
    function_map={"analyze_activity": analyze_activity}
)

health_summary_agent = AssistantAgent(
    name="HealthSummaryAgent",
    system_message="You are a health summary expert. You combine results from multiple agents to provide a holistic overview of the user's physical and mental state.",
    llm_config=False,
    function_map={"summarize_health": summarize_health}
)

anomaly_agent = AssistantAgent(
    name="AnomalyDetectionAgent",
    system_message="You are an anomaly detection assistant. Your task is to detect and categorize potential health risks based on the analysis reports from other agents.",
    llm_config=False,
    function_map={"detect_anomalies": detect_anomalies}
)

# 🚀 Generate sample data
stress_data = generate_stress_samples(1)[0]
sleep_data = generate_sleep_samples(1)[0]
activity_data = generate_activity_samples(1)[0]
nutrition_data = generate_nutrition_sample()

# ✅ Manually invoke each agent's function

print("🧠 Calling StressAgent...")
stress_result = stress_agent.function_map["analyze_stress"](stress_data)
print("\n📊 StressAgent result:")
print(stress_result)

print("\n😴 Calling SleepAgent...")
sleep_result = sleep_agent.function_map["analyze_sleep"](sleep_data)
print("\n🌙 SleepAgent result:")
print(sleep_result)

print("\n🏃 Calling ActivityAgent...")
activity_result = activity_agent.function_map["analyze_activity"](activity_data)
print("\n🏃 ActivityAgent result:")
print(activity_result)

print("\n📋 Calling HealthSummaryAgent...")
summary = health_summary_agent.function_map["summarize_health"](stress_result, sleep_result, activity_result)
print("\n📝 Health Summary Agent says:\n")
print(summary)

print("\n🚨 Calling AnomalyDetectionAgent...")
anomaly_result = anomaly_agent.function_map["detect_anomalies"](stress_result, sleep_result, activity_result)
print("\n🚨 Anomaly Detection Result:")
print(anomaly_result)

print("\n🍽 Calling NutritionAgent...")
nutrition_result = analyze_nutrition(nutrition_data, stress_result, sleep_result, activity_result)
print("\n🍽 NutritionAgent result:")
print(nutrition_result)
