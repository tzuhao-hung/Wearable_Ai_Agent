import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# 初始化 GPT 客戶端
token = os.environ.get("GITHUB_TOKEN")
client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential(token),
)

def analyze_stress(data: dict) -> str:
    """
    接收一筆生理資料（dict 格式），回傳 GPT 分析結果。
    必須包含：HR, TEMP, EDA, acc_magnitude
    """
    hr = data.get("HR")
    temp = data.get("TEMP")
    eda = data.get("EDA")
    acc = data.get("acc_magnitude")

    prompt = f"""
The user provided the following physiological data:
- Heart Rate (HR): {hr} bpm
- Skin Temperature: {temp} °C
- Electrodermal Activity (EDA): {eda} µS
- Movement Acceleration: {acc}

As a stress analysis AI agent, estimate the user's stress level (Low / Medium / High),
explain your reasoning based on the data, and give one recommendation to reduce stress if needed.
"""

    response = client.complete(
        messages=[
            SystemMessage(content="You are a helpful assistant."),
            UserMessage(content=prompt)
        ],
        model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=600,
        top_p=1.0
    )

    return response.choices[0].message.content
