# autogen_demo.py (AutoGen GroupChat version: AI Health Team)

import sys
import os

# Add parent directory to import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from autogen import (
    UserProxyAgent,
    AssistantAgent,
    GroupChat,
    GroupChatManager
)
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

# 🚀 Generate shared sample data
stress_data = generate_stress_samples(1)[0]
sleep_data = generate_sleep_samples(1)[0]
activity_data = generate_activity_samples(1)[0]
nutrition_data = generate_nutrition_sample()

# 👤 User agent
user = UserProxyAgent(name="User", code_execution_config=False)

# 🧠 Functional agents
stress_agent = AssistantAgent(
    name="StressAgent",
    llm_config=False,
    function_map={"analyze_stress": lambda _: analyze_stress(stress_data)},
    system_message="You are a stress analysis expert. Use preloaded data to analyze."
)

sleep_agent = AssistantAgent(
    name="SleepAgent",
    llm_config=False,
    function_map={"analyze_sleep": lambda _: analyze_sleep(sleep_data)},
    system_message="You are a sleep analysis expert. Use preloaded data to analyze."
)

activity_agent = AssistantAgent(
    name="ActivityAgent",
    llm_config=False,
    function_map={"analyze_activity": lambda _: analyze_activity(activity_data)},
    system_message="You are a physical activity expert. Use preloaded data to analyze."
)

anomaly_agent = AssistantAgent(
    name="AnomalyDetectionAgent",
    llm_config=False,
    function_map={"detect_anomalies": lambda args: detect_anomalies(
        args['stress'], args['sleep'], args['activity'])},
    system_message="You detect and rate potential health anomalies based on agent reports."
)

nutrition_agent = AssistantAgent(
    name="NutritionAgent",
    llm_config=False,
    function_map={"analyze_nutrition": lambda args: analyze_nutrition(
        nutrition_data, args['stress'], args['sleep'], args['activity'])},
    system_message="You recommend a personalized meal plan using nutrition intake and health reports."
)

summary_agent = AssistantAgent(
    name="HealthSummaryAgent",
    llm_config=False,
    function_map={"summarize_health": lambda args: summarize_health(
        args['stress'], args['sleep'], args['activity'])},
    system_message="You summarize the user's health based on agent results."
)

# 🧑‍⚕️ Group chat setup
groupchat = GroupChat(
    agents=[
        user,
        stress_agent,
        sleep_agent,
        activity_agent,
        anomaly_agent,
        nutrition_agent,
        summary_agent
    ],
    messages=[],
    max_round=8
)


manager = GroupChatManager(
    groupchat=groupchat,
    llm_config={
        "config_list": [{
            "model": "gpt-4o",
            "api_key": os.environ["GITHUB_TOKEN"]
        }]
    }
)



# 🟢 Start collaborative conversation
user.initiate_chat(
    manager,
    message="""
Hi team, based on today’s wearable data, how am I doing overall?
Do I need to adjust anything in my health or diet today?
"""
)
