import sys
import os

# Add parent directory to import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from simulate.generate_stress_data import generate_stress_samples
from core.stress_agent import analyze_stress  # Optional if you're still using it

print("🎬 Generating 5 simulated stress samples using GPT...")
samples = generate_stress_samples(5)

if not samples:
    print("❌ Failed to retrieve samples. Please check GPT response format.")
    exit()

for i, sample in enumerate(samples, start=1):
    print(f"\n📍 Sample {i}:")
    print(f"  - Heart Rate: {sample['HR']} bpm")
    print(f"  - Temperature: {sample['TEMP']} °C")
    print(f"  - EDA: {sample['EDA']} µS")
    print(f"  - Movement: {sample['acc_magnitude']}")
    print(f"  - Stress Level: {sample.get('stress_level', 'N/A')}")
    print("🧠 Summary:")
    print(sample.get("summary", "No summary provided."))
    print("-" * 50)

print("\n✅ All samples successfully analyzed.")
