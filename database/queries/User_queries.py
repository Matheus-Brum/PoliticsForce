from database.db_general import Database
from member import Member
import hashlib


class UserQueries(Database):

    def __init__(self):
        # self.connection = Database.get_connection(self)
        # self.disconnect = Database.disconnect(self)
        super().__init__()

    def get_user(self, email):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * "
                       "FROM Members INNER JOIN USERS ON Members.Member_no = Users.Member_no "
                       "WHERE Members.Email=?", (email,))
        user_info = cursor.fetchone()
        return user_info

    def create_user(self, username, salt, hashed_password):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT Member_no "
                       "FROM Members "
                       "WHERE Email=?", (username,))
        member_id = cursor.fetchone()[0]
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

    def validate_user(self, email):
        cursor = self.get_connection().cursor()
        cursor.execute("""
                    SELECT Users.Salt, Users.Password
                    FROM Members INNER JOIN Users ON Members.Member_no = Users.Member_no
                    WHERE Members.Email=?
                    """, (email,))
        user_cred = cursor.fetchone()
        # print('user_cred=', user_cred)
        if user_cred is not None:
            return True
        else:
            return False

    def get_admin_credentials(self, password):
        admin_no = '9999999999'
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT Salt, Password "
                       "FROM Users "
                       "WHERE Member_no = ?", (admin_no,))
        admin_cred = cursor.fetchone()
        if admin_cred is not None:
            salt = admin_cred[0]
            hashed_password = hashlib.sha512(str(password + salt).encode("utf-8")).hexdigest()
            if admin_cred[1] == hashed_password:
                return True
            else:
                return False
        else:
            return False

    def get_all_users(self):
        all_users = []
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * "
                       "FROM Members INNER JOIN USERS ON Members.Member_no = Users.Member_no ")
        users = cursor.fetchall()
        for person in users:
            member = Member(person[1], person[2], person[3], person[4], person[5],
                            person[6], person[7], person[8], person[9], person[10],
                            person[11], person[12], person[13], person[14], person[15])
            all_users.append(member)
        return all_users
