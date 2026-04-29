from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///places.db'
db = SQLAlchemy(app)

# model
class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    order = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)

# HOME PAGE
@app.route("/")
def index():
    return render_template("index.html")

# ADD NEW PLACE PAGE
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        order = request.form["order"]
        rating = request.form["rating"]
        location = request.form["location"]

        new_place = Place(
            name=name,
            order=order,
            rating=float(rating),
            location=location
        )

        try:
            db.session.add(new_place)
            db.session.commit()
            return redirect("/map")
        except:
            return "Error adding place"

    return render_template("add.html")

# MAP (GALLERY) PAGE
@app.route("/map")
def map():
    places = Place.query.all()
    return render_template("map.html", places=places)

# RUN APP
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)