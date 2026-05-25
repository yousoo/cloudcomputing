from flask import Flask
import psycopg2

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host="webserve-db.postgres.database.azure.com",
        database="studydb",
        user="yousoo",
        password="자신의비밀번호",
        sslmode="require"
    )

@app.route("/")
def members():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT member_id, username, name, email, created_at
        FROM members
        ORDER BY member_id;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>회원 명단</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f5f5f5;
            }
            h1 {
                color: #333;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                background-color: white;
            }
            th, td {
                border: 1px solid #ccc;
                padding: 12px;
                text-align: left;
            }
            th {
                background-color: #333;
                color: white;
            }
        </style>
    </head>
    <body>
        <h1>회원 명단</h1>
        <table>
            <tr>
                <th>ID</th>
                <th>아이디</th>
                <th>이름</th>
                <th>이메일</th>
                <th>가입일</th>
            </tr>
    """

    for row in rows:
        html += f"""
            <tr>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td>{row[2]}</td>
                <td>{row[3]}</td>
                <td>{row[4]}</td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)