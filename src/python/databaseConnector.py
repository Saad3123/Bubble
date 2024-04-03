from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from databaseclass import DatabaseConnector

app = Flask(__name__)
CORS(app)

# Initialize your DatabaseConnector
db_connector = DatabaseConnector(
    host='localhost', 
    username='csci375team2', 
    password='sihj715gtdjx', 
    database='csci375team2_testdb_bubble'
)
db_connector.connect()

@app.route('/index')
def login():
    return send_from_directory('htmlCode', 'index.html')

@app.route('/signUp')
def signup():
    return send_from_directory('htmlCode', 'signUp.html')

@app.route('/user_login', methods=['POST'])
def user_login():
    email = request.form.get('email')
    password = request.form.get('password')
    result = db_connector.user_login(email, password)
    return jsonify({"success": result})  # Placeholder response

@app.route('/user_register', methods=['POST'])
def user_register():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    result = db_connector.user_register(email, username, password)
    return jsonify({"success": result})  # Placeholder response

if __name__ == '__main__':
    app.run(debug=True)
