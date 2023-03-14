from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
Bootstrap(app)
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    year = db.Column(db.Integer)
    description = db.Column(db.Text)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.Text)
    img_url = db.Column(db.String(255))


@app.route("/")
def home():
    all_movies = db.session.query(Movie).order_by(Movie.rating.desc()).all()
    return render_template("index.html", movies=all_movies)


@app.route("/add", methods=['POST', "GET"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        new_movie = Movie(
            title=request.form['movie_title'],
            year=request.form['movie_year'],
            description=request.form['movie_description'],
            rating=request.form['movie_rating'],
            ranking=request.form['movie_ranking'],
            review=request.form['movie_review'],
            img_url=request.form['movie_img_url']
        )

        db.session.add(new_movie)
        db.session.commit()
        return redirect("/")


@app.route("/edit", methods=['POST', "GET"])
def edit():
    current_movie = Movie.query.get(request.args["id"])
    if request.method == "GET":
        return render_template("edit.html", movie=current_movie)
    else:
        movie_rating = request.form['movie_rating']
        current_movie.rating = movie_rating
        movie_review = request.form['movie_review']
        current_movie.review = movie_review
        db.session.commit()
        return redirect("/")


@app.route("/delete", methods=["GET"])
def delete():
    current_movie = Movie.query.get(request.args["id"])
    db.session.delete(current_movie)
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)

    #
    # with app.app_context():
    #     db.create_all()
    #
    #     new_movie = Movie(
    #         title="Navalny",
    #         year=2022,
    #         description="About an investigation of poisoning of Aleksey Navalny",
    #         rating=9.3,
    #         ranking=10,
    #         review="Oscar 2023",
    #         img_url="https://www.amherst.edu/system/files/styles/original/private/navalny%2520square.jpeg"
    #     )
    #
    #     db.session.add(new_movie)
    #     db.session.commit()


    # new_movie = Movie(
    #     title="Phone Booth",
    #     year=2002,
    #     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
    #     rating=7.3,
    #     ranking=10,
    #     review="My favourite character was the caller.",
    #     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
    # )
    # db.session.add(new_movie)
    # db.session.commit()
