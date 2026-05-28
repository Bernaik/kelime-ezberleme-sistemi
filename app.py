from flask import Flask, render_template, request, session
import os
from werkzeug.utils import secure_filename
import sqlite3
import random

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONSf


app.secret_key = "kelime-ezberleme-secret"

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

        return render_template(
            "message.html",
            title="Kayıt Başarılı 🎉",
            message="Hesabın başarıyla oluşturuldu. Şimdi giriş yapabilirsin.",
            button_text="Giriş Yap",
            button_link="/login",
        )

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
            return render_template(
                "message.html",
                title="Giriş Başarılı 🎉",
                message="Sisteme başarıyla giriş yaptın.",
                button_text="Quiz'e Git",
                button_link="/quiz",
            )
        else:
            return render_template(
                "message.html",
                title="Hata ❌",
                message="Kullanıcı adı veya şifre yanlış.",
                button_text="Tekrar Dene",
                button_link="/login",
            )

    return render_template("login.html")
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

        picture_path = ""

        if "picture" in request.files:

            file = request.files["picture"]

            if file and file.filename != "" and allowed_file(file.filename):

                filename = secure_filename(file.filename)

                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

                picture_path = f"uploads/{filename}"

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO words(english,turkish,sample,picture) VALUES(?,?,?,?)",
            (english, turkish, sample, picture_path),
        )

        connection.commit()
        connection.close()

        return render_template(
            "message.html",
            title="Kelime Eklendi ✅",
            message="Yeni kelime başarıyla sisteme kaydedildi.",
            button_text="Yeni Kelime Ekle",
            button_link="/add-word",
        )

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
        return render_template(
            "message.html",
            title="Ayarlar Güncellendi ⚙️",
            message=f"Soru sayısı başarıyla güncellendi: {question_count}",
            button_text="Ayarlara Dön",
            button_link="/settings",
        )

    return render_template("settings.html", question_count=question_count)


@app.route("/wordle", methods=["GET", "POST"])
def wordle():
    import sqlite3
    import random

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT english FROM words WHERE learned=1")
    learned_words = cursor.fetchall()

    if learned_words:
        word_list = [w[0].upper() for w in learned_words if len(w[0]) == 5]
    else:
        word_list = ["REBUS", "APPLE", "BRAIN", "NIGHT", "TIGER", "NOBLE"]

    connection.close()

    if "wordle_answer" not in session:
        session["wordle_answer"] = random.choice(word_list)
        session["wordle_guesses"] = []

    answer = session["wordle_answer"]
    message = ""
    game_over = False

    if request.method == "POST":
        guess = request.form["guess"].upper()

        if len(guess) != 5:
            message = "Lütfen 5 harfli bir kelime gir."
        else:
            result = []

            for i in range(5):
                if guess[i] == answer[i]:
                    result.append("correct")
                elif guess[i] in answer:
                    result.append("wrong-place")
                else:
                    result.append("wrong")

            guesses = session["wordle_guesses"]
            guesses.append({"word": guess, "result": result})
            session["wordle_guesses"] = guesses

            if guess == answer:
                message = "Tebrikler! Kelimeyi buldun 🎉"
                game_over = True
            elif len(guesses) >= 6:
                message = f"Hakkın bitti. Doğru kelime: {answer}"
                game_over = True

    if request.args.get("reset") == "1":
        session.pop("wordle_answer", None)
        session.pop("wordle_guesses", None)
        return render_template(
            "message.html",
            title="Wordle Yenilendi",
            message="Yeni oyun başlatıldı.",
            button_text="Wordle'a Dön",
            button_link="/wordle",
        )

    return render_template(
        "wordle.html",
        guesses=session.get("wordle_guesses", []),
        message=message,
        game_over=game_over,
    )


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


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        username = request.form["username"]
        new_password = request.form["new_password"]

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))

        user = cursor.fetchone()

        if user:
            cursor.execute(
                "UPDATE users SET password=? WHERE username=?", (new_password, username)
            )

            connection.commit()
            connection.close()

            return render_template(
                "message.html",
                title="Şifre Güncellendi 🔐",
                message="Şifren başarıyla değiştirildi. Yeni şifrenle giriş yapabilirsin.",
                button_text="Giriş Yap",
                button_link="/login",
            )

        connection.close()

        return render_template(
            "message.html",
            title="Kullanıcı Bulunamadı ❌",
            message="Bu kullanıcı adına ait bir hesap bulunamadı.",
            button_text="Tekrar Dene",
            button_link="/forgot-password",
        )

    return render_template("forgot_password.html")


if __name__ == "__main__":
    app.run(debug=True)
