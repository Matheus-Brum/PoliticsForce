from database.db_general import Database
from member import Member


class CommitteeQueries(Database):

    def __init__(self):
        # self.connection = Database.get_connection(self)
        # self.disconnect = Database.disconnect(self)
        super().__init__()

    def get_all_members(self):
        all_members = []
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * "
                       "FROM Members")
        members = cursor.fetchall()
        for person in members:
            member = Member(person[1], person[2], person[3], person[4], person[5],
                            person[6], person[7], person[8], person[9], person[10],
                            person[11], person[12], person[13], person[14], person[15])
            all_members.append(member)
        return all_members

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
        cursor.execute("SELECT Id FROM RegionalCommittee WHERE Name = ?", (committee,))
        parent_id = cursor.fetchone()
        if parent_id is not None:
            parent_id = parent_id[0]
        if parent_id is not None:
            cursor.execute(
                "SELECT CirconscriptionCommittee.Name "
                "FROM RegionalCommittee INNER JOIN CirconscriptionCommittee ON RegionalCommittee.Id = CirconscriptionCommittee.Parent_id "
                "WHERE RegionalCommittee.Id = ?",
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
        cursor.execute("SELECT Id FROM NationalCommittee WHERE Name = ?", (committee,))
        parent_id = cursor.fetchone()
        if parent_id is not None:
            parent_id = parent_id[0]
        if parent_id is not None:
            cursor.execute(
                "SELECT RegionalCommittee.Name "
                "FROM NationalCommittee INNER JOIN RegionalCommittee ON NationalCommittee.Id = RegionalCommittee.Parent_id "
                "WHERE NationalCommittee.Id = ?",
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

    def occurrence_in_committees_m(self):
        members_in_c = []
        res_temp = []
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT Committee FROM Members")
        res = cursor.fetchall()
        for item in res:
            res_temp.append(item[0])
        res_distinct = list(set(res_temp))
        for e in res_distinct:
            members_in_c.append({"name": e, "value": res_temp.count(e)})
        return members_in_c

    def occurrence_in_committees_u(self):
        members_in_c = []
        res_temp = []
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT Members.Committee FROM Members INNER JOIN Users ON Members.member_no = Users.member_no")
        res = cursor.fetchall()
        for item in res:
            res_temp.append(item[0])
        res_distinct = list(set(res_temp))
        for e in res_distinct:
            members_in_c.append({"name": e, "value": res_temp.count(e)})
        return members_in_c
