import sqlite3


def setupDB():

    con = sqlite3.connect("theGivingCook.db")

    cur = con.cursor()

    cur.execute("CREATE TABLE movie(title, year, score)")

setupDB()
