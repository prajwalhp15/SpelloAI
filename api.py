from flask import Flask, request, jsonify
from spellfix.engine import SpellCorrector

app = Flask(__name__)

# Initialize spell corrector
spell = SpellCorrector()  
spell.build_from_file("data/dictionary.txt")  # Load dictionary here

# Optional home route (fixes 404 on root URL)
@app.route('/')
def home():
    return " Spell Correction API is running"

# API endpoint for correction
@app.route('/correct', methods=['POST'])
def correct_word():
    data = request.get_json()
    word = data.get("word", "")
    if not word:
        return jsonify({"error": "No word provided"}), 400

    result = spell.lookup(word, topk=1)
    if result:
        corrected_word, _ = result[0]
    else:
        corrected_word = word

    return jsonify({
        "input": word,
        "corrected": corrected_word
    })

if __name__ == "__main__":
    app.run(debug=True)
