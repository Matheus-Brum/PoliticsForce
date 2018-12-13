import hashlib
import unittest
import sqlite3
import uuid
from database.queries.User_queries import UserQueries


class TestUserQueries(unittest.TestCase):

    def setUp(self):
        self.queries = UserQueries()
        self.queries.connection = sqlite3.connect('test/db_test.db')

    def tearDown(self):
        self.queries.disconnect()

    def test_create_user(self):
        # creation utilisateur valide
        salt = uuid.uuid4().hex
        membre_id = '1234567892'
        membre_valid = 'cc@gmail.com'
        hashed_password = hashlib.sha512(str('abc' + salt).encode("utf-8")).hexdigest()
        self.queries.create_user(membre_valid, salt, hashed_password)
        cursor = self.queries.get_connection().cursor()
        cursor.execute("DELETE FROM Users WHERE Member_no=?", (membre_id,))
        self.queries.connection.commit()

        # creation utilisateur qui n'est pas membre
        membre_invalid = 'xx@gmail.com'
        self.assertRaises(TypeError, self.queries.create_user, membre_invalid, salt, hashed_password)

    def test_get_credentials(self):
        # courriel valid ; mot de passe valid
        email = 'aa@gmail.com'
        password = 'abc'
        self.assertTrue(self.queries.get_credentials(email, password))

        # courriel valid ; mot de passe invalid
        password = 'def'
        self.assertFalse(self.queries.get_credentials(email, password))

        # courriel invalid ; mot de passe invalid
        email = 'xx@gmail.com'
        self.assertFalse(self.queries.get_credentials(email, password))

        # courriel invalid ; mot de passe valid
        password = 'abc'
        self.assertFalse(self.queries.get_credentials(email, password))

    def test_validate_user_pass(self):
        # courriel valid ; mot de passe valid
        email = 'aa@gmail.com'
        password = 'abc'
        self.assertTrue(self.queries.validate_user_pass(email, password))

        # courriel valid ; mot de passe invalid
        email = 'aa@gmail.com'
        password = 'def'
        self.assertFalse(self.queries.validate_user_pass(email, password))

        # courriel invalid ; mot de passe valid
        email = 'a@gmail.com'
        password = 'abc'
        self.assertFalse(self.queries.validate_user_pass(email, password))

        # courriel invalid ; mot de passe invalid
        email = 'xx@gmail.com'
        password = 'qaz'
        self.assertFalse(self.queries.validate_user_pass(email, password))


if __name__ == '__main__':
    unittest.main()
