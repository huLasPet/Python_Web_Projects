# TODO:
#   2. Fix /add to work with the DB, create other API calls as well
#   3. Fix the new cafe form


from flask import Flask, render_template
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
    image_url = StringField('Picture of the cafe', validators=[DataRequired()])
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
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', 'a', newline='', encoding="UTF-8") as csv_file:
            csv_file.write(
                f"\n{form.cafe.data},{form.location.data},{form.opens.data},{form.closes.data},{form.coffee.data},{form.wifi.data},{form.power.data}")
        return render_template('add.html', form=form, submitted=True)
    return render_template('add.html', form=form, submitted=False)


@app.route('/cafes')
def cafes():
    return render_template('cafes.html', cafes=Cafe.query.all())


if __name__ == '__main__':
    app.run(debug=True)


