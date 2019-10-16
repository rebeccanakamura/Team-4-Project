# https://git.heroku.com/team4project2019october.git
# https://team4project2019october.herokuapp.com/

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://qkxwsxtzqarbil:71ea2fdf5ca277a6f1004142878a01b100160153c7e2bc796d67b8578209ac32@ec2-174-129-220-12.compute-1.amazonaws.com:5432/dcqtupk0oa2c1m"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///team4project.db"
# postgres://qkxwsxtzqarbil:71ea2fdf5ca277a6f1004142878a01b100160153c7e2bc796d67b8578209ac32@ec2-174-129-220-12.compute-1.amazonaws.com:5432/dcqtupk0oa2c1m

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(100))
    done = db.Column(db.Boolean)

    def __init__(self, logo, title, byline, headline, opening, text1, text2, pic1, pic2):
        self.logo = logo
        self.title = title
        self.byline = byline
        self.headline = headline
        self.opening = opening
        self.text1 = text1
        self.text2 = text2
        self.pic1 = pic1
        self.pic2 = pic2

class ProfileSchema(ma.Schema):
    class Meta: 
        fields = ("id", "logo", "title", "byline", "headline", "opening", "text1", "text2", "pic1", "pic2")

profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)

@app.route("/profiles", methods=["GET"])
def get_profiles():
    all_profiles = Profile.query.all()
    result = profiles_schema.dump(all_profiles)
    return jsonify(result)

@app.route("/profile", methods=["POST"])
def add_profile():
    logo = request.json["logo"]
    title = request.json["title"]
    byline = request.json["byline"]
    headline = request.json["headline"]
    opening = request.json["opening"]
    text1 = request.json["text1"]
    text2 = request.json["text2"]
    pic1 = request.json["pic1"]
    pic2 = request.json["pic2"]


    new_profile = Profile(logo, title, byline, headline, opening, text1, text2, pic1, pic2)
    db.session.add(new_profile)
    db.session.commit()

    created_profile = Profile.query.get(new_profile.id)
    return profile_schema.jsonify(created_profile)

@app.route("/profile/<id>", methods=["PUT"])
def update_profile(id):
    profile = Profile.query.get(id)

    profile.logo = request.json["logo"]
    profile.title = request.json["title"]
    profile.byline = request.json["byline"]
    profile.headline = request.json["headline"] 
    profile.opening = request.json["opening"]
    profile.text1 = request.json["text1"]
    profile.text2 = request.json["text2"]
    profile.pic1 = request.json["pic1"]
    profile.pic2 = request.json["pic2"]   

    db.session.commit()
    return profile_schema.jsonify(profile)

@app.route("/profile/<id>", methods=["DELETE"])
def delete_profile(id):
    profile = Profile.query.get(id)
    db.session.delete(profile)
    db.session.commit()

    return "RECORD DELETED"

if __name__ == "__main__":
    app.debug=True
    app.run()