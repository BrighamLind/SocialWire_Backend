from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, "app.sqlite")

CORS(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    pic_url = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(420), nullable=True)

    def __init__(self, pic_url, username, description):
        self.pic_url = pic_url
        self.username = username
        self.description = description


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "pic_url", "username", "description")


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route("/add-user", methods=["POST"])
def add_user():
    pic_url = request.json["user-picture"]
    username = request.json["user-name"]
    description = request.json["description"]

    record = User(pic_url, username, description)
    db.session.add(record)
    db.session.commit()
    user = User.query.get(record.id)

    return user_schema.jsonify(user)


if __name__ == "__main__":
    app.debug = True
    app.run()
