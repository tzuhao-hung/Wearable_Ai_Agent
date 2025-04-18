import os
import json
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Init GPT client
token = os.environ.get("GITHUB_TOKEN")
client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential(token),
)

def generate_activity_samples(n=3) -> list:
    """
    Generate realistic simulated activity data using GPT.
    Returns a list of dicts with keys:
    acceleration, time, weight, duration, activity, steps, calories
    """
    prompt = f"""
Please generate {n} realistic samples of physical activity data from wearable devices.

Each sample should include:
- ACCELERATION (3-axis): a list like [0.01, 0.03, 0.02]
- TIME: e.g., "14:30"
- BODY WEIGHT: in kg
- DURATION: how long the motion lasts (in minutes)

Then estimate:
- ACTIVITY TYPE: Sedentary / Walking / Running
- STEP COUNT: estimated steps taken (must be non-zero if walking or running)
- CALORIES BURNED: based on body weight + duration + activity type

Also include a short summary of how this was inferred.

Return only the raw JSON array. Do not include any explanation, markdown code block (like ```json), or summary text outside the array. Just return the array like: [ {{...}}, {{...}} ]
"""

    response = client.complete(
        messages=[
            SystemMessage(content="You are a motion tracking assistant."),
            UserMessage(content=prompt)
        ],
        model="gpt-4o-mini",
        temperature=0.8,
        max_tokens=1500,
        top_p=1.0
    )

    content = response.choices[0].message.content

    # 🧹 Clean GPT output
    if "```json" in content:
        content = content.split("```json")[-1]
    if "```" in content:
        content = content.split("```")[0]
    if "###" in content:
        content = content.split("###")[0]
    content = content.strip()

    try:
        raw = json.loads(content)

        # 🔁 Normalize keys
        normalized_samples = []
        for item in raw:
            if isinstance(item, dict):
                new_item = {}
                for k, v in item.items():
                    key = k.lower().strip()

                    if key == "body weight":
                        new_item["weight"] = v
                    elif key == "step count":
                        new_item["steps"] = v
                    elif key == "activity type":
                        new_item["activity"] = v
                    elif key == "calories burned":
                        new_item["calories"] = v
                    else:
                        new_item[key] = v

                normalized_samples.append(new_item)

        #print("✅ Normalized Activity Samples:\n", json.dumps(normalized_samples, indent=2))

        # ✅ Filter out incomplete entries
        samples = [
            s for s in normalized_samples
            if s.get("acceleration") and s.get("duration") and s.get("weight")
        ]

        if not samples:
            print("⚠️ No valid activity samples parsed.")
            return []

        return samples

    except json.JSONDecodeError:
        print("⚠️ GPT response parsing failed:\n", content)
        return []


