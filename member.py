class Member:
    def __init__(self, f_name, l_name, member_no, phone_no, mem_exp_date, reach_moment, birth_date, email,
                 last_donation, date_last_donation, donation_ok, election_year, comment, address, committee):
        self.f_name = f_name
        self.l_name = l_name
        self.member_no = member_no
        self.phone_no = phone_no
        self.mem_exp_date = mem_exp_date
        self.reach_moment = reach_moment
        self.birth_date = birth_date
        self.email = email
        self.last_donation = last_donation
        self.date_last_donation = date_last_donation
        self.donation_ok = donation_ok
        self.election_year = election_year
        self.comment = comment
        self.address = address
        self.committee = committee

    def serialize(self):
        return {
            'f_name': self.f_name,
            'l_name': self.l_name,
            'member_no': self.member_no,
            'phone_no': self.phone_no,
            'mem_exp_date': self.mem_exp_date,
            'reach_moment': self.reach_moment,
            'birth_date': self.birth_date,
            'email': self.email,
            'last_donation': self.last_donation,
            'date_last_donation': self.date_last_donation,
            'donation_ok': self.donation_ok,
            'election_year': self.election_year,
            'comment': self.comment,
            'address': self.address,
            'committee': self.committee
        }
