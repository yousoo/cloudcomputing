from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import os

app = Flask(__name__)

app.secret_key = "your_secret_key"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_db_connection():
    conn = psycopg2.connect(
        host="DB_HOST",
        database="DB_NAME",
        user="DB_USER",
        password="DB_PASSWORD",
        port="5432"
    )
    return conn


@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            posts.post_id,
            posts.image_path,
            posts.content,
            posts.created_at,
            users.username,
            COUNT(likes.like_id) AS like_count
        FROM posts
        JOIN users ON posts.user_id = users.user_id
        LEFT JOIN likes ON posts.post_id = likes.post_id
        GROUP BY posts.post_id, users.username
        ORDER BY posts.created_at DESC
    """)

    posts = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", posts=posts)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO users(username, password, name)
            VALUES (%s, %s, %s)
        """, (username, hashed_password, name))

        conn.commit()
        cur.close()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT user_id, username, password
            FROM users
            WHERE username = %s
        """, (username,))

        user = cur.fetchone()

        cur.close()
        conn.close()

        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect("/")
        else:
            return "로그인 실패"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/post/write", methods=["GET", "POST"])
def write_post():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        content = request.form["content"]
        image = request.files["image"]

        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image.save(image_path)

        db_image_path = "uploads/" + filename

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO posts(user_id, image_path, content)
            VALUES (%s, %s, %s)
        """, (session["user_id"], db_image_path, content))

        conn.commit()
        cur.close()
        conn.close()

        return redirect("/")

    return render_template("write.html")


@app.route("/post/<int:post_id>/like", methods=["POST"])
def like_post(post_id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT like_id
        FROM likes
        WHERE post_id = %s AND user_id = %s
    """, (post_id, session["user_id"]))

    existing_like = cur.fetchone()

    if existing_like:
        cur.execute("""
            DELETE FROM likes
            WHERE post_id = %s AND user_id = %s
        """, (post_id, session["user_id"]))
    else:
        cur.execute("""
            INSERT INTO likes(post_id, user_id)
            VALUES (%s, %s)
        """, (post_id, session["user_id"]))

    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")


@app.route("/post/<int:post_id>/comment", methods=["POST"])
def add_comment(post_id):
    if "user_id" not in session:
        return redirect("/login")

    comment_text = request.form["comment_text"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO comments(post_id, user_id, comment_text)
        VALUES (%s, %s, %s)
    """, (post_id, session["user_id"], comment_text))

    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")


@app.route("/profile/<username>")
def profile(username):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id, username, name
        FROM users
        WHERE username = %s
    """, (username,))

    user = cur.fetchone()

    if user is None:
        cur.close()
        conn.close()
        return "사용자를 찾을 수 없습니다."

    cur.execute("""
        SELECT post_id, image_path, content, created_at
        FROM posts
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user[0],))

    posts = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("profile.html", user=user, posts=posts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
