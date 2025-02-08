from flask import Flask, request, redirect, url_for
import random

app = Flask(__name__)

# ✅ List of 3 valid access codes
ACCESS_CODES = ["DDAYYOONGI", "AGUSTD", "SUGA123"]

# 30 Multiple-Choice Questions about D-DAY Album
questions = [
    {"question": "What is the title track of Yoongi's album D-DAY?", "options": ["Haegeum", "Moonlight", "Snooze"], "answer": "Haegeum"},
    {"question": "What is the meaning of 'Haegeum'?", "options": ["A traditional Korean instrument", "Freedom", "Both"], "answer": "Both"},
    {"question": "Which song on D-DAY features IU?", "options": ["People Pt. 2", "SDL", "Snooze"], "answer": "People Pt. 2"},
    {"question": "What is the first track on D-DAY?", "options": ["D-Day", "Haegeum", "Amygdala"], "answer": "D-Day"},
    {"question": "What track from D-DAY encourages listeners to embrace their true selves?", "options": ["Polar Night", "Interlude: Dawn", "Amygdala"], "answer": "Polar Night"},
    {"question": "Which track highlights themes of determination?", "options": ["Amygdala", "SDL", "Snooze"], "answer": "Amygdala"},
    {"question": "What is the interlude track on D-DAY?", "options": ["SDL", "Amygdala", "People Pt. 2"], "answer": "SDL"},
    {"question": "What is the final track on D-DAY?", "options": ["Life Goes On", "Snooze", "Amygdala"], "answer": "Life Goes On"},
]

random.shuffle(questions)  # Shuffle questions for every game

# Game state
game_state = {
    "current_index": 0,
    "score": 0,
    "access_granted": False  # Access control variable
}

@app.route("/", methods=["GET", "POST"])
def access_code():
    if request.method == "POST":
        user_code = request.form["access_code"].strip()
        if user_code in ACCESS_CODES:  # ✅ Check if user entered one of the valid codes
            game_state["access_granted"] = True
            return redirect(url_for("quiz"))
        else:
            return '''
            <h1>Invalid Access Code! ❌</h1>
            <a href="/">Try Again</a>
            '''

    return '''
    <h1>Enter Access Code to Play</h1>
    <form method="POST">
        <input type="text" name="access_code" placeholder="Enter Code" required>
        <button type="submit">Submit</button>
    </form>
    '''

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if not game_state["access_granted"]:
        return redirect(url_for("access_code"))

    # Handle answers
    if request.method == "POST":
        user_answer = request.form["answer"]
        correct_answer = questions[game_state["current_index"]]["answer"]

        # Check if the answer is correct
        if user_answer == correct_answer:
            game_state["score"] += 1

        # Move to the next question
        game_state["current_index"] += 1

    # Check if there are no more questions
    if game_state["current_index"] >= len(questions):
        return redirect(url_for("end"))

    # Display current question and options
    current_question = questions[game_state["current_index"]]
    question_text = current_question["question"]
    options = current_question["options"]

    options_html = ""
    for option in options:
        options_html += f'<button type="submit" name="answer" value="{option}">{option}</button><br>'

    return f"""
    <h1>D-DAY Album Trivia</h1>
    <p>{question_text}</p>
    <form method="POST">
        {options_html}
    </form>
    <p>Score: {game_state["score"]}/{len(questions)}</p>
    """

@app.route("/end")
def end():
    final_score = game_state["score"]
    total_questions = len(questions)

    return f"""
    <h1>Game Over!</h1>
    <p>Your final score: {final_score}/{total_questions}</p>
    <a href="/">Play Again</a>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
