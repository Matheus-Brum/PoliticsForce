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
                       "(F_name, L_name, Member_no, Phone_no, Mem_exp_date, Reach_moment, Birth_date, Email, Last_donation,"
                            " Date_last_donation, Donation_ok, Election_year, Comment, Address)"
                       " VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (member.f_name, member.l_name, member.member_no, member.phone_no, member.mem_exp_date, member.reach_moment,
                            member.birth_date, member.email, member.last_donation, member.date_last_donation, member.donation_ok,
                            member.election_year, member.comment, member.address))
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
        cursor.execute("SELECT F_name, L_name, Id, Phone_no, Address "
                       "FROM Members "
                       "WHERE ? LIKE ?",
                       (search_in, "'%"+search_for+"%'"))
        results = cursor.fetchall()
        for result in results:
            member = Member(result[0], result[1], result[2], result[3], result[4])
            members.append(member)
        return members
