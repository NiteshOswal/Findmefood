import os
import dotenv
import MySQLdb as mysql

dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))

class DB(object):
    """ the most basic connection adapter, yolo no opts! """
    def __init__(self):
        self._conn = None
    
    def __enter__(self):
        self._conn = mysql.connect(
            os.environ.get("DB_HOST", "localhost"),
            os.environ.get("DB_USER", "root"),
            os.environ.get("DB_PASS", "secret"),
            os.environ.get("DB_NAME", "spiderman")
        )
        self._conn.autocommit(True)
        return self

    def find(self, query):
        cur = self._conn.cursor(mysql.cursors.DictCursor)
        cur.execute(query)
        return cur.fetchall()

    def findOne(self, query):
        cur = self._conn.cursor(mysql.cursors.DictCursor)
        cur.execute(query)
        return cur.fetchone()

    def update(self, query):
        cur = self._conn.cursor()
        print query
        cur.execute(query)
        return cur.rowcount > 0

    def insert(self, query):
        cur = self._conn.cursor()
        cur.execute(query)
        return cur.lastrowid

    def __exit__(self, type, value, traceback):
        if self._conn:
            self._conn.close()
