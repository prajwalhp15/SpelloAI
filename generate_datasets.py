import random
import os

# Folder where you want to save the files
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

DICT_PATH = os.path.join(DATA_FOLDER, "dictionary.txt")
ERROR_PATH = os.path.join(DATA_FOLDER, "errors.txt")

# Base list of Indian-origin words written in English script
base_words = [
    "Aam", "Ram", "Bandegai", "Pattaguyra", "Rasam", "Idli", "Dosa", "Chapathi",
    "Puri", "Kichdi", "Puliyogare", "Bisibele", "Roti", "Sambar", "Chutney",
    "Pulao", "Upma", "Sabzi", "Biryani", "Kheer", "Payasa", "Gulab", "Jalebi",
    "Paneer", "Masala", "Vada", "Pakoda", "Dal", "Raita", "Chole", "Bhature",
    "Poori", "Kofta", "Halwa", "Kesari", "Lassi", "Roti", "Pav", "Bhaji",
    "Samosa", "Kachori", "Momo", "Rogan", "Josh", "Paratha", "Khichdi", "Thepla",
    "Dhokla", "Pesarattu", "Ragi", "Mudda", "Rava", "Tamarind", "Curd"
]

# Expand to 5000 unique-looking words by adding suffixes/prefixes
dictionary_words = []
for i in range(5000):
    w = random.choice(base_words)
    variation = w + random.choice(["", "a", "e", "i", "o", "u", "ya", "ra", "ji", "la", "ga", "na", "ka", "ma", "sa"])
    dictionary_words.append(variation.capitalize())

# Write the correct dictionary file
with open(DICT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(dictionary_words))

# Function to create misspellings
def make_misspelling(word):
    word = list(word)
    ops = [
        lambda w: w[:-1] if len(w) > 2 else w,                  # missing last letter
        lambda w: w + [random.choice(["m", "n", "a"])],         # extra letter
        lambda w: [c.lower() for c in w],                       # all lowercase
        lambda w: [c.upper() for c in w],                       # all uppercase
        lambda w: [random.choice([c.upper(), c.lower()]) for c in w],  # mixed case
        lambda w: [random.choice([c, random.choice("aeiou")]) for c in w],  # vowel swap
        lambda w: w[::-1] if len(w) > 3 else w                  # reverse for small words
    ]
    func = random.choice(ops)
    w2 = "".join(func(word))
    return w2

# Generate 10,000 misspelled versions
error_words = [make_misspelling(random.choice(dictionary_words)) for _ in range(10000)]

# Write the errors file
with open(ERROR_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(error_words))

print(f"✅ Created {DICT_PATH} (5000 words)")
print(f"✅ Created {ERROR_PATH} (10000 misspellings)")
print("Done! Files match assignment format.")
