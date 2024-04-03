from flask import Flask, render_template, request, jsonify
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user_login', methods=['POST'])
def user_login():
    email = request.form.get('email')
    password = request.form.get('password')
    result = db_connector.user_login(email, password)
    print(result)
    return jsonify({"success": result})

if __name__ == '__main__':
    app.run(debug=True)