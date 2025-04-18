import os
import json
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Initialize GPT client using Azure
token = os.environ.get("GITHUB_TOKEN")
client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential(token),
)

def generate_stress_samples(n=5) -> list:
    """
    Generate n realistic samples of physiological data using GPT.
    For each sample, GPT determines the stress level and writes a human-friendly summary.
    """
    prompt = f"""
Please generate {n} realistic samples of physiological data from wearable devices.

For each sample:
- Include these fields:
    - HR (Heart Rate) in bpm
    - TEMP (Skin Temperature) in Celsius
    - EDA (Electrodermal Activity) in microsiemens
    - acc_magnitude (overall movement intensity)

Then:
- Estimate the stress level (choose one: Low, Medium, High) based on these values.
- Write a short, natural-language summary to the user:
    - Highlight any values that might indicate stress
    - Suggest an action or tip to help reduce stress if needed

Return the result as a JSON array of Python dictionaries.
Each dictionary should include:
HR, TEMP, EDA, acc_magnitude, stress_level, summary

Return only the raw JSON array. Do not include any markdown formatting.
"""

    response = client.complete(
        messages=[
            SystemMessage(content="You are a helpful health assistant."),
            UserMessage(content=prompt)
        ],
        model="gpt-4o-mini",
        temperature=0.9,
        max_tokens=1500,
        top_p=1.0
    )

    content = response.choices[0].message.content

    # Remove potential markdown formatting (```json ... ```)
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
