import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Initialize GPT client
token = os.environ.get("GITHUB_TOKEN")
client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential(token),
)

def analyze_sleep(data: dict) -> str:
    """
    Analyze sleep-related physiological data and determine sleep stage using GPT.

    Expected keys in `data`:
    - HR (Heart Rate)
    - HRV (Heart Rate Variability)
    - TEMP (Skin Temperature)
    - ACCELERATION (3-axis list)
    - GSR (Galvanic Skin Response)
    - TIME (time string like '02:00')
    """
    hr = data.get("HR")
    hrv = data.get("HRV")
    temp = data.get("TEMP")
    accel = data.get("ACCELERATION")
    gsr = data.get("GSR")
    time = data.get("TIME")

    prompt = f"""
The user provided the following nighttime physiological data:
- Heart Rate (HR): {hr} bpm
- Heart Rate Variability (HRV): {hrv} ms
- Skin Temperature: {temp} °C
- Acceleration (3-axis): {accel}
- Galvanic Skin Response (GSR): {gsr} µS
- Time of night: {time}

Keep your analysis concise. Limit to 3–5 key points, and avoid overly detailed physiological explanations.
As a sleep monitoring AI agent, estimate the user's current sleep stage (Awake / Light / Deep / REM).
Then explain your reasoning based on the physiological data and sleep science.
"""

    response = client.complete(
        messages=[
            SystemMessage(content="You are a helpful and accurate sleep analysis assistant."),
            UserMessage(content=prompt)
        ],
        model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=600,
        top_p=1.0
    )

    return response.choices[0].message.content
