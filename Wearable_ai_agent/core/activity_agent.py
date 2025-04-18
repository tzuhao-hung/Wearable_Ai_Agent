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

def analyze_activity(data: dict) -> str:
    """
    Analyze activity data and return activity type, step count, calories, and a short summary.
    Expected keys:
    - acceleration (3-axis list)
    - time (string)
    - weight (kg)
    - duration (minutes)
    """
    acc = data.get("acceleration")
    time = data.get("time")
    weight = data.get("weight")
    duration = data.get("duration")

    prompt = f"""
The following is wearable activity data collected from a user:
- Acceleration (3-axis): {acc}
- Time of Day: {time}
- Body Weight: {weight} kg
- Duration: {duration} minutes

As an AI Activity Agent, determine:
1. Activity Type (Sedentary, Walking, or Running)
2. Estimated step count
3. Estimated calories burned
4. A short explanation of how you inferred the above values

Keep your analysis concise. Limit to 3–5 key points, and avoid overly detailed physiological explanations.
Respond with each point clearly in bullet format.
"""

    response = client.complete(
        messages=[
            SystemMessage(content="You are an AI assistant specialized in activity recognition."),
            UserMessage(content=prompt)
        ],
        model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=800,
        top_p=1.0
    )

    return response.choices[0].message.content
