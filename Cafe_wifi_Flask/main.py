# TODO:
#   2. Fix /add to work with the DB, create other API calls as well

import sqlalchemy
from flask import Flask, render_template, jsonify, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap(app)
db_sqlalchemy = SQLAlchemy(app)


class Cafe(db_sqlalchemy.Model):
    id = db_sqlalchemy.Column(db_sqlalchemy.Integer, primary_key=True)
    name = db_sqlalchemy.Column(db_sqlalchemy.String(250), unique=True, nullable=False)
    map_url = db_sqlalchemy.Column(db_sqlalchemy.String(500), nullable=False)
    img_url = db_sqlalchemy.Column(db_sqlalchemy.String(500), nullable=False)
    location = db_sqlalchemy.Column(db_sqlalchemy.String(250), nullable=False)
    has_sockets = db_sqlalchemy.Column(db_sqlalchemy.Boolean, nullable=False)
    has_toilet = db_sqlalchemy.Column(db_sqlalchemy.Boolean, nullable=False)
    has_wifi = db_sqlalchemy.Column(db_sqlalchemy.Boolean, nullable=False)
    can_take_calls = db_sqlalchemy.Column(db_sqlalchemy.Boolean, nullable=False)
    seats = db_sqlalchemy.Column(db_sqlalchemy.String(250), nullable=False)
    coffee_price = db_sqlalchemy.Column(db_sqlalchemy.String(250), nullable=False)


# db_sqlalchemy.create_all()


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location - Google Maps link', validators=[DataRequired(), URL()])
    location_name = StringField('Location name', validators=[DataRequired()])
    image_url = StringField('Picture of the cafe', validators=[DataRequired(), URL()])
    seats = StringField('# of seats', validators=[DataRequired()])
    toilet = SelectField('Can use toilet', validators=[DataRequired()], choices=["True", "False"])
    wifi = SelectField('Can use Wi-Fi', validators=[DataRequired()], choices=["True", "False"])
    power = SelectField('Can charge device', validators=[DataRequired()], choices=["True", "False"])
    price = StringField('Coffee price', validators=[DataRequired()])
    calls = SelectField('Can take calls', validators=[DataRequired()], choices=["True", "False"])
    submit = SubmitField()


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    """Add a cafe to the site via a form."""
    form = CafeForm()
    if form.validate_on_submit():
        cafe_to_add = Cafe(can_take_calls=bool(form.calls.data),
                           coffee_price=form.price.data,
                           has_sockets=bool(form.power.data),
                           has_toilet=bool(form.toilet.data),
                           has_wifi=bool(form.wifi.data),
                           img_url=form.image_url.data,
                           location=form.location_name.data,
                           map_url=form.location.data,
                           name=form.cafe.data,
                           seats=form.seats.data)
        try:
            db_sqlalchemy.session.add(cafe_to_add)
            db_sqlalchemy.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return jsonify(respnse={"error": "Record already exists"})
        return render_template('add.html', form=form, submitted=True)
    return render_template('add.html', form=form, submitted=False)


@app.route('/cafes')
def cafes():
    """List all cafes on the site."""
    return render_template('cafes.html', cafes=Cafe.query.all())


@app.route("/api/all", methods=["GET"])
def all_cafes():
    """Creates a list of dictionaries from the cafes in the DB
    Creates a .json response from that list which returns the info for all cafes."""
    all_cafes_list = []
    cafe_dictionary = Cafe.query.all()
    for cafe in cafe_dictionary:
        temp = cafe.__dict__
        del temp["_sa_instance_state"]
        all_cafes_list.append(temp)
    return jsonify(cafes=all_cafes_list)


@app.route("/api/add", methods=["POST"])
def api_add_cafe():
    """/api/add?*args where the args are the entries below separated by &"""
    cafe_to_add = Cafe(can_take_calls=bool(int(request.args.get("can_take_calls"))),
                       coffee_price=request.args.get("coffee_price"),
                       has_sockets=bool(int(request.args.get("has_sockets"))),
                       has_toilet=bool(int(request.args.get("has_toilet"))),
                       has_wifi=bool(int(request.args.get("has_wifi"))),
                       img_url=request.args.get("img_url"),
                       location=request.args.get("location"),
                       map_url=request.args.get("map_url"),
                       name=request.args.get("name"),
                       seats=request.args.get("seats"))
    try:
        db_sqlalchemy.session.add(cafe_to_add)
        db_sqlalchemy.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return jsonify(respnse={"error": "Record already exists"})
    return jsonify(respnse={"success": "Cafe added to the DB"})


if __name__ == '__main__':
    app.run(debug=True)
