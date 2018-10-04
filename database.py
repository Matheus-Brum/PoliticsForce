import sqlite3
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

    def insert_member(self, member):
        cursor = self.get_connection().cursor()
        cursor.execute("INSERT INTO Members "
                       "(F_name, L_name, Member_no, Phone_no, Address)"
                       " VALUES(?, ?, ?, ?, ?)",
                       (member.f_name, member.l_name, member.member_no, member.phone_no, member.address))
        self.connection.commit()

    def get_all_members(self):
        counter = 1
        members = []
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT max(id) "
                       "FROM Members")
        limit = cursor.fetchone()[0]
        while counter <= limit:
            cursor.execute("SELECT * "
                           "FROM Members "
                           "WHERE Id = ?", (counter,))
            member_info = cursor.fetchone()
            member = Member(member_info[1], member_info[2], member_info[3], member_info[4], member_info[5])
            members.append(member)
            counter += 1
        return members

    def verify_member(self, member):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * " 
                       "FROM Members "
                       "WHERE F_name = ? AND L_name = ? AND Member_no = ? AND Phone_no = ? AND Address = ?",
                       (member.f_name, member.l_name, member.member_no, member.phone_no, member.address))
        member_data = cursor.fetchone()
        if member_data is not None:
            return True
        else:
            return False
