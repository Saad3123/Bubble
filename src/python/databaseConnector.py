from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import threading
from flask_socketio import SocketIO, emit, join_room, leave_room

from databaseclass import DatabaseConnector

app = Flask(__name__)
CORS(app, origins=["http://localhost:3002", "http://127.0.0.1:3002"])
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:3002", "http://127.0.0.1:3002"])

# Initialize your DatabaseConnector
db_connector = DatabaseConnector(
    host='127.0.0.1', 
    username='csci375team2', 
    password='sihj715gtdjx', 
    database='csci375team2_testdb_bubble'
)
db_connector.connect()

# Define a lock object to synchronize database access
db_lock = threading.Lock()

# Wrap database calls with the lock to ensure they are executed sequentially
def synchronized_database_call(func):
    def synchronized_call(*args, **kwargs):
        with db_lock:
            return func(*args, **kwargs)
    return synchronized_call

# Apply the synchronized_database_call decorator to database-related routes
db_connector.user_login = synchronized_database_call(db_connector.user_login)
db_connector.user_register = synchronized_database_call(db_connector.user_register)
db_connector.user_return_info = synchronized_database_call(db_connector.user_return_info)
db_connector.chatrooms_list = synchronized_database_call(db_connector.chatrooms_list)
db_connector.chatrooms_delete = synchronized_database_call(db_connector.chatrooms_delete)
db_connector.chatrooms_create = synchronized_database_call(db_connector.chatrooms_create)
db_connector.chatrooms_password_status = synchronized_database_call(db_connector.chatrooms_password_status)
db_connector.chatrooms_join = synchronized_database_call(db_connector.chatrooms_join)
db_connector.messages_send = synchronized_database_call(db_connector.messages_send)
db_connector.messages_list_in_chatroom = synchronized_database_call(db_connector.messages_list_in_chatroom)

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
    formatted_user_info = {'userid': result[0], 'email': result[1], 'username': result[2], 'bio': result[3]}
    return jsonify({"success": formatted_user_info})  # Placeholder response

# Chatroom functions
@app.route('/chatrooms_list', methods=['POST'])
def chatrooms_list():
    result = db_connector.chatrooms_list()
    formatted_rooms = [{'chatroomid': room[0], 'name': room[1]} for room in result]
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

@app.route('/messages_send', methods=['POST'])
def messages_send():
    chatroomid = request.form.get('chatroomid')
    userid = request.form.get('userid')
    message = request.form.get('message')
    
    # Save the message to the database
    result = db_connector.messages_send(userid, chatroomid, message)
        
    return jsonify({"success": result})

@app.route('/messages_list', methods=['POST'])
def messages_list():
    chatroomid = request.form.get('chatroomid')
    result = db_connector.messages_list_in_chatroom(chatroomid)
    formatted_messages = [{'messageid': message[0], 'userid': message[1], 'username': message[2], 'time': message[3], 'text': message[4]} for message in result]
    return jsonify({"success": formatted_messages})  # Placeholder response

@app.route('/messages_delete', methods=['POST'])
def messages_delete():
    messageid = request.form.get('messageid')
    userid = request.form.get('userid')
    result = db_connector.messages_delete(userid, messageid)
    return jsonify({"success": result})  # Placeholder response

@app.route('/messages_edit', methods=['POST'])
def messages_edit():
    userid = request.form.get('userid')
    messageid = request.form.get('messageid')
    updatedMessage = request.form.get('updatedmessage')
    result = db_connector.messages_edit(userid, messageid, updatedMessage)
    return jsonify({"success": result})  # Placeholder response

@socketio.on('connect')
def handle_connect():
    print('Client connected')

# Define a room when a user joins a chatroom
@socketio.on('join_room')
def on_join(data):
    chatroomid = data['chatroomid']
    join_room(chatroomid)
    print(f"A user joined chatroom {chatroomid}")

# Define a room when a user leaves a chatroom
@socketio.on('leave_room')
def on_leave(data):
    chatroomid = data['chatroomid']
    leave_room(chatroomid)
    print(f"A user left chatroom {chatroomid}")

# Handle sending messages
@socketio.on('server_update_chatroom')
def handle_message(data):
    chatroomid = data['chatroomid']
    emit('client_update_chatroom', {'chatroomid': chatroomid}, room=chatroomid)

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
