from flask import Flask, request, render_template_string, session, redirect

app = Flask(__name__)
app.secret_key = "dev-secret"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username", "")
        # Insecure login: accepts anything
        session["user"] = username
        return redirect("/dashboard")

    return """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Leaky Login</title>
<style>
body {
  font-family: Arial, sans-serif;
  background: #0f1226;
  color: #e7eaf6;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  margin: 0;
}
.container {
  background: #161a3a;
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 10px;
  padding: 30px;
  width: 320px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.5);
}
h2 { margin-top: 0; color: #7c8aff; }
label { display: block; margin: 10px 0 5px; font-weight: bold; }
input {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #333;
  background: #111530;
  color: #e7eaf6;
}
button {
  width: 100%;
  margin-top: 15px;
  padding: 10px;
  background: linear-gradient(135deg, #7c8aff, #b38cff);
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  color: #0f1226;
}
button:hover { opacity: 0.9; }
</style>
</head>
<body>
  <div class="container">
    <h2>Leaky Login</h2>
    <p>Login with any username. Can you find the flag?</p>
    <form method="POST">
      <label>Username</label>
      <input type="text" name="username" placeholder="username" required>
      <label>Password</label>
      <input type="password" name="password" placeholder="password">
      <button type="submit">Login</button>
    </form>
  </div>
</body>
</html>
    """

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    with open("flag.txt", "r") as f:
        flag = f.read().strip()

    # ⚠️ vulnerable: username goes straight into template
    template = f"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Dashboard</title>
<style>
body {{
  font-family: Arial, sans-serif;
  background: #0f1226;
  color: #e7eaf6;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  margin: 0;
}}
.container {{
  background: #161a3a;
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 10px;
  padding: 30px;
  width: 400px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.5);
}}
h2 {{ margin-top: 0; color: #7c8aff; }}
pre {{
  background: #0b0f28;
  padding: 10px;
  border-radius: 6px;
  overflow-x: auto;
}}
a {{ color: #7c8aff; text-decoration: none; }}
</style>
</head>
<body>
  <div class="container">
    <h2>Dashboard</h2>
    <p>Hello, {session['user']}</p>
    <p>Flag:
      {{% if session['user'] == 'admin' %}}{{{{ flag }}}}{{% else %}}Only admin can see the flag{{% endif %}}
    </p>
    <p><a href="/">Back</a></p>
  </div>
</body>
</html>
    """

    return render_template_string(template, flag=flag, session=session)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

