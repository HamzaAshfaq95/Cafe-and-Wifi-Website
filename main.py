from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, MappedColumn, DeclarativeBase
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
db.init_app(app)

Bootstrap5(app)

def url_checker(form, field):
   if not field.data.startswith(("http://", "https://")):
       raise ValidationError("Write a correct URL (starting from http)")
class CafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    map_url = StringField("Map URL")
    img_url = StringField("Image URL", validators=[url_checker])
    location = StringField("Location")
    has_sockets = BooleanField("Has Sockets")
    has_toilet = BooleanField("Has Toilet")
    has_wifi = BooleanField("Has Wifi")
    can_take_calls = BooleanField("Can Take Calls")
    seats = StringField("Seats")
    coffee_price = StringField("Price")
    submit = SubmitField("Submit")

class ContactForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    number = StringField("Contact Number")
    submit = SubmitField("Done")

class Cafe(db.Model):
    id: Mapped[int] = MappedColumn(Integer, primary_key=True)
    name: Mapped[str] = MappedColumn(String(250), unique=True)
    map_url: Mapped[str] = MappedColumn(String(250))
    img_url: Mapped[str] = MappedColumn(String(250))
    location: Mapped[str] = MappedColumn(String(250))
    has_sockets: Mapped[bool] = MappedColumn(Boolean)
    has_toilet: Mapped[bool] = MappedColumn(Boolean)
    has_wifi: Mapped[bool] = MappedColumn(Boolean)
    can_take_calls: Mapped[bool] = MappedColumn(Boolean)
    seats: Mapped[str] = MappedColumn(String(250))
    coffee_price: Mapped[str] = MappedColumn(String(250))

def __repr__(self):
    return f"<Cafe {self.name}>"

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cafes")
def cafes():
    with app.app_context():
        result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
        all_cafes = result.scalars().all()
    return render_template("cafes.html", cafes=all_cafes)

@app.route("/add-cafe", methods=["POST", "GET"])
def add():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(name=form.name.data, map_url=form.map_url.data, img_url=form.img_url.data, location=form.location.data, has_sockets=form.has_sockets.data, has_toilet=form.has_toilet.data, has_wifi=form.has_wifi.data, can_take_calls=form.can_take_calls.data, seats=form.seats.data, coffee_price=form.coffee_price.data)
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("cafes"))
    return render_template("add.html", form=form)

@app.route("/contact", methods=["POST", "GET"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        number = form.number.data
        print(f"{name} having email: {email} and number: {number} has contacted you")
        return redirect(url_for("home"))
    return render_template("contact.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)