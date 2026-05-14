from flask import Flask, render_template, request
import sqlite3
import random

app = Flask(__name__)

question_count = 10


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO users(username,password) VALUES(?,?)", (username, password)
        )

        connection.commit()
        connection.close()

        return "Kayıt başarılı!"

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?", (username, password)
        )

        user = cursor.fetchone()
        connection.close()

        if user:
            return "Giriş başarılı!"
        else:
            return "Kullanıcı adı veya şifre yanlış!"

    return render_template("login.html")


@app.route("/add-word", methods=["GET", "POST"])
def add_word():
    if request.method == "POST":
        english = request.form["english"]
        turkish = request.form["turkish"]
        sample = request.form["sample"]

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO words(english,turkish,sample) VALUES(?,?,?)",
            (english, turkish, sample),
        )

        connection.commit()
        connection.close()

        return "Kelime eklendi!"

    return render_template("add_word.html")


@app.route("/words")
def words():
    search = request.args.get("search", "")

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    if search:
        cursor.execute(
            "SELECT * FROM words WHERE english LIKE ? OR turkish LIKE ?",
            (f"%{search}%", f"%{search}%"),
        )
    else:
        cursor.execute("SELECT * FROM words")

    words = cursor.fetchall()
    connection.close()

    return render_template("words.html", words=words, search=search)


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    if request.method == "POST":
        word_id = request.form["word_id"]
        answer = request.form["answer"]

        cursor.execute(
            "SELECT turkish, correct_count FROM words WHERE id=?", (word_id,)
        )

        word = cursor.fetchone()

        if word:
            correct_answer = word[0]
            correct_count = word[1]

            if answer.lower() == correct_answer.lower():
                correct_count += 1
                learned = 0

                if correct_count >= 6:
                    learned = 1

                cursor.execute(
                    "UPDATE words SET correct_count=?, learned=? WHERE id=?",
                    (correct_count, learned, word_id),
                )

                connection.commit()
                connection.close()

                return render_template(
                    "quiz_result.html",
                    message=f"Doğru cevap! Tekrar sayısı: {correct_count}",
                    success=True,
                    progress=(correct_count / 6) * 100,
                )

            else:
                cursor.execute(
                    "UPDATE words SET correct_count=0, learned=0 WHERE id=?", (word_id,)
                )

                connection.commit()
                connection.close()

                return render_template(
                    "quiz_result.html",
                    message="Yanlış cevap! Sayaç sıfırlandı.",
                    success=False,
                    progress=0,
                )

    cursor.execute("SELECT * FROM words WHERE learned=0 ORDER BY RANDOM() LIMIT 1")

    word = cursor.fetchone()
    connection.close()

    return render_template("quiz.html", word=word)


@app.route("/report")
def report():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM words")
    total_words = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM words WHERE learned=1")
    learned_words_count = cursor.fetchone()[0]

    not_learned_words = total_words - learned_words_count

    if total_words > 0:
        success_rate = round((learned_words_count / total_words) * 100, 2)
    else:
        success_rate = 0

    connection.close()

    return render_template(
        "report.html",
        total_words=total_words,
        learned_words=learned_words_count,
        not_learned_words=not_learned_words,
        success_rate=success_rate,
    )


@app.route("/settings", methods=["GET", "POST"])
def settings():
    global question_count

    if request.method == "POST":
        question_count = int(request.form["question_count"])
        return f"Soru sayısı güncellendi: {question_count}"

    return render_template("settings.html", question_count=question_count)


@app.route("/wordle", methods=["GET", "POST"])
def wordle():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT english FROM words WHERE learned=1")
    word_list = cursor.fetchall()

    if len(word_list) == 0:
        cursor.execute("SELECT english FROM words")
        word_list = cursor.fetchall()

    connection.close()

    if len(word_list) == 0:
        return render_template("wordle.html", word=None)

    if request.method == "POST":
        target_word = request.form["target_word"].lower()
        guess = request.form["guess"].lower()

        result = []

        for i in range(len(guess)):
            if i < len(target_word) and guess[i] == target_word[i]:
                result.append("correct")
            elif guess[i] in target_word:
                result.append("present")
            else:
                result.append("wrong")

        is_win = guess == target_word

        return render_template(
            "wordle.html", word=target_word, guess=guess, result=result, is_win=is_win
        )

    selected_word = random.choice(word_list)[0].lower()

    return render_template("wordle.html", word=selected_word)


@app.route("/learned-words")
def learned_words():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM words WHERE learned=1")
    learned_word_list = cursor.fetchall()

    connection.close()

    return render_template("learned_words.html", learned_words=learned_word_list)


@app.route("/word-chain", methods=["GET", "POST"])
def word_chain():

    story = None
    summary = None

    if request.method == "POST":

        word1 = request.form["word1"]
        word2 = request.form["word2"]
        word3 = request.form["word3"]
        word4 = request.form["word4"]
        word5 = request.form["word5"]

        story = (
            f"One day, a curious character named {word1} began a mysterious journey during the {word2}. "
            f"Along the way, a dangerous {word3} appeared and changed everything. "
            f"Just when hope seemed lost, {word4} arrived and helped save the situation. "
            f"From that moment on, everyone remembered the meaning of {word5} as a symbol of courage and friendship."
        )

        summary = (
            f"{word1} goes on an adventure during the {word2}, faces a {word3}, "
            f"and is rescued thanks to {word4}. "
            f"The story ends with the meaning of {word5} representing bravery and friendship."
        )

    return render_template("word_chain.html", story=story, summary=summary)


if __name__ == "__main__":
    app.run(debug=True)
