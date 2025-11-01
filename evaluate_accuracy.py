import csv
import os

def evaluate_accuracy(reference_file="data/dictionary.txt", output_file="data/output.txt"):
    total = 0
    correct = 0
    wrong_samples = []

    if not os.path.exists(reference_file):
        print(f"❌ Reference file not found: {reference_file}")
        return
    if not os.path.exists(output_file):
        print(f"❌ Output file not found: {output_file}")
        return

    with open(output_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        reference_text = open(reference_file, encoding="utf-8").read().lower()

        for row in reader:
            if len(row) < 2:
                continue
            error, corrected = row
            total += 1
            if corrected.lower().strip() in reference_text:
                correct += 1
            else:
                wrong_samples.append((error, corrected))

    accuracy = (correct / total) * 100 if total else 0
    print(f"✅ Total words: {total}")
    print(f"✅ Correctly corrected: {correct}")
    print(f"🎯 Accuracy: {accuracy:.2f}%")

    print("\n⚠️ Sample incorrect corrections:")
    for e, c in wrong_samples[:10]:
        print(f"  {e} → {c}")

if __name__ == "__main__":
    evaluate_accuracy()
