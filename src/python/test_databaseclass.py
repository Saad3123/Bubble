import unittest
from databaseclass import DatabaseConnector

class TestDatabaseConnector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_connector = DatabaseConnector(
            host='localhost',
            username='csci375team2',
            password='sihj715gtdjx',
            database='csci375team2_unittesting_bubble'
        )
        cls.db_connector.connect()

    @classmethod
    def tearDownClass(cls):
        cls.db_connector.disconnect()

    def setUp(self):
        # Create necessary users, chatrooms, and messages for testing
        # User for testing user_register_and_return_info
        self.user_email = "test_user@example.com"
        self.user_password = "test_password"
        self.db_connector.user_register(self.user_email, "test_username", self.user_password)

        # User for testing user_delete
        self.user_delete_email = "delete_user@example.com"
        self.user_delete_password = "delete_password"
        self.db_connector.user_register(self.user_delete_email, "delete_username", self.user_delete_password)

        # Chatroom for testing chatrooms_create_and_delete
        self.chatroom_name = "test_chatroom"
        self.db_connector.chatrooms_create(self.chatroom_name)

        # Chatroom for testing chatrooms_join
        self.join_chatroom_name = "join_test_chatroom"
        self.db_connector.chatrooms_create(self.join_chatroom_name)

        # Chatroom for testing messages_send
        self.send_message_chatroom_name = "send_test_chatroom"
        self.db_connector.chatrooms_create(self.send_message_chatroom_name)

        # Chatroom for testing messages_edit_and_delete
        self.edit_delete_chatroom_name = "edit_delete_test_chatroom"
        self.db_connector.chatrooms_create(self.edit_delete_chatroom_name)

        # User for testing messages_edit_and_delete
        self.edit_delete_user_email = "edit_delete@example.com"
        self.edit_delete_user_password = "edit_delete_password"
        self.db_connector.user_register(self.edit_delete_user_email, "edit_delete_username", self.edit_delete_user_password)

    def tearDown(self):
        # Clean up created users and chatrooms
        self.db_connector.user_delete(self.user_email)
        self.db_connector.user_delete(self.user_delete_email)
        self.db_connector.chatrooms_delete(self.chatroom_name)
        self.db_connector.chatrooms_delete(self.join_chatroom_name)
        self.db_connector.chatrooms_delete(self.send_message_chatroom_name)
        self.db_connector.chatrooms_delete(self.edit_delete_chatroom_name)
        self.db_connector.user_delete(self.edit_delete_user_email)

    def test_user_register_and_return_info(self):
        info = self.db_connector.user_return_info(self.user_email)
        self.assertIsNotNone(info)
        self.assertEqual(info[1], self.user_email)

    def test_user_delete(self):
        info = self.db_connector.user_return_info(self.user_delete_email)
        self.assertIsNotNone(info)
        self.assertTrue(self.db_connector.user_delete(info[0]))

    def test_chatrooms_create_and_delete(self):
        chatrooms = self.db_connector.chatrooms_list()
        self.assertTrue(any(chatroom[1] == self.chatroom_name for chatroom in chatrooms))
        self.assertTrue(self.db_connector.chatrooms_delete(chatrooms[0][0]))

    def test_chatrooms_join(self):
        chatrooms = self.db_connector.chatrooms_list()
        chatroom_id = [chatroom[0] for chatroom in chatrooms if chatroom[1] == self.join_chatroom_name][0]
        self.assertIsNotNone(self.db_connector.chatrooms_join(chatroom_id))

    def test_messages_send(self):
        chatrooms = self.db_connector.chatrooms_list()
        chatroom_id = [chatroom[0] for chatroom in chatrooms if chatroom[1] == self.send_message_chatroom_name][0]
        info = self.db_connector.user_return_info(self.user_email)
        self.assertIsNotNone(info)
        userid = info[0]
        message_content = "Test message"
        self.assertTrue(self.db_connector.messages_send(userid, chatroom_id, message_content))

    def test_messages_edit_and_delete(self):
        chatrooms = self.db_connector.chatrooms_list()
        chatroom_id = [chatroom[0] for chatroom in chatrooms if chatroom[1] == self.edit_delete_chatroom_name][0]
        info = self.db_connector.user_return_info(self.edit_delete_user_email)
        self.assertIsNotNone(info)
        userid = info[0]
        message_content = "Initial message"
        self.assertTrue(self.db_connector.messages_send(userid, chatroom_id, message_content))
        messages = self.db_connector.messages_list_in_chatroom(chatroom_id)
        message_id = messages[0][0]
        new_message_content = "Edited message"
        self.assertTrue(self.db_connector.messages_edit(userid, chatroom_id, message_id, new_message_content))
        self.assertTrue(self.db_connector.messages_delete(userid, chatroom_id, message_id))

    def test_messages_list_in_chatroom(self):
        chatrooms = self.db_connector.chatrooms_list()
        chatroom_id = [chatroom[0] for chatroom in chatrooms if chatroom[1] == self.send_message_chatroom_name][0]
        info = self.db_connector.user_return_info(self.user_email)
        self.assertIsNotNone(info)
        userid = info[0]
        message_content = "Test message 1"
        self.assertTrue(self.db_connector.messages_send(userid, chatroom_id, message_content))
        message_content = "Test message 2"
        self.assertTrue(self.db_connector.messages_send(userid, chatroom_id, message_content))
        messages = self.db_connector.messages_list_in_chatroom(chatroom_id)
        self.assertEqual(len(messages), 2)

if __name__ == '__main__':
    unittest.main()
