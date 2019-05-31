from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "app.sqlite")

CORS(app)
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    pic_url = db.Column(db.String(), nullable= False)
    username = db.Column(db.String(), nullable= False)
    description = db.Column(db.String(420), nullable= True)

    def __init__(self, pic_url, username, description):
        self.pic_url = pic_url
        self.username = username
        self. description = description