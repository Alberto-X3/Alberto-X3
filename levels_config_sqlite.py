"""
DB-Structure:
========================

lvl:
------------------------
:user:<int>
    ID from the user
:level:<int>
    LVL from the user
:xp:<int>
    XP from the user

"""

from sqlite3 import connect

create = "CREATE TABLE IF NOT EXISTS lvl\n" \
         "(user integer, level integer, xp integer)"

con = connect("levels.sqlite")
cur = con.cursor()

cur.execute(create)

con.commit()
con.close()
