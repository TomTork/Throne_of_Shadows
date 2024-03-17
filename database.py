import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("./database.db")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS main(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            existing INTEGER,
            happy INTEGER,
            money INTEGER,
            debt INTEGER,
            taro INTEGER,
            weapons INTEGER,
            foods TEXT,
            others TEXT
        )""")
        if not self.get_all():  # auto generate table
            self.c.execute("""INSERT INTO main VALUES(0,0,0,0,1,0,1,"","")""")
            self.conn.commit()

    def reload(self):
        self.set_existing(0)
        self.set_happy(100)
        self.set_money(20)
        self.set_debt(1)
        self.set_taro(0)
        self.set_weapons(1)
        self.set_foods("")
        self.set_others("")

    def get_all(self):
        return self.c.execute("SELECT * FROM main").fetchall()

    def get_existing(self) -> int:
        return int(self.c.execute("SELECT existing FROM main WHERE ID=0").fetchone()[0])

    def set_existing(self, value: int):
        self.c.execute(f"UPDATE main SET existing={value} WHERE ID=0")
        self.conn.commit()

    def get_happy(self) -> int:
        return int(self.c.execute("SELECT happy FROM main WHERE ID=0").fetchone()[0])

    def set_happy(self, value: int):
        self.c.execute(f"UPDATE main SET happy={value} WHERE ID=0")
        self.conn.commit()

    def get_money(self) -> int:
        return int(self.c.execute("SELECT money FROM main WHERE ID=0").fetchone()[0])

    def set_money(self, value: int):
        self.c.execute(f"UPDATE main SET money={value} WHERE ID=0")
        self.conn.commit()

    def get_debt(self) -> int:
        return int(self.c.execute("SELECT debt FROM main WHERE ID=0").fetchone()[0])

    def set_debt(self, value: int):
        self.c.execute(f"UPDATE main SET debt={value} WHERE ID=0")
        self.conn.commit()

    def get_taro(self) -> int:
        return int(self.c.execute("SELECT taro FROM main WHERE ID=0").fetchone()[0])

    def set_taro(self, value: int):
        self.c.execute(f"UPDATE main SET taro={value} WHERE ID=0")
        self.conn.commit()

    def get_weapons(self) -> int:
        return int(self.c.execute("SELECT weapons FROM main WHERE ID=0").fetchone()[0])

    def set_weapons(self, value: int):
        self.c.execute(f"UPDATE main SET weapons={value} WHERE ID=0")
        self.conn.commit()

    def get_foods(self) -> str:
        return str(self.c.execute("SELECT foods FROM main WHERE ID=0").fetchone()[0])

    def set_foods(self, value: str):
        self.c.execute(f"UPDATE main SET foods=\"{value}\" WHERE ID=0")
        self.conn.commit()

    def get_others(self) -> str:
        return str(self.c.execute("SELECT others FROM main WHERE ID=0").fetchone()[0])

    def set_others(self, value: str):
        self.c.execute(f"UPDATE main SET others=\"{value}\" WHERE ID=0")
        self.conn.commit()