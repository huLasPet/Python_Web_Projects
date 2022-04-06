# TODO:
#   1. replace .csv with a SQL DB
#   2. get or post data via API calls as well


from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, URLField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy

import csv

app = Flask(__name__)
#app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
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
    opens = StringField('Opening time', validators=[DataRequired()])
    closes = StringField('Closing time', validators=[DataRequired()])
    coffee = SelectField('Coffee rating', validators=[DataRequired()],
                         choices=["☕", 2 * "☕", 3 * "☕", 4 * "☕", 5 * "☕"])
    wifi = SelectField('Wifi', validators=[DataRequired()], choices=["✘", "💪", 2 * "💪", 3 * "💪", 4 * "💪", 5 * "💪"])
    power = SelectField('Power', validators=[DataRequired()],
                        choices=["✘", "🔌", 2 * "🔌", 3 * "🔌", 4 * "🔌", 5 * "🔌"])
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
    return render_template('cafes.html', cafes=Cafe.query.all())#list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)


