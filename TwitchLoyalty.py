
import requests
import json
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

#This creates the SQLite Table

def createTables():
	with getCur() as cur:
		cur.execute("CREATE TABLE IF NOT EXISTS CurrentViewers(Username TEXT PRIMARY KEY);")
		cur.execute("CREATE TABLE IF NOT EXISTS Viewers(Username TEXT PRIMARY KEY, ViewCount INTEGER);")

def currentViewers(viewers):
	with getCur() as cur:
		cur.execute("DELETE FROM CurrentViewers;")
		for viewer in viewers:
			cur.execute("INSERT INTO CurrentViewers VALUES(?);",(viewer,))


def incrementViewer(viewer):
	with getCur() as cur:
		cur.execute("SELECT EXISTS(SELECT * FROM Viewers  WHERE Username = ?)",(viewer,))
		if cur.fetchone()[0] == 0:
			cur.execute("INSERT INTO Viewers VALUES (?,1);",(viewer,))
		else:
			cur.execute("UPDATE Viewers SET ViewCount = ViewCount + 1 WHERE Username = ?;",(viewer,))

#Boolean that returns True if veiewer has viewed this session
def currentlyViewing(viewer):
	with getCur() as cur:
		cur.execute("SELECT EXISTS(SELECT * FROM CurrentViewers WHERE Username = ?)",(viewer,))
		return cur.fetchone()[0] == 1


def getViewers():
	print('Beginning file download with requests')
	url ='https://tmi.twitch.tv/group/user/' + settings.TWITCHCHANNEL + '/chatters'
	r = requests.get(url)
	tmp = json.loads(r.content.decode('ascii'))
	return tmp["chatters"]["viewers"]

# This goes through the CURRENT viewers and compares them against the table of viewers
def incrementViewers():
	viewers = getViewers()
	with getCur() as cur:
		for viewer in viewers:
			if not currentlyViewing(viewer):
				incrementViewer(viewer)
	currentViewers(viewers)

if __name__ == "__main__":
	createTables()
	incrementViewers()







