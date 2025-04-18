import os
import json
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Initialize GPT client using Azure
token = os.environ.get("GITHUB_TOKEN")  # You already set this
client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential(token),
)

def generate_sleep_samples(n=5) -> list:
    """
    Generate n realistic samples of sleep-related physiological data using GPT.
    """
    prompt = f"""
Please generate {n} realistic samples of nighttime physiological data from wearable devices.

Each sample should include the following fields:
- HR (Heart Rate) in bpm
- HRV (Heart Rate Variability) in ms
- TEMP (Skin Temperature) in Celsius
- ACCELERATION (3-axis as [x, y, z])
- GSR (Galvanic Skin Response) in microsiemens
- TIME (e.g., 23:00, 02:00, 04:00)
- Estimated sleep stage (choose one: Awake, Light, Deep, REM)
- One-sentence explanation of why this stage was inferred

Return the result as a JSON array of Python dictionaries.
Each dictionary should include:
HR, HRV, TEMP, ACCELERATION, GSR, TIME, sleep_stage, explanation

Return only the raw JSON array. Do not include any markdown formatting.
"""

    response = client.complete(
        messages=[
            SystemMessage(content="You are a helpful sleep monitoring assistant."),
            UserMessage(content=prompt)
        ],
        model="gpt-4o-mini",
        temperature=0.9,
        max_tokens=1800,
        top_p=1.0
    )

    content = response.choices[0].message.content

    # Clean up markdown formatting if needed
    if content.startswith("```json"):
        content = content.replace("```json", "").strip("`").strip()
    elif content.startswith("```"):
        content = content.strip("`").strip()

    try:
        samples = json.loads(content)
        return samples
    except json.JSONDecodeError:
        print("⚠️ Failed to parse GPT response. Raw content below:\n", content)
        return []

# For testing directly
if __name__ == "__main__":
    data = generate_sleep_samples(3)
    for d in data:
        print(json.dumps(d, indent=2))
