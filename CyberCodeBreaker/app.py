from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Game State Storage
game_data = {
    "secret_code": [],
    "attempts_left": 7
}

def generate_code():
    # Generates 4 unique random digits (0-9)
    return [str(x) for x in random.sample(range(10), 4)]

@app.route('/')
def index():
    game_data["secret_code"] = generate_code()
    game_data["attempts_left"] = 7
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    user_guess = request.json.get("guess", "")
    
    # Validation
    if len(user_guess) != 4 or not user_guess.isdigit() or len(set(user_guess)) != 4:
        return jsonify({"status": "invalid", "message": "Enter 4 unique digits!"})
    
    game_data["attempts_left"] -= 1
    guess_list = list(user_guess)
    secret = game_data["secret_code"]

    # Calculate Exact Matches (Bulls) and Partial Matches (Cows)
    exact_matches = sum(1 for i in range(4) if guess_list[i] == secret[i])
    partial_matches = sum(1 for i in range(4) if guess_list[i] in secret and guess_list[i] != secret[i])

    if exact_matches == 4:
        return jsonify({
            "status": "win",
            "message": "SYSTEM HACKED! Code Breaker Success!",
            "secret": "".join(secret)
        })

    if game_data["attempts_left"] <= 0:
        return jsonify({
            "status": "lose",
            "message": f"ACCESS DENIED! Code was: {''.join(secret)}",
            "secret": "".join(secret)
        })

    return jsonify({
        "status": "continue",
        "exact": exact_matches,
        "partial": partial_matches,
        "attempts_left": game_data["attempts_left"],
        "guess": user_guess
    })

@app.route('/reset', methods=['POST'])
def reset():
    game_data["secret_code"] = generate_code()
    game_data["attempts_left"] = 7
    return jsonify({"status": "reset"})

if __name__ == '__main__':
    app.run(debug=True)