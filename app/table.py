import sqlite3

from Database import Database


# read the connection parameters
params = {
    "database":"gmail_emails_db",
}


class Table(Database):

    def __init__(self):
        super().__init__(**params)

    def create_table(self):

        """ create table in the PostgreSQL database """

        CREATE_TABLE_COMMAND = ("""
            CREATE TABLE IF NOT EXISTS emails (
                id SERIAL PRIMARY KEY,
                email VARCHAR(320) NOT NULL,
                subject VARCHAR(500) NOT NULL,
                date_received TIMESTAMP NOT NULL
            )
            """)

        try:
            # execute command
            self.modify(CREATE_TABLE_COMMAND)

            return True
        except (Exception, sqlite3.DatabaseError) as error:
            print(error)

        return False

    def create_email(self, email, subject, received_date):

        CREATE_EMAIL_COMMAND = (f"""
            INSERT INTO emails (email, subject, date_received) VALUES
            ('{email}', '{subject}', '{received_date}')
        """)

        try:
            # execute command to create email data
            self.modify(CREATE_EMAIL_COMMAND)

            return True
        except (Exception, sqlite3.DatabaseError) as error:
            print(error)

        return False


    def check_row_exists(self, email, subject, received_date):


        QUERY_EMAIL_COMMAND = (f"""
            SELECT email FROM emails 
            WHERE email='{email}' AND subject='{subject}' AND date_received='{received_date}';
        """)

        try:
            # execute command to check email data exists
            res = self.fetch(QUERY_EMAIL_COMMAND)

            return res.fetchone() is not None

        except (Exception, sqlite3.DatabaseError) as error:
            print(error)

        return False

    def query_set(self, WHERE):


        QUERY_EMAIL_COMMAND = (f"""
            SELECT * FROM emails 
            WHERE {WHERE};
        """)

        try:
            # execute command to check email data exists
            res = self.fetch(QUERY_EMAIL_COMMAND)

            return res.fetchone() is not None

        except (Exception, sqlite3.DatabaseError) as error:
            print(error)

        return False
        
    
    def closeConnection(self):
        try:
            # close communication with the PostgreSQL database server
            self.close()
            return True

        except (Exception, sqlite3.DatabaseError) as error:
            print(error)
        return False

