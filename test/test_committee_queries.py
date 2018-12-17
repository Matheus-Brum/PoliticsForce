import unittest
import sqlite3
from database.db_general import Database
from database.queries.Committee_queries import CommitteeQueries


class TestCommitteeQueries(unittest.TestCase):

    def setUp(self):
        self.queries = CommitteeQueries()
        self.queries.connection = sqlite3.connect('test/db_test.db')

    def tearDown(self):
        self.queries.disconnect()

    def test_get_members_circonscription(self):
        # circonscription existante
        circonscription = 'Québec'
        committees = self.queries.get_members_circonscription(circonscription)
        expected = '1234567893'
        for mbr in committees:
            self.assertEqual(mbr.member_no, expected,
                             "Erreur: Committee_queries.get_members_circonscription.circonscription_existente")

        # circonscription inexistante
        circonscription = 'Joyal'
        committees = self.queries.get_members_circonscription(circonscription)
        expected = []
        self.assertEqual(committees, expected,
                         "Erreur: Committee_queries.get_members_circonscription.circonscription_inexistente")

    def test_get_members_regional(self):
        # region existante
        regional = 'Ontario'
        committees = self.queries.get_members_regional(regional)
        expected = ['1234567891', '4444444444', '1234567892']
        i = 0
        for mbr in committees:
            # print("Ontario : " + mbr.member_no + " ;")
            self.assertEqual(mbr.member_no, expected[i],
                             "Erreur: Committee_queries.get_members_regional.region_existente")
            i += 1

        # region inexistante
        regional = 'Joyal'
        committees = self.queries.get_members_circonscription(regional)
        expected = []
        self.assertEqual(committees, expected, "Erreur: Committee_queries.get_members_regional.region_inexistente")

    def test_get_members_national(self):
        # niveau national existant
        national = 'Canada'
        committees = self.queries.get_members_national(national)
        expected = ['1234567890', '1234567891', '4444444444', '1234567893']
        i = 0
        for mbr in committees:
            # print("Canada : " + mbr.member_no + " ;")
            self.assertEqual(mbr.member_no, expected[i],
                             "Erreur: Committee_queries.get_members_national.national_existent")
            i += 1

        # niveau national inexistant
        national = 'Joyal'
        committees = self.queries.get_members_circonscription(national)
        expected = []
        self.assertEqual(committees, expected, "Erreur: Committee_queries.get_members_national.national_inexistent")


if __name__ == '__main__':
    unittest.main()
