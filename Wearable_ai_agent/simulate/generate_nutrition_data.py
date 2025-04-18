import os
import json
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Init GPT
token = os.environ.get("GITHUB_TOKEN")
client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential(token),
)

def generate_nutrition_sample() -> dict:
    """
    Generate a realistic single-day nutrition intake sample using GPT.
    """
    prompt = """
Generate a realistic daily nutrition intake summary for a person.
Include the following fields in the output:
- calories (in kcal)
- protein (in grams)
- fat (in grams)
- carbs (in grams)
- fiber (in grams)
- sugar (in grams)

Return only a single JSON object like:
{
  "calories": ...,
  "protein": ...,
  "fat": ...,
  "carbs": ...,
  "fiber": ...,
  "sugar": ...
}

Do not include explanations, markdown, or formatting. Return only the raw JSON.
"""

    response = client.complete(
        messages=[
            SystemMessage(content="You are a helpful health assistant."),
            UserMessage(content=prompt)
        ],
        model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=500,
        top_p=1.0
    )

    content = response.choices[0].message.content.strip()

    # Clean markdown or extra text
    if "```json" in content:
        content = content.split("```json")[-1]
    if "```" in content:
        content = content.split("```")[0]
    if "###" in content:
        content = content.split("###")[0]

    content = content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("⚠️ Failed to parse nutrition sample:\n", content)
        return {}

# Example test run
if __name__ == "__main__":
    print(json.dumps(generate_nutrition_sample(), indent=2))
