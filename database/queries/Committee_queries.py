from database.db_general import Database
from member import Member


class CommitteeQueries(Database):

    def __init__(self):
        # self.connection = Database.get_connection(self)
        # self.disconnect = Database.disconnect(self)
        super().__init__()

    def get_all_members(self, committee):
        cursor = self.get_connection().cursor()
        cursor.execute("")
        pass

    def get_members_circonscription(self, committee):
        committees = []
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * "
                       "FROM Members "
                       "WHERE Committee = ?", (committee,))
        members = cursor.fetchall()
        for person in members:
            member = Member(person[1], person[2], person[3], person[4], person[5],
                            person[6], person[7], person[8], person[9], person[10],
                            person[11], person[12], person[13], person[14], person[15])
            committees.append(member)
        return committees

    def get_members_regional(self, committee):
        committees_members = []
        circonscription_committees = []
        cursor = self.get_connection().cursor()
        if len(self.get_members_circonscription(committee)) > 0:
            committees_members = self.get_members_circonscription(committee)
        cursor.execute("SELECT Id FROM RegionalC WHERE Name = ?", (committee,))
        parent_id = cursor.fetchone()
        if parent_id is not None:
            parent_id = parent_id[0]
        if parent_id is not None:
            cursor.execute(
                "SELECT CirconscriptionC.Name "
                "FROM RegionalC INNER JOIN CirconscriptionC ON RegionalC.Id = CirconscriptionC.Parent_id "
                "WHERE RegionalC.Id = ?",
                (parent_id,))
            results = cursor.fetchall()
            if len(results) > 0:
                for line in results:
                    circonscription_committees.append(line[0])
                for i in circonscription_committees:
                    cursor.execute("SELECT * "
                                   "FROM Members "
                                   "WHERE Committee = ?", (i,))
                    committees_members_circonscription = cursor.fetchall()
                    for person in committees_members_circonscription:
                        member = Member(person[1], person[2], person[3], person[4], person[5],
                                        person[6], person[7], person[8], person[9], person[10],
                                        person[11], person[12], person[13], person[14], person[15])
                        committees_members.append(member)
        return committees_members

    def get_members_national(self, committee):
        committees_members = []
        regional_committees = []
        cursor = self.get_connection().cursor()
        if len(self.get_members_regional(committee)) > 0:
            committees_members = self.get_members_regional(committee)
        cursor.execute("SELECT Id FROM NationalC WHERE Name = ?", (committee,))
        parent_id = cursor.fetchone()
        if parent_id is not None:
            parent_id = parent_id[0]
        if parent_id is not None:
            cursor.execute(
                "SELECT RegionalC.Name "
                "FROM NationalC INNER JOIN RegionalC ON NationalC.Id = RegionalC.Parent_id "
                "WHERE NationalC.Id = ?",
                (parent_id,))
            results = cursor.fetchall()
            for line in results:
                regional_committees.append(line[0])
            for i in regional_committees:
                cursor.execute("SELECT * "
                               "FROM Members "
                               "WHERE Committee = ?", (i,))
                committees_members_region = cursor.fetchall()
                for person in committees_members_region:
                    member = Member(person[1], person[2], person[3], person[4], person[5],
                                    person[6], person[7], person[8], person[9], person[10],
                                    person[11], person[12], person[13], person[14], person[15])
                    committees_members.append(member)
        return committees_members
