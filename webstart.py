from flask import Flask, render_template
import sqlite3
import settings

# This sets up the SQLite and creates a cursor which creates, edits and stores values
class getCur():
    con = None
    cur = None
    def __enter__(self):
        self.con = sqlite3.connect(settings.DBFILE)
        self.cur = self.con.cursor()
        self.cur.execute("PRAGMA foreign_keys = 1;")
        return self.cur
    def __exit__(self, type, value, traceback):
        if self.cur and self.con and not value:
            self.cur.close()
            self.con.commit()
            self.con.close()

        return False


# This sets up flask to work properly
app = Flask(__name__)
@app.route("/")
def getLeaderboard():
	leaderboard = []
	with getCur() as cur:
		cur.execute("SELECT Username, ViewCount FROM Viewers ORDER BY ViewCount DESC LIMIT 100")
		leaderboard = cur.fetchall()
	return render_template('index.html',leaderboard=leaderboard)

if __name__=='__main__':
	app.run(host='0.0.0.0', port=8000)







