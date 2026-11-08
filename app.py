import os
from slugify import slugify
from flask import Flask, render_template

app = Flask(__name__)

def read_articles():
    articles = os.listdir("articles")
    slug_articles = {}

    for article in articles:
        slug = slugify(article)
        slug_articles[slug] = article
    return slug_articles


@app.route("/")
def blog():
    articles = read_articles()
    return render_template("blog.html", articles=articles)


@app.route("/blog/<slug>")
def article(slug):
    return render_template("article.html", slug=slug)



if __name__ == "__main__":
    app.run(debug=True)