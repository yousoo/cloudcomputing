from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host="Azure_PostgreSQL_서버주소",
        database="studydb",
        user="사용자명",
        password="비밀번호",
        port="5432"
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/phone", methods=["GET", "POST"])
def phone():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        memo = request.form["memo"]

        conn = get_connection()
        cur = conn.cursor()

        sql = """
        INSERT INTO phonebook (name, phone, memo)
        VALUES (%s, %s, %s)
        """

        cur.execute(sql, (name, phone, memo))

        conn.commit()
        cur.close()
        conn.close()

        return redirect("/phone")

    return render_template("phone.html")

@app.route("/phone_list")
def phone_list():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            phonebook_id,
            name,
            phone,
            memo,
            created_at
        FROM phonebook
        ORDER BY phonebook_id DESC
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "phone_list.html",
        rows=rows
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
