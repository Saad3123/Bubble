from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from databaseclass import DatabaseConnector

app = Flask(__name__)
CORS(app)

# Initialize your DatabaseConnector
db_connector = DatabaseConnector(
    host='127.0.0.1', 
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

@app.route('/homePage')
def homepage():
    return send_from_directory('htmlCode', 'homePage.html')




# user functions
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

@app.route('/user_return_info', methods=['POST'])
def user_return_info():
    email = request.form.get('email')
    result = db_connector.user_return_info(email)
    return jsonify({"success": result})  # Placeholder response


# Chatroom functions
@app.route('/chatrooms_list', methods=['POST'])
def chatrooms_list():
    result = db_connector.chatrooms_list()
    formatted_rooms = [{'id': room[0], 'name': room[1]} for room in result]
    return jsonify({"success": formatted_rooms})  # Placeholder response

@app.route('/chatrooms_delete', methods=['POST'])
def chatrooms_delete():
    chatroomid = request.form.get('chatroomid')
    result = db_connector.chatrooms_delete(chatroomid)
    return jsonify({"success": result})  # Placeholder response

@app.route('/chatrooms_create', methods=['POST'])
def chatrooms_create():
    name = request.form.get('name')
    password = request.form.get('password')
    if len(password) == 0:
        result = db_connector.chatrooms_create(name)
    else:
        result = db_connector.chatrooms_create(name, password)
    return jsonify({"success": result})  # Placeholder response

@app.route('/chatrooms_password_status', methods=['POST'])
def chatrooms_password_status():
    chatroomid = request.form.get('chatroomid')
    result = db_connector.chatrooms_password_status(chatroomid)
    return jsonify({"success": result})  # Placeholder response

@app.route('/chatrooms_join', methods=['POST'])
def chatrooms_join():
    chatroomid = request.form.get('chatroomid')
    password = request.form.get('password')
    if password == 'null':
        password = None
    print(request.form.get('password'))
    result = db_connector.chatrooms_join(chatroomid, password)
    return jsonify({"success": result})  # Placeholder response

if __name__ == '__main__':
    app.run(debug=True)
