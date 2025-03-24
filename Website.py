import sqlite3
from flask import Flask, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Replace with a secure secret key

# HTML templates (using render_template_string for simplicity)
login_page = """
<!doctype html>
<html>
  <head>
    <title>Login</title>
  </head>
  <body>
    <h2>Login with your key</h2>
    <form method="post">
      <input type="password" name="key" placeholder="Enter your key" required>
      <input type="submit" value="Login">
    </form>
    {% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
  </body>
</html>
"""

dashboard_page = """
<!doctype html>
<html>
  <head>
    <title>Dashboard</title>
  </head>
  <body>
    <h2>Dashboard</h2>
    <p>Welcome! You are logged in with key: {{ key }}</p>
    <ul>
      <li><a href="{{ url_for('code_status') }}">Code Status</a></li>
      <li><a href="{{ url_for('bot_status') }}">Bot Status</a></li>
    </ul>
    <p><a href="{{ url_for('logout') }}">Logout</a></p>
  </body>
</html>
"""

status_page = """
<!doctype html>
<html>
  <head>
    <title>{{ title }}</title>
  </head>
  <body>
    <h2>{{ title }}</h2>
    <p>{{ message }}</p>
    <p><a href="{{ url_for('dashboard') }}">Back to Dashboard</a></p>
  </body>
</html>
"""

@app.route("/")
def home():
    return "Welcome to the website!"

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        key = request.form.get("key")
        # Validate the key from the shared SQLite database.
        conn = sqlite3.connect("keys.db")
        c = conn.cursor()
        c.execute("SELECT * FROM keys WHERE key = ?", (key,))
        result = c.fetchone()
        conn.close()
        if result is None:
            error = "Invalid key."
        else:
            session["logged_in"] = True
            session["key"] = key
            return redirect(url_for("dashboard"))
    return render_template_string(login_page, error=error)

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template_string(dashboard_page, key=session.get("key"))

@app.route("/code_status")
def code_status():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template_string(status_page, title="Code Status", message="The code is running normally.")

@app.route("/bot_status")
def bot_status():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template_string(status_page, title="Bot Status", message="The bot is online and operational.")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
