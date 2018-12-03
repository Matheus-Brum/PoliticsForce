import sqlite3
import hashlib
import uuid
from .member import Member


class Database:

    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/db.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def get_session(self, id_session):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT SessionEmail, SessionCommittee "
                       "FROM Sessions "
                       "WHERE Id_session=?",
                       (id_session,))
        email = cursor.fetchall()[0]
        committee = cursor.fetchall()[1]
        # level = cursor.fetchall()[2]
        """
        if email is None or committee is None:
            return None
        else:
            return [email, committee]
        """
        return [email, committee]

    def create_user(self, username, salt, hashed_password):
        print(type(username))
        print(type(salt))
        print(type(hashed_password))
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT Member_no "
                       "FROM Members "
                       "WHERE Email=?", (username,))
        member_id = cursor.fetchone()[0]
        print('member_id', member_id)
        cursor.execute(("INSERT INTO Users(Member_no, Password, Salt) "
                        "VALUES(?, ?, ?)"), (member_id, hashed_password, salt))
        self.connection.commit()

    def get_credentials(self, email, password):
        cursor = self.get_connection().cursor()
        cursor.execute("""
                    SELECT Users.Salt, Users.Password
                    FROM Members INNER JOIN Users ON Members.Member_no = Users.Member_no
                    WHERE Members.Email=?
                    """, (email,))
        user_cred = cursor.fetchone()
        if user_cred is not None:
            salt = user_cred[0]
            hashed_password = hashlib.sha512(str(password + salt).encode("utf-8")).hexdigest()
            if user_cred[1] == hashed_password:
                return True
            else:
                return False
        else:
            return False

    def validate_user_pass(self, email, password):
        cursor = self.get_connection().cursor()
        cursor.execute("""
                    SELECT Users.Salt, Users.Password
                    FROM Members INNER JOIN Users ON Members.Member_no = Users.Member_no
                    WHERE Members.Email=?
                    """, (email,))
        user_cred = cursor.fetchone()
        if user_cred is not None:
            return True
        else:
            return False

    def save_session(self, email, committee):
        id_session = uuid.uuid4().hex
        cursor = self.get_connection().cursor()
        cursor.execute("INSERT INTO Sessions(Id_session, SessionEmail, SessionCommittee) "
                       "VALUES(?, ?, ?)", (id_session, email, committee))
        # self.connection.commit()
        return id_session

    def delete_session(self, id_session):
        cursor = self.get_connection().cursor()
        cursor.execute(("DELETE FROM Sessions "
                        "WHERE id_session=?"),
                       (id_session,))
        self.connection.commit()

    def insert_member(self, member):
        cursor = self.get_connection().cursor()
        cursor.execute("INSERT INTO Members "
                       "(F_name, L_name, Member_no, Phone_no, Mem_exp_date, Reach_moment, Birth_date, Email, Last_donation,"
                       " Date_last_donation, Donation_ok, Election_year, Comment, Address, Circonscription)"
                       " VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (member.f_name, member.l_name, member.member_no, member.phone_no, member.mem_exp_date,
                        member.reach_moment,
                        member.birth_date, member.email, member.last_donation, member.date_last_donation,
                        member.donation_ok,
                        member.election_year, member.comment, member.address, member.circonscription))
        self.connection.commit()

    def verify_member_no(self, member_number):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT Member_no FROM Members "
                       "WHERE Member_no =? ", (member_number,))
        member_no = cursor.fetchone()
        if member_no is None:
            return True
        else:
            return False

    def supprimer_member(self, member_number):
        cursor = self.get_connection().cursor()
        cursor.execute("DELETE FROM Members "
                       "WHERE Member_no =? ", (member_number,))
        self.connection.commit()

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

    def verify_member(self, member):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * "
                       "FROM Members "
                       "WHERE F_name = ? AND L_name = ? AND Member_no = ? AND Phone_no = ? AND Mem_exp_date = ? "
                       "AND Reach_moment = ? AND Birth_date = ? AND Email = ? AND Last_donation = ? "
                       "AND Date_last_donation = ? AND Donation_ok = ? AND Election_year = ? AND Comment = ?"
                       "AND Address = ? AND Committee = ?",
                       (member.f_name, member.l_name, member.member_no, member.phone_no, member.mem_exp_date,
                        member.reach_moment, member.birth_date, member.email, member.last_donation,
                        member.date_last_donation, member.donation_ok, member.election_year, member.comment,
                        member.address, member.committee))
        member_data = cursor.fetchone()
        if member_data is not None:
            return True
        else:
            return False

    def search_members(self, search_in, search_for):
        members = []
        cursor = self.get_connection().cursor()
        print("SEARCH IN : " + search_in)
        print("SEARCH FOR : " + search_for)
        sql = "SELECT * FROM Members WHERE " + search_in + " LIKE '%" + search_for + "%'"
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            member = Member(result[1], result[2], result[3], result[4], result[5],
                            result[6], result[7], result[8], result[9], result[10],
                            result[11], result[12], result[13], result[14], result[15])
            members.append(member)
        return members

    def search_member(self, member_no):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM Members WHERE Member_no = ?", (member_no,))
        member_info = cursor.fetchone()

        member = Member(member_info[1], member_info[2], member_info[3], member_info[4], member_info[5],
                        member_info[6], member_info[7], member_info[8], member_info[9], member_info[10],
                        member_info[11], member_info[12], member_info[13], member_info[14], member_info[15])
        print(member.f_name, member.l_name, member.member_no, member.phone_no, member.address, member.email, member.last_donation, member.date_last_donation,
              member.donation_ok, member.election_year, member.mem_exp_date, member.reach_moment, member.birth_date, member.comment, member.committee)
        if member_info is not None:
            return member

    def get_user(self, email):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * "
                       "FROM Members INNER JOIN USERS ON Members.Member_no = Users.Member_no "
                       "WHERE Members.Email=?", (email,))
        user_info = cursor.fetchone()
        return user_info

    def update_member(self, member):
        member_key = member.member_no
        cursor = self.get_connection().cursor()
        cursor.execute("UPDATE Members "
                       "SET F_name = ?, L_name = ?, Member_no = ?, Phone_no = ?, Mem_exp_date = ?, "
                       "Reach_moment = ?, Birth_date = ?, Email = ?, Last_donation = ?, "
                       "Date_last_donation = ?, Donation_ok = ?, Election_year = ?, Comment = ?,"
                       "Address = ?, Committee = ? "
                       "WHERE Member_no = ?", (member.f_name, member.l_name, member.member_no, member.phone_no,
                                               member.mem_exp_date, member.reach_moment, member.birth_date,
                                               member.email, member.last_donation, member.date_last_donation, member.donation_ok,
                                               member.election_year, member.comment, member.address, member.committee, member_key))
        self.connection.commit()
