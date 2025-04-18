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

def summarize_health(stress_report: str, sleep_report: str, activity_report: str) -> str:
    """
    Summarize overall health condition based on stress, sleep, and activity agent reports.
    """
    prompt = f"""
Assume the following reports were generated from different time periods throughout the same day.

You are a health summary assistant.

Your task:
1. Summarize the user's **overall condition** based on the reports from other agents.
2. DO NOT repeat all the details already analyzed by the other agents.
3. Focus only on high-level takeaways, risks, and personalized advice.
4. Keep it within 4–5 short sentences. No lists, no markdown.

--- Stress Report ---
{stress_report}

--- Sleep Report ---
{sleep_report}

--- Activity Report ---
{activity_report}
"""

    response = client.complete(
        messages=[
            SystemMessage(content="You are a helpful, thoughtful health advisor."),
            UserMessage(content=prompt)
        ],
        model="gpt-4o-mini",
        temperature=0.6,
        max_tokens=800,
        top_p=1.0
    )

    return response.choices[0].message.content
