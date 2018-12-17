import sqlite3
import unittest
from database.db_general import Database


class TestDbGeneral(unittest.TestCase):

    def setUp(self):
        self.db = Database()
        self.db.connection = sqlite3.connect('test/db_test.db')

    def tearDown(self):
        self.db.disconnect()

    def test_get_connection(self):
        cursor = self.db.get_connection().cursor()
        self.assertIsNotNone(cursor, "Erreur: non connecté à la base de données du test")

        cursor = self.db.get_connection().cursor()
        self.assertIsNotNone(cursor, "Erreur: non connecté à la base de données du programme")

    def test_disconnect(self):
        self.assertIsNone(self.db.disconnect(), "Erreur: non déconnecté de la base de données")


if __name__ == '__main__':
    unittest.main()
