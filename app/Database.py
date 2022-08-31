import sqlite3


class Database:
    """ Manage table using PostgreSQL database """

    def __init__(self, *args, **kwargs):
        self.con = sqlite3.connect(**kwargs)
        self.cur = self.con.cursor()

    def modify(self, query):
        self.cur.execute(query)
        # commit the changes
        self.con.commit()

    def fetch(self, query):
        # query database
        res = self.cur.execute(query)
        return res

    def close(self):
		# close communication with the PostgreSQL database server
        self.cur.close()
        self.con.close()

