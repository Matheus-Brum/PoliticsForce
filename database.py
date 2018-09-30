import sqlite3


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

    def ajouter(self, prenom, nom):
        cursor = self.get_connection().cursor()
        cursor.execute("INSERT INTO membre "
                       "(prenom, nom)"
                       " VALUES(?, ?)",
                       (prenom, nom))
        self.connection.commit()
