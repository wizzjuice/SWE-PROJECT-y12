from flask import Flask, render_template, request, redirect, url_for
import signin

app = Flask(__name__)

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/validate_signup', methods=["POST"])
def validate_signup():
    email = request.form.get("email")
    password = request.form.get("password")
    username = request.form.get("username")

    signin.add_accounts(email, password, username)

    return redirect(url_for("signup"))

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/validate_login', methods=["POST"])
def validate_login():
    username = request.form.get("username")
    password = request.form.get("password")

    signin.check_login(username, password)

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)