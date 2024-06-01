from flask import request, jsonify
from config import app, db
from model import User
from flask_migrate import Migrate
from sqlalchemy import select
import hashlib


migrate = Migrate(app, db)

@app.route("/", methods = ['GET', 'POST'])
def start():
    users = User.query.all()
    jsonification = [u.to_json() for u in users]
    return jsonify(jsonification)

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    secret = "secretkey"
    name = request.json.get('name')
    email = request.json.get('email')    
    password = request.json.get('password')
    password_confirmation = request.json.get('password')

    if password != password_confirmation:
        return jsonify({'error': 'Passwords do not match'}), 400

    row = db.session.execute(select(User).where(User.email == email)).first()
    if row:
        return jsonify({"message": "Email already exists"}), 400
    
    m = hashlib.sha256()
    m.update(str.encode(password + secret))

    newsign = User(name=name, email=email, password=m.hexdigest())
    try:
         db.session.add(newsign)
         db.session.commit()
    except Exception as e:
         return jsonify({"message": str(e)}), 400

    return jsonify({"message": "User created!"}), 201

@app.route("/login", methods = ['POST'])
def login():
    input_email = request.json.get('email')
    input_password = request.json.get('password')
    
    row = db.session.execute(select(User).where(User.email == input_email)).first()
    if row is None or len(row) == 0:
        return jsonify({"message": "User not found"}), 404

    user = row[0]

    m = hashlib.sha256()
    secret = input_password + "secretkey"
    m.update(str.encode(secret))
    m = m.hexdigest()

    if user.password != m:
        return jsonify({"message": "Wrong password"}), 400

    
    return jsonify({"message": "logged in!"}), 201


if __name__ == "__main__":
    app.run()
