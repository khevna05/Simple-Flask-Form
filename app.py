from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

template_dir = os.path.abspath("templates")  # Corrected the template folder name
app = Flask(__name__, template_folder=template_dir)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        age = request.form["age"]
        gender = request.form["gender"]
        address = request.form["address"]

        new_user = User(name=name, email=email, phone=phone, age=age, gender=gender, address=address)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("user")) 

    return render_template("index.html")  

@app.route("/user")
def user():
    users = User.query.all()
    return render_template("user.html", users=users)

@app.route("/delete/<int:id>")
def delete(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('user'))

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    user = User.query.get(id)
    if request.method == "POST":
        user.name = request.form["name"]
        user.email = request.form["email"]
        user.phone = request.form["phone"]
        user.age = request.form["age"]
        user.gender = request.form["gender"]
        user.address = request.form["address"]
        db.session.commit()
        return redirect(url_for("user"))

    return render_template("update.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)
