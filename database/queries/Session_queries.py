from database.db_general import Database

import uuid


class SessionQueries(Database):

    def __init__(self):
        # self.connection = Database.get_connection(self)
        # self.disconnect = Database.disconnect(self)
        super().__init__()

    def get_session(self, id_session):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT SessionEmail, SessionCommittee "
                       "FROM Sessions "
                       "WHERE Id_session=?",
                       (id_session,))
        result = cursor.fetchall()[0]
        email = result[0]
        committee = result[1]
        if email is None or committee is None:
            return None
        else:
            return [email, committee]

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
