import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.stress_agent import analyze_stress
from simulate.generate_stress_data import generate_stress_samples

print("🎬 Generating 5 simulated user samples...")
samples = generate_stress_samples(5)

if not samples:
    print("❌ 無法獲取模擬資料。請確認 GPT 回傳格式正確。")
    exit()

for i, sample in enumerate(samples):
    print(f"\n📍 Sample {i+1}: {sample}")
    print("🧠 GPT 分析：")
    result = analyze_stress(sample)
    print(result)
    print("-" * 50)

print("\n✅ All samples analyzed.")
