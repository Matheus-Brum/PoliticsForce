
from database.db_general import Database
from member import Member


class MemberQueries(Database):

    def __init__(self):
        # self.connection = Database.get_connection(self)
        # self.disconnect = Database.disconnect(self)
        super().__init__()

    def verify_member_no(self, member_number):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT Member_no FROM Members "
                       "WHERE Member_no =? ", (member_number,))
        member_no = cursor.fetchone()
        if member_no is None:
            return True
        else:
            return False

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
        members_found = []
        cursor = self.get_connection().cursor()
        """
        if level is 1:
            members = CommitteeQueries().get_members_circonscription(committee)
        elif level is 2:
            members = CommitteeQueries().get_members_regional(committee)
        else:
            members = CommitteeQueries().get_members_national(committee)
        """
        sql = "SELECT * FROM Members WHERE " + search_in + " LIKE '%" + search_for + "%' "
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            member = Member(result[1], result[2], result[3], result[4], result[5],
                            result[6], result[7], result[8], result[9], result[10],
                            result[11], result[12], result[13], result[14], result[15])
            members_found.append(member)
        return members_found

    def search_member(self, member_no):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM Members WHERE Member_no = ?", (member_no,))
        member_info = cursor.fetchone()
        if member_info is not None:
            member = Member(member_info[1], member_info[2], member_info[3], member_info[4], member_info[5],
                            member_info[6], member_info[7], member_info[8], member_info[9], member_info[10],
                            member_info[11], member_info[12], member_info[13], member_info[14], member_info[15])
            return member
        return None

    def insert_member(self, member):
        cursor = self.get_connection().cursor()
        cursor.execute("INSERT INTO Members "
                       "(F_name, L_name, Member_no, Phone_no, Mem_exp_date, Reach_moment, Birth_date, Email, "
                       "Last_donation, Date_last_donation, Donation_ok, Election_year, Comment, Address, Committee)"
                       " VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (member.f_name, member.l_name, member.member_no, member.phone_no, member.mem_exp_date,
                        member.reach_moment, member.birth_date, member.email, member.last_donation,
                        member.date_last_donation,member.donation_ok, member.election_year, member.comment,
                        member.address, member.committee))
        self.connection.commit()
        return True

    def supprimer_member(self, member_number):
        cursor = self.get_connection().cursor()
        cursor.execute("DELETE FROM Members "
                       "WHERE Member_no =? ", (member_number,))
        self.connection.commit()
        return True

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
                                               member.email, member.last_donation, member.date_last_donation,
                                               member.donation_ok,
                                               member.election_year, member.comment, member.address, member.committee,
                                               member_key))
        self.connection.commit()
        return True
