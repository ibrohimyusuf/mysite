import hashlib

import os
from slugify import slugify
from articles import Article
from flask import (Flask, render_template, request, session, make_response, redirect)

app = Flask(__name__)
app.secret_key = "thisisverysecret"

users = {
    "admin": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}


articles = Article.all()


@app.get("/admin")
def admin_page():
    if "user" in session:
        return "Ur already authenticated"
    return render_template("login.html")

@app.get("/logout")
def logout():
    if "user" not in session:
       return "You can't log out without log in"
    del session["user"]
    return "Logged out"
    
    return message

@app.post("/admin")
def admin_login():
    username = request.form["username"]
    password = request.form["password"]

    if username not in users:
        return render_template("login.html", error="username/password incorrect")

    hashed = hashlib.sha256(password.encode()).hexdigest()

    if users[username] != hashed:
        return render_template("login.html", error="username/password incorrect")

    session["user"] = username

    return "You are now authenticated"

@app.route("/set-session")
def set_session():
    session["user_id"] = 1
    return "session set"

@app.route("/get-session")
def get_session():
    return f"user_id = {session['user_id']}"

@app.route("/first-time")
def first_time():
    if 'seen' not in request.cookies:
        response = make_response("You are new here")
        response.set_cookie('seen', '1')
        return response

    seen = int(request.cookies['seen'])
    response = make_response(f"I have seen you {seen} times")
    response.set_cookie('seen', str(seen+1))
    return response

@app.route("/")
def blog():
    articles = Article.all()
    return render_template("blog.html", articles=articles)


@app.route("/blog/<slug>")
def article(slug):
    article = articles[slug]
    return render_template("article.html", article=article)

@app.get("/publish")
def publish():
    if "user" not in session:
        return redirect("/admin")

    return render_template("publish.html")

@app.post("/publish")
def article_publish():
    title = request.form["title"]
    text = request.form["text"]

    with open(f"articles/{title}", "w") as f:
        f.write(f"{text}\n")
    return "successful"





if __name__ == "__main__":
    app.run(debug=True)