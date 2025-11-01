import json
from spellfix.engine import SpellCorrector

# Initialize and load dictionary
spell = SpellCorrector()
spell.build_from_file("data/dictionary.txt")

# Load test dataset
with open("data/test_words.json", "r", encoding="utf-8") as f:
    test_data = json.load(f)

correct = 0
total = len(test_data)
results = []

for item in test_data:
    word = item["input"]
    expected = item["expected"]

    result = spell.lookup(word, topk=1)
    predicted = result[0][0] if result else word

    is_correct = (predicted.lower() == expected.lower())
    correct += int(is_correct)
    results.append({
        "input": word,
        "predicted": predicted,
        "expected": expected,
        "status": "correct" if is_correct else "false"
    })

# Calculate and print results
accuracy = (correct / total) * 100
print(f"\n🔍 Total words tested: {total}")
print(f"✅ Correct predictions: {correct}")
print(f"📈 Accuracy: {accuracy:.2f}%\n")

print("Detailed Results:")
for r in results:
    print(f"{r['input']:10s} → Predicted: {r['predicted']:10s} | Expected: {r['expected']:10s} | {r['status']}")
