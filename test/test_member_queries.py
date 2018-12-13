import unittest
import sqlite3
from member import Member
from database.queries.Member_queries import MemberQueries


class TestMemberQueries(unittest.TestCase):

    def setUp(self):
        self.queries = MemberQueries()
        self.queries.connection = sqlite3.connect('test/db_test.db')

    def tearDown(self):
        self.queries.disconnect()

    def test_verify_member_no(self):
        # membre valide
        membre_valide = '1234567890'
        verifier_membre_valide = self.queries.verify_member_no(membre_valide)
        self.assertFalse(verifier_membre_valide, "Erreur: Member_queries.verify_member_no(membre_valide)")

        # membre invalide
        membre_invalide = '1234567899'
        verifier_membre_invalide = self.queries.verify_member_no(membre_invalide)
        self.assertTrue(verifier_membre_invalide, "Erreur: Member_queries.verify_member_no(membre_invalide)")

    def test_verify_member(self):
        # membre valide
        membre_valide = Member('aa', 'aaa', '1234567890', '1111111111', '01/01/2010', 'midi', '01/01/1990',
                               'aa@gmail.com', 100, '01/01/2010', 'oui', 'oui', 'testaa', 'H3P2B1,Portland,ME,US',
                               'Canada')
        verifier_membre_valide = self.queries.verify_member(membre_valide)
        self.assertTrue(verifier_membre_valide, "Erreur: Member_queries.verify_member(membre_valide)")

        # membre invalide
        membre_invalide = Member('bb', 'aaa', '1234567890', '1111111111', '01/01/2010', 'midi', '01/01/1990',
                                 'aa@gmail.com', 100, '01/01/2010', 'oui', 'oui', 'testaa', 'H3P2B1,Portland,ME,US',
                                 'Canada')
        verifier_membre_invalide = self.queries.verify_member(membre_invalide)
        self.assertFalse(verifier_membre_invalide, "Erreur: Member_queries.verify_member(membre_invalide)")

    def test_search_members(self):
        search_in = ['f_name', 'l_name', 'member_no', 'phone_no', 'address']
        with_result = ['a', 'aaa', '1234567890', '1111111111', 'H3P2B1']
        without_result = ['h', 'g', '1234567896', '555', 'Montreal']
        for i in range(len(search_in)):
            search_with = self.queries.search_members(search_in[i], with_result[i])
            search_without = self.queries.search_members(search_in[i], without_result[i])
            for mbr in search_with:
                self.assertEqual(mbr.member_no, '1234567890', "Error: Member_queries.search_members(with_result)")
            self.assertEqual(search_without, [], "Erreur: Member_queries.search_members(without_result)")

    def test_search_member(self):
        # membre valide
        membre_valide = '1234567890'
        search_membre_valide = self.queries.search_member(membre_valide)
        self.assertEqual(search_membre_valide.member_no, '1234567890',
                         "Erreur: Member_queries.verify_member_no(membre_valide)")

        # membre invalide
        membre_invalide = '1234567899'
        search_membre_invalide = self.queries.search_member(membre_invalide)
        self.assertIsNone(search_membre_invalide, "Erreur: Member_queries.verify_member_no(membre_invalide)")

    def test_insert_member(self):
        # inserer un membre inexistent
        id_valide = '1234567897'
        membre_valide = Member('ee', 'ee', id_valide, '8888888888', '01/01/2010', 'midi', '01/01/1990',
                               'ee@gmail.com', 100, '01/01/2010', 'oui', 'oui', 'testaa', 'j4n0g6,Portland,ME,US',
                               'USA')
        self.assertIsNone(self.queries.search_member(id_valide), "Erreur: Member_queries.insert_member(membre_valide)")
        self.queries.insert_member(membre_valide)
        self.assertIsNotNone(self.queries.search_member(id_valide))
        self.queries.supprimer_member(id_valide)
        self.assertIsNone(self.queries.search_member(id_valide))

        # inserer un membre avec un id_membre deja existent
        id_invalide = '1234567893'
        membre_invalide = Member('ff', 'fff', id_invalide, '1111111111', '01/01/2010', 'midi', '01/01/1990',
                                 'ff@gmail.com', 100, '01/01/2010', 'oui', 'oui', 'testaa', 'j4n0g6,Portland,ME,US',
                                 'USA')
        self.assertIsNotNone(self.queries.search_member(id_invalide),
                             "Erreur: Member_queries.insert_member(membre_existent)")
        self.assertRaises(sqlite3.IntegrityError, self.queries.insert_member, membre_invalide)

    def test_supprimer_member(self):
        # supprimer un membre
        id_valide = '1234567898'
        membre_valide = Member('ee', 'ee', id_valide, '8888888888', '01/01/2010', 'midi', '01/01/1990',
                               'ee@gmail.com', 100, '01/01/2010', 'oui', 'oui', 'testaa', 'j4n0g6,Portland,ME,US',
                               'USA')
        self.assertIsNone(self.queries.search_member(id_valide), "Erreur: Member_queries.supprimer_member")
        self.queries.insert_member(membre_valide)
        self.assertIsNotNone(self.queries.search_member(id_valide), "Erreur: Member_queries.supprimer_member")
        self.queries.supprimer_member(id_valide)
        self.assertIsNone(self.queries.search_member(id_valide), "Erreur: Member_queries.supprimer_member")

    def test_update_member(self):
        membre_valide = Member('cc', 'ccc', '1234567892', '3333333333', '01/01/2010', 'midi', '01/01/1990',
                               'cc@gmail.com', 300, '01/01/2010', 'oui', 'oui', '',
                               '123456,A1A1A1,Alberton,PE,CA', 'Toronto')
        self.assertTrue(self.queries.update_member(membre_valide), "Erreur: Member_queries.update_member")
        """
        membre_invalide = Member('aa', 'aaa', '1234567899', '1111111111', '01/01/2010', 'midi', '01/01/1990',
                                 'aa@gmail.com', 100, '01/01/2010', 'oui', 'oui', '', 'H3P2B1,Portland,ME,US',
                                 'Canada')
        self.assertTrue(self.queries.update_member(membre_invalide), "Erreur: Member_queries.update_member")
        """


if __name__ == '__main__':
    unittest.main()
