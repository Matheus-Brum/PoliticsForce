import unittest
from database.db_general import Database


class Test(unittest.TestCase):
    def test_aaa(self):
        validate = Database.get_connection()
        self.assertEqual(validate, None)


