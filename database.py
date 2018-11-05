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

    def join_all_tables(self):

        cursor = self.get_connection().cursor()
        cursor.execute("SELECT  * FROM Members "
                       "INNER JOIN Users ON Members.Member_no = Users.Member_no "
                       "INNER JOIN Sessions ON Members.Email = Sessions.SessionEmail")
        joined_tables = cursor.fetchall()
        return joined_tables

    def get_session(self, id_session):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT SessionEmail "
                       "FROM Sessions "
                       "WHERE Id_session=?",
                       (id_session,))
        email = cursor.fetchone()[0]
        if email is None:
            return None
        else:
            return email

    def create_user(self, username, salt, hashed_password):
        connection = self.get_connection()
        connection.execute(("INSERT INTO users(utilisateur, salt, hash)"
                            " VALUES(?, ?, ?)"), (username, salt,
                                                  hashed_password))
        connection.commit()

    """
    def get_user_login_info(self, username):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT salt, hash "
                       "FROM users "
                       "WHERE utilisateur=?",
                       (username,))
        user = cursor.fetchone()
        if user is None:
            return None
        else:
            return user[0], user[1]
    """

    def get_credentials(self, email, password):
        # joined_tables = self.join_all_tables()
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

    def save_session(self, email):
        id_session = uuid.uuid4().hex
        connection = self.get_connection()
        connection.execute(("INSERT INTO Sessions(Id_session, SessionEmail) "
                            "VALUES(?, ?)"), (id_session, email))
        connection.commit()
        return id_session

    def delete_session(self, id_session):
        connection = self.get_connection()
        connection.execute(("DELETE FROM sessions "
                            "WHERE id_session=?"),
                           (id_session,))
        connection.commit()

    def insert_member(self, member):
        cursor = self.get_connection().cursor()
        cursor.execute("INSERT INTO Members "
                       "(F_name, L_name, Member_no, Phone_no, Mem_exp_date, Reach_moment, Birth_date, Email, Last_donation,"
                       " Date_last_donation, Donation_ok, Election_year, Comment, Address)"
                       " VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (member.f_name, member.l_name, member.member_no, member.phone_no, member.mem_exp_date,
                        member.reach_moment,
                        member.birth_date, member.email, member.last_donation, member.date_last_donation,
                        member.donation_ok,
                        member.election_year, member.comment, member.address))
        self.connection.commit()

    def supprimer_member(self, member_number):
        cursor = self.get_connection().cursor()
        cursor.execute("DELETE FROM Members "
                       "WHERE Member_no =? ", (member_number,))
        self.connection.commit()

    def get_all_members(self):
        counter = 0
        members = []
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT count(*) "
                       "FROM Members")
        limit = cursor.fetchone()[0]
        cursor.execute("SELECT id "
                       "FROM Members")
        counters = cursor.fetchall()
        while counter < limit:
            cursor.execute("SELECT * "
                           "FROM Members "
                           "WHERE Id = ?", (counters[counter][0],))
            member_info = cursor.fetchone()
            member = Member(member_info[1], member_info[2], member_info[3], member_info[4], member_info[5],
                            member_info[6], member_info[7], member_info[8], member_info[9], member_info[10],
                            member_info[11], member_info[12], member_info[13], member_info[14])
            members.append(member)
            counter += 1

        return members

    def verify_member(self, member):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * "
                       "FROM Members "
                       "WHERE F_name = ? AND L_name = ? AND Member_no = ? AND Phone_no = ? AND Mem_exp_date = ? "
                       "AND Reach_moment = ? AND Birth_date = ? AND Email = ? AND Last_donation = ? "
                       "AND Date_last_donation = ? AND Donation_ok = ? AND Election_year = ? AND Comment = ?"
                       "AND Address = ?",
                       (member.f_name, member.l_name, member.member_no, member.phone_no, member.mem_exp_date,
                        member.reach_moment, member.birth_date, member.email, member.last_donation,
                        member.date_last_donation, member.donation_ok, member.election_year, member.comment,
                        member.address))
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
                            result[11], result[12], result[13], result[14])
            members.append(member)
        return members

    def search_member(self, member_no):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM Members WHERE Member_no = ?", (member_no,))
        member_info = cursor.fetchone()

        member = Member(member_info[1], member_info[2], member_info[3], member_info[4], member_info[5],
                        member_info[6], member_info[7], member_info[8], member_info[9], member_info[10],
                        member_info[11], member_info[12], member_info[13], member_info[14])

        if member_info is not None:
            return member

    def search_member2(self, f_name):
        members = []
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT F_name, L_name"
                       "FROM Members "
                       "WHERE F_name = ?",
                       (f_name,))
        member_info = cursor.fetchall()
        print('member_info', member_info)
        for row in member_info:
            member = Member(member_info[1], member_info[2], member_info[3],
                            member_info[4], member_info[5], member_info[6],
                            member_info[7], member_info[8])
            members.append(member)
        return members
