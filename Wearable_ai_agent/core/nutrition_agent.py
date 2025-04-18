import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Init GPT
token = os.environ.get("GITHUB_TOKEN")
client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential(token),
)

def analyze_nutrition(nutrition_data: dict, stress_result: str, sleep_result: str, activity_result: str) -> str:
    """
    Analyze nutrition intake + health conditions to suggest meals.
    Accepts:
    - nutrition_data: dict with fields like calories, protein, fat, etc.
    - stress_result / sleep_result / activity_result: string reports from other agents
    """

    prompt = f"""
The user has the following nutrition intake data for today:
- Calories: {nutrition_data.get("calories", "N/A")} kcal
- Protein: {nutrition_data.get("protein", "N/A")} g
- Fat: {nutrition_data.get("fat", "N/A")} g
- Carbs: {nutrition_data.get("carbs", "N/A")} g
- Fiber: {nutrition_data.get("fiber", "N/A")} g
- Sugar: {nutrition_data.get("sugar", "N/A")} g

Here are the user's health analysis results from other agents:

--- Stress Report ---
{stress_result}

--- Sleep Report ---
{sleep_result}

--- Activity Report ---
{activity_result}

Your tasks:
1. Analyze the nutrition data and determine if the intake is balanced.
2. Consider the stress, sleep, and activity levels to suggest nutritional adjustments.
3. Recommend a full-day meal plan (breakfast, lunch, dinner) that would improve overall health based on the current data.
4. Prioritize balance, recovery, and energy support depending on the user's state.

Be simple, supportive, and human-friendly in tone. Avoid sounding like a medical diagnosis.
"""

    response = client.complete(
        messages=[
            SystemMessage(content="You are a helpful AI nutritionist."),
            UserMessage(content=prompt)
        ],
        model="gpt-4o-mini",
        temperature=0.8,
        max_tokens=1000,
        top_p=1.0
    )

    return response.choices[0].message.content
