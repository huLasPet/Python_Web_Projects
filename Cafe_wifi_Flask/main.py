import sqlalchemy
from flask import Flask, render_template, jsonify, request, redirect, url_for
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
    """The DB to be used."""
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
    """The form to use when adding or editing Cafes."""
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField('Location - Google Maps link', validators=[DataRequired(), URL()])
    location = StringField('Location name', validators=[DataRequired()])
    img_url = StringField('Picture of the cafe', validators=[DataRequired(), URL()])
    seats = StringField('# of seats', validators=[DataRequired()])
    has_toilet = SelectField('Can use toilet', validators=[DataRequired()], choices=["True", "False"])
    has_wifi = SelectField('Can use Wi-Fi', validators=[DataRequired()], choices=["True", "False"])
    has_sockets = SelectField('Can charge device', validators=[DataRequired()], choices=["True", "False"])
    coffee_price = StringField('Coffee price', validators=[DataRequired()])
    can_take_calls = SelectField('Can take calls', validators=[DataRequired()], choices=["True", "False"])
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
        cafe_to_add = Cafe(can_take_calls=bool(form.can_take_calls.data),
                           coffee_price=form.coffee_price.data,
                           has_sockets=bool(form.has_sockets.data),
                           has_toilet=bool(form.has_toilet.data),
                           has_wifi=bool(form.has_wifi.data),
                           img_url=form.img_url.data,
                           location=form.location.data,
                           map_url=form.map_url.data,
                           name=form.name.data,
                           seats=form.seats.data)
        try:
            db_sqlalchemy.session.add(cafe_to_add)
            db_sqlalchemy.session.commit()
            return redirect(url_for('cafes'))
        except sqlalchemy.exc.IntegrityError:
            return jsonify(respnse={"error": "Record already exists"})
    return render_template('add.html', form=form, submitted=False)


@app.route("/delete/<cafe_id>")
def delete_cafe(cafe_id):
    """Delete a Cafe via the site."""
    cafe_to_delete = Cafe.query.get(cafe_id)
    db_sqlalchemy.session.delete(cafe_to_delete)
    db_sqlalchemy.session.commit()
    return redirect(url_for('cafes'))


@app.route("/edit/<cafe_id>", methods=["GET", "POST"])
def edit_cafe(cafe_id):
    """Edit a Cafe via the form on the site."""
    cafe_to_update = Cafe.query.get(cafe_id)
    form = CafeForm(can_take_calls=cafe_to_update.can_take_calls,
                    coffee_price=cafe_to_update.coffee_price,
                    has_sockets=cafe_to_update.has_sockets,
                    has_toilet=cafe_to_update.has_toilet,
                    has_wifi=cafe_to_update.has_wifi,
                    img_url=cafe_to_update.img_url,
                    location=cafe_to_update.map_url,
                    map_url=cafe_to_update.map_url,
                    name=cafe_to_update.name,
                    seats=cafe_to_update.seats)
    if form.validate_on_submit():
        try:
            cafe_to_update.can_take_calls = bool(form.can_take_calls.data)
            cafe_to_update.coffee_price = form.coffee_price.data
            cafe_to_update.has_sockets = bool(form.has_sockets.data)
            cafe_to_update.has_toilet = bool(form.has_toilet.data)
            cafe_to_update.has_wifi = bool(form.has_wifi.data)
            cafe_to_update.img_url = form.img_url.data
            cafe_to_update.map_url = form.location.data
            cafe_to_update.map_url = form.map_url.data
            cafe_to_update.name = form.name.data
            cafe_to_update.seats = form.seats.data
            db_sqlalchemy.session.commit()
            return redirect(url_for('cafes'))
        except sqlalchemy.exc.IntegrityError:
            return jsonify(respnse={"error": "Record already exists"})
    return render_template('edit.html', form=form, submitted=False)



@app.route('/cafes')
def cafes():
    """List all cafes on the site."""
    return render_template('cafes.html', cafes=Cafe.query.all())


@app.route("/api/all", methods=["GET"])
def all_cafes():
    """Get all Cafes from the DB via an API call - for documentation check the index page."""
    all_cafes_list = []
    cafe_dictionary = Cafe.query.all()
    for cafe in cafe_dictionary:
        temp = cafe.__dict__
        del temp["_sa_instance_state"]
        all_cafes_list.append(temp)
    return jsonify(cafes=all_cafes_list)


@app.route("/api/add", methods=["POST"])
def api_add_cafe():
    """Add a Cafe to the DB via an API call - for documentation check the index page."""
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


@app.route("/api/delete", methods=["POST"])
def api_delete_cafe():
    """Delete a Cafe from the DB via an API call - for documentation check the index page."""
    cafe_id = request.args.get("id")
    cafe_to_delete = Cafe.query.get(cafe_id)
    try:
        db_sqlalchemy.session.delete(cafe_to_delete)
        db_sqlalchemy.session.commit()
        return jsonify(respnse={"success": "Record deleted"})
    except sqlalchemy.orm.exc.UnmappedInstanceError:
        return jsonify(respnse={"error": "Invalid ID"})


@app.route("/api/edit", methods=["POST"])
def api_edit_cafe():
    """Edit a Cafe in the DB via an API call - for documentation check the index page."""
    cafe_id = request.args.get("id")
    cafe_to_edit = Cafe.query.get(cafe_id)
    try:
        cafe_to_edit.can_take_calls = bool(int(request.args.get("can_take_calls")))
        cafe_to_edit.coffee_price = request.args.get("coffee_price")
        cafe_to_edit.has_sockets = bool(int(request.args.get("has_sockets")))
        cafe_to_edit.has_toilet = bool(int(request.args.get("has_toilet")))
        cafe_to_edit.has_wifi = bool(int(request.args.get("has_wifi")))
        cafe_to_edit.img_url = request.args.get("img_url")
        cafe_to_edit.map_url = request.args.get("location")
        cafe_to_edit.map_url = request.args.get("map_url")
        cafe_to_edit.name = request.args.get("name")
        cafe_to_edit.seats = request.args.get("seats")
        db_sqlalchemy.session.commit()
        return jsonify(respnse={"success": "Record edited"})
    except AttributeError:
        return jsonify(respnse={"error": "Invalid data"})


if __name__ == '__main__':
    app.run(host="192.168.0.24", port=5000, threaded=True, debug=True)
