import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
import json

# 初始化 GPT 客戶端
token = os.environ.get("GITHUB_TOKEN")
client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential(token),
)

def generate_stress_samples(n=5) -> list:
    """
    使用 GPT 生成 n 筆模擬的生理資料樣本，格式為 list of dicts。
    每筆資料包含 HR, TEMP, EDA, acc_magnitude。
    """
    prompt = f"""
Please generate {n} realistic samples of physiological data from wearable devices.
For each sample, include the following fields:
- HR (Heart Rate) in bpm
- TEMP (Skin Temperature) in Celsius
- EDA (Electrodermal Activity) in microsiemens
- acc_magnitude (overall movement intensity)

Return the data as a JSON list of Python dictionaries.
Each dictionary should include these keys: HR, TEMP, EDA, acc_magnitude.
Only return the JSON array.
"""

    response = client.complete(
        messages=[
            SystemMessage(content="You are a helpful assistant."),
            UserMessage(content=prompt)
        ],
        model="gpt-4o-mini",
        temperature=0.9,
        max_tokens=1000,
        top_p=1.0
    )

    content = response.choices[0].message.content

    # 🧽 清除 markdown block 標記（```json ... ```）
    if content.startswith("```json"):
        content = content.replace("```json", "").strip("`").strip()
    elif content.startswith("```"):
        content = content.strip("`").strip()

    try:
        samples = json.loads(content)
        return samples
    except json.JSONDecodeError:
        print("⚠️ 無法解析 GPT 回傳的 JSON 格式。請檢查內容：\n", content)
        return []

