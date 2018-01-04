from flask import Flask
import sqlite3
import SimpleHTTPServer
import SocketServer

PORT = 8000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()


# This sets up flask to work properly
app = Flask(__name__)
@app.route("/")
def getLeaderboard():
	leaderboard = ""
	with getCur() as cur:
		cur.execute("SELECT Username, ViewCount FROM Viewers ORDER BY ViewCount DESC LIMIT 10")
		leaderboard = cur.fetchall()
	return str(leaderboard)

# This sets up the SQLite and creates a cursor which creates, edits and stores values
class getCur():
    con = None
    cur = None
    def __enter__(self):
        self.con = sqlite3.connect('viewerDB.sqlite')
        self.cur = self.con.cursor()
        self.cur.execute("PRAGMA foreign_keys = 1;")
        return self.cur
    def __exit__(self, type, value, traceback):
        if self.cur and self.con and not value:
            self.cur.close()
            self.con.commit()
            self.con.close()

        return False


