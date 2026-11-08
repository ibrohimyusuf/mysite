import os
from flask import Flask, render_template

app = Flask(__name__)
articles = os.listdir("articles")


@app.route("/")
def blog():
    return render_template("blog.html", articles=articles)


@app.route("/blog/<slug>")
def article(slug):
    return render_template("article.html", slug=slug)



if __name__ == "__main__":
    app.run(debug=True)