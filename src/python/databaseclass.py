import mysql.connector

class DatabaseConnector:
    """
        @var
            host     - (string) location of the database server
            username - (string) username of the account on the database
            password - (string) password of the account
            database - (string) name of the database to connect to
    """
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None


    """
        @return
            - returns true on successful connection
            - returns false on failed connection
    """
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Connected to the database")
            return True
        except mysql.connector.Error as err:
            print("Error connecting to the database:", err)
            return False

    """
        disconnect from the database
    """
    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Disconnected from the database")

    """
        @var
            email    - (string) email of the account
            password - (string) password of the account

        @return
            - returns true on a successful login
            - returns false on a failed login
    """
    def user_login(self, email, password):
        query = "SELECT * FROM USERS WHERE email = %s AND password = %s"
        values = (email, password)
        
        try:
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            
            if result:
                print("email and password match found in the database")
                return True
            else:
                print("email and password do not match any records in the database")
                return False
        except mysql.connector.Error as err:
            print("Error checking credentials:", err)
            return False 
        
    """
        @var
            email    - (string) email for the registering account
            username - (string) username for the registering account
            password - (string) password for the registering account

        @return
            - returns true if account successfully registered
            - returns false if account can not be created
    """
    def user_register(self, email, username, password):
        # Check if email already exists
        query_check_email = "SELECT * FROM USERS WHERE email = %s"
        values_check_email = (email,)
        try:
            self.cursor.execute(query_check_email, values_check_email)
            existing_user = self.cursor.fetchone()
            if existing_user:
                print("Email already exists. Registration failed.")
                return False
        except mysql.connector.Error as err:
            print("Error checking email:", err)
            return False

        # Register new user
        query_register_user = "INSERT INTO USERS (email, username, password) VALUES (%s, %s, %s)"
        values_register_user = (email, username, password)
        try:
            self.cursor.execute(query_register_user, values_register_user)
            self.connection.commit()
            print("User registered successfully.")
            return True
        except mysql.connector.Error as err:
            print("Error registering user:", err)
            return False

    """
        @var
            email    - (string) email for the account to get info for

        @return
            - returns a list on success [uid,email,username,bio]
            - returns false on a failure
    """
    def user_return_info(self, email):
        query = "SELECT userid,email,username,bio FROM USERS WHERE email = %s"
        values = (email,)
        
        try:
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            
            if result:
                print("fetched user info")
                return result
            else:
                print("cannot fetch user info (should never be reached, \
                      this should only be called after a email has been validated)")
                return False
        except mysql.connector.Error as err:
            print("Error fetching user info:", err)
            return False 

    """
        @var
            userid    - (string) userid for the account to delete

        @return
            - returns true if account is deleted
            - returns false if account could not be delete
    """
    def user_delete(self, userid):
        # Check if user exists
        query_check_user = "SELECT * FROM USERS WHERE userid = %s"
        values_check_user = (userid,)
        try:
            self.cursor.execute(query_check_user, values_check_user)
            existing_user = self.cursor.fetchone()
            if not existing_user:
                print("User does not exist. Deletion failed.")
                return False
        except mysql.connector.Error as err:
            print("Error checking user:", err)
            return False

        # Delete user
        query_delete_user = "DELETE FROM USERS WHERE userid = %s"
        try:
            self.cursor.execute(query_delete_user, (userid,))
            self.connection.commit()
            print("User deleted successfully.")
            return True
        except mysql.connector.Error as err:
            print("Error deleting user:", err)
            return False

    """
        @var
            userid    - (string) userid for the account bio to update
            new_bio   - (string) new bio for the account

        @return
            - returns true if bio is updated
            - returns false if bios could not be updated
    """
    def user_update_bio(self, userid, new_bio):
        # Update user bio
        query_update_bio = "UPDATE USERS SET bio = %s WHERE userid = %s"
        values_update_bio = (new_bio, userid)
        try:
            self.cursor.execute(query_update_bio, values_update_bio)
            self.connection.commit()
            print("User bio updated successfully.")
            return True
        except mysql.connector.Error as err:
            print("Error updating user bio:", err)
            return False

    """
        @var
            name     - (string) name for the chatroom
            password - (string) new bio for the account or default none for no password

        @return
            - returns true if chatroom was created
            - retuns false if not created
    """
    def chatrooms_create(self, name, password=None):
        # Check if chatroom name already exists
        query_check_chatroom = "SELECT * FROM CHATROOMS WHERE name = %s"
        values_check_chatroom = (name,)
        try:
            self.cursor.execute(query_check_chatroom, values_check_chatroom)
            existing_chatroom = self.cursor.fetchone()
            if existing_chatroom:
                print("Chatroom name already exists. Creation failed.")
                return False
        except mysql.connector.Error as err:
            print("Error checking chatroom name:", err)
            return False

        # Create new chatroom
        query_create_chatroom = "INSERT INTO CHATROOMS (name, password) VALUES (%s, %s)"
        values_create_chatroom = (name, password)
        try:
            self.cursor.execute(query_create_chatroom, values_create_chatroom)
            self.connection.commit()
            print("Chatroom created successfully.")
            return True
        except mysql.connector.Error as err:
            print("Error creating chatroom:", err)
            return False

    """
        @var
            chatroomid - (string) chatroom id to be deleted
        @return
            - returns true if chatroom was deleted
            - retuns false if not deleted
    """
    def chatrooms_delete(self, chatroomid):
        try:
            # Delete messages associated with the chatroom
            delete_messages_query = "DELETE FROM MESSAGES WHERE chatroomid = %s"
            self.cursor.execute(delete_messages_query, (chatroomid,))
            
            # Delete the chatroom
            delete_chatroom_query = "DELETE FROM CHATROOMS WHERE chatroomid = %s"
            self.cursor.execute(delete_chatroom_query, (chatroomid,))
            
            # Commit the changes
            self.connection.commit()
            
            print("Chatroom and associated messages deleted successfully.")
            return True
        except mysql.connector.Error as err:
            print("Error deleting chatroom:", err)
            return False

    """
        @return
            - returns a list of all chatrooms [(charoomid1,name1),(chatroomid2,name2), ...]
            - retuns false if not deleted
    """
    def chatrooms_list(self):
        query = "SELECT chatroomid, name FROM CHATROOMS ORDER BY name ASC"
        try:
            self.cursor.execute(query)
            chatrooms = self.cursor.fetchall()
            print("List of chatrooms:")
            for chatroom in chatrooms:
                print(chatroom)
            return chatrooms
        except mysql.connector.Error as err:
            print("Error listing chatrooms:", err)
            return None

    """
        @var
            chatroomid - (string) chatroom to join
            password   - (string) password of the chatroom you are trying to join
        @return
            - returns true if you are allowed to join
            - returns false otherwise
    """
    def chatrooms_join(self, chatroomid, password=None):
        if password:
            query = "SELECT * FROM CHATROOMS WHERE chatroomid = %s AND password = %s"
            values = (chatroomid, password)
        else:
            query = "SELECT * FROM CHATROOMS WHERE chatroomid = %s AND password IS NULL"
            values = (chatroomid,)
        try:
            self.cursor.execute(query, values)
            chatroom = self.cursor.fetchone()
            if chatroom:
                print("Successfully joined the chatroom.")
                return chatroom
            else:
                print("Failed to join the chatroom. Invalid chatroomid or password.")
                return None
        except mysql.connector.Error as err:
            print("Error joining chatroom:", err)
            return None

    """
        @var
            chatroomid - (string) chatroomid to check
        @return
            - returns True is chatroom has password
            - return False if chatroom does not have a password
    """
    def chatrooms_password_status(self, chatroomid):
        query = "SELECT IFNULL(password, 'No password') AS password_status FROM CHATROOMS WHERE chatroomid = %s"
        values = (chatroomid,)
        
        try:
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            if result:
                if result[0] == 'No password':
                    return False
                else:
                    return True
            else:
                return "Chatroom not found"
        except mysql.connector.Error as err:
            print("Error checking chatroom password status:", err)
            return None

    """
        @var
            userid     - (string) user sending the message
            chatroomid - (string) chatroom the message is sent into
            message    - (string) message content
        @return
            - returns true if message successfully sent
            - returns false otherwise
    """
    def messages_send(self, userid, chatroomid, message):
        query = "INSERT INTO MESSAGES (chatroomid, userid, message) VALUES (%s, %s, %s)"
        values = (chatroomid, userid, message)
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Message sent successfully.")
            return True
        except mysql.connector.Error as err:
            print("Error sending message:", err)
            return False

    """
        @var
            userid     - (string) user that is trying to delete the message
            chatroomid - (string) chatroom the message is in
            messageid  - (string) messageid of the messaage to be deleted
        @return
            - returns true if message successfully deleted
            - returns false otherwise
    """
    def messages_delete(self, userid, chatroomid, messageid):
        query = "DELETE FROM MESSAGES WHERE chatroomid = %s AND userid = %s AND messageid = %s"
        values = (chatroomid, userid, messageid)
        try:
            # Check if the user attempting to delete the message is the same as the one who sent it
            check_query = "SELECT * FROM MESSAGES WHERE chatroomid = %s AND userid = %s AND messageid = %s"
            check_values = (chatroomid, userid, messageid)
            self.cursor.execute(check_query, check_values)
            existing_message = self.cursor.fetchone()
            if not existing_message:
                print("Message not found or you don't have permission to delete it.")
                return False

            # If the user is authorized, proceed with deleting the message
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Message deleted successfully.")
            return True
        except mysql.connector.Error as err:
            print("Error deleting message:", err)
            return False

    """
        @var
            userid      - (string) user that is trying to edit the message
            chatroomid  - (string) chatroom the message is in
            new_message - (string) new message string
        @return
            - returns true if message successfully deleted
            - returns false otherwise
    """
    def messages_edit(self, userid, chatroomid, messageid, new_message):
        query = "UPDATE MESSAGES SET message = %s WHERE chatroomid = %s AND userid = %s AND messageid = %s"
        values = (new_message, chatroomid, userid, messageid)
        try:
            # Check if the user attempting to edit the message is the same as the one who sent it
            check_query = "SELECT * FROM MESSAGES WHERE chatroomid = %s AND userid = %s AND messageid = %s"
            check_values = (chatroomid, userid, messageid)
            self.cursor.execute(check_query, check_values)
            existing_message = self.cursor.fetchone()
            if not existing_message:
                print("Message not found or you don't have permission to edit it.")
                return False

            # If the user is authorized, proceed with editing the message
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Message edited successfully.")
            return True
        except mysql.connector.Error as err:
            print("Error editing message:", err)
            return False

    """
        @var
            chatroomid - (string) chatroom of messages to acquire
            limit      - (string) how many messages you want to acquire
                         if not specified all messages will be retrieved
        @return
            - returns true if message successfully deleted
            - returns false otherwise
    """
    def messages_list_in_chatroom(self, chatroomid, limit=None):
        query = "SELECT messageid,USERS.userid,username,time,message FROM MESSAGES JOIN USERS WHERE chatroomid = %s AND USERS.userid = MESSAGES.userid ORDER BY time DESC"
        if limit is not None:
            query += " LIMIT %s"
            values = (chatroomid, limit)
        else:
            values = (chatroomid,)

        try:
            self.cursor.execute(query, values)
            messages = self.cursor.fetchall()
            print("Messages in chatroom (from newest to oldest):")
            for message in messages:
                print(message)
            return messages
        except mysql.connector.Error as err:
            print("Error listing messages in chatroom:", err)
            return None