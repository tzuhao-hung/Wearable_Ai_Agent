import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

token = os.environ.get("GITHUB_TOKEN")
client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential(token),
)

def detect_anomalies(stress_report: str, sleep_report: str, activity_report: str) -> str:
    """
    Analyze agent reports and determine if there's any health-related anomaly.
    """
    prompt = f"""
You are an anomaly detection assistant. Assume the following reports were collected throughout the day.

Your task:
1. Detect any unusual or potentially dangerous health patterns.
2. Classify the overall severity: None / Mild / Urgent / Critical
3. Suggest 1 action the user should take.
4. Do NOT copy entire agent reports. Just give:
   - Detected Issue (if any)
   - Severity
   - Recommended Action

--- Stress Report ---
{stress_report}

--- Sleep Report ---
{sleep_report}

--- Activity Report ---
{activity_report}

Use this format:
Anomaly: <Short description>  
Severity: <Level>  
Action: <Recommendation>
"""

    response = client.complete(
        messages=[
            SystemMessage(content="You are a clinical anomaly detection assistant."),
            UserMessage(content=prompt)
        ],
        model="gpt-4o-mini",
        temperature=0.6,
        max_tokens=800,
        top_p=1.0
    )

    return response.choices[0].message.content
