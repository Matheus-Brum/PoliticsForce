import unittest
import sqlite3
from database.queries.Session_queries import SessionQueries


class TestSessionQueries(unittest.TestCase):

    def setUp(self):
        self.queries = SessionQueries()
        self.queries.connection = sqlite3.connect('test/db_test.db')

    def tearDown(self):
        self.queries.disconnect()

    def test_get_session(self):
        email = 'aa@gmail.com'
        committee = 'Canada'
        id_session = self.queries.save_session(email, committee, 3)
        result = self.queries.get_session(id_session)
        self.assertEqual(result[0], email, "Error getting the session")
        self.assertEqual(result[1], committee, "Error getting the session")

    def test_save_session(self):
        self.queries.connection = None
        id_session = self.queries.save_session('aa@gmail.com', 'Canada', 3)
        self.assertIsNotNone(id_session, "Error saving the session")

    def test_delete_session(self):
        id_session = self.queries.save_session('aa@gmail.com', 'Canada', 3)
        self.assertIsNotNone(id_session, "test_delete_session: session not created")
        self.queries.delete_session(id_session)
        self.assertRaises(IndexError, self.queries.get_session, id_session)


if __name__ == '__main__':
    unittest.main()
