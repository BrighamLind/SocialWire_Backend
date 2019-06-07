from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
import os

app = Flask(__name__)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, "app.sqlite")

CORS(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String(420), nullable=True)

    def __init__(self, image, name, description):
        self.image = image
        self.name = name
        self.description = description


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "image", "name", "description")


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route("/add-user", methods=["POST"])
def add_user():
    image = request.json["image"]
    name = request.json["name"]
    description = request.json["description"]

    record = User(image, name, description)
    db.session.add(record)
    db.session.commit()
    user = User.query.get(record.id)

    return user_schema.jsonify(user)


@app.route("/turpentine", methods=["GET"])
def get_all_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users).data

    return jsonify(result)


@app.route("/turpentine/<id>", methods=["GET"])
def get_user_by_name(id):
    record = User.query.get(id)

    return user_schema.jsonify(record)


@app.route("/edit/<id>", methods=["PUT"])
def edit_user(id):
    record = User.query.get(id)

    new_image = request.json["image"]
    new_name = request.json["name"]
    new_description = request.json["description"]

    record.image = new_image
    record.name = new_name
    record.description = new_description

    db.session.commit()

    return user_schema.jsonify(record)


@app.route("/delete/<id>", methods=["DELETE"])
def delete_user(id):
    record = User.query.get(id)

    db.session.delete(record)
    db.session.commit()

    return f"Successfully deleted profile #{id}"


if __name__ == "__main__":
    app.debug = True
    app.run()
