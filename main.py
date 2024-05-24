from flask import Flask, request, jsonify
from config import app, db
from model import User

@app.route("/login", methods = ['GET', 'POST'])
def login():
    users = User.query.all()
    jsonification = [User.to_json() for u in users]
    return jsonify(jsonification)
    

if __name__ == '__main__':
    app.run(debug=True)