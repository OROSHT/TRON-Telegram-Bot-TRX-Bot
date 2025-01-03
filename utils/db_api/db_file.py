import os
import aiosqlite
import datetime
import time

class Profile:
    def __init__(self, info_bd):
        self.user_id, self.username, self.banned, self.balance, self.adress, self.first_time, self.accept = info_bd

class DataBase:
    def __init__(self, database):
        self.database = database

    async def check_start(self):
        self.db = await aiosqlite.connect(self.database)
        await self.db.execute('''CREATE TABLE IF NOT EXISTS users
                                 (user_id INT, username TEXT, banned INT DEFAULT 0, balance INT DEFAULT 0, 
                                  adress TEXT, first_time INT, accept INT DEFAULT 0)''')
        await self.db.execute('''CREATE TABLE IF NOT EXISTS history
                                 (user_id INT, adress TEXT, TRX INT, RUB INT, time_end TEXT)''')
        await self.db.execute('''CREATE TABLE IF NOT EXISTS course
                                 (RUB INT)''')
        if not await (await self.db.execute('SELECT * FROM course')).fetchone():
            await self.db.execute('INSERT INTO course (RUB) VALUES (0)')
        await self.db.commit()

    async def get_course(self):
        course = await (await self.db.execute('SELECT * FROM course')).fetchone()
        return course[0]

    async def update_course(self, value):
        await self.db.execute("UPDATE course SET RUB = ?", (value,))
        await self.db.commit()

    async def add_db(self, user_id, username):
        info = await (await self.db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))).fetchone()
        if not info:
            await self.db.execute('INSERT INTO users (user_id, username, first_time) VALUES (?, ?, ?)', (user_id, username, time.time()))
        elif username != info[1]:
            await self.db.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id))
        await self.db.commit()

    async def get_user(self, user_id):
        info = await (await self.db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))).fetchone()
        return Profile(info) if info else None

    async def get_username(self, username):
        info = await (await self.db.execute("SELECT * FROM users WHERE username = ?", (username,))).fetchone()
        return Profile(info) if info else None

    async def change_balance(self, user_id, amount):
        await self.db.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
        await self.db.commit()

    async def insert_history(self, user_id, adress, TRX, RUB):
        await self.db.execute('INSERT INTO history (user_id, adress, TRX, RUB, time_end) VALUES (?, ?, ?, ?, ?)', 
                              (user_id, adress, TRX, RUB, datetime.datetime.now().strftime("%d.%m.%Y %H:%M")))
        await self.db.commit()

    async def change_adres(self, user_id, adress):
        await self.db.execute("UPDATE users SET adress = ? WHERE user_id = ?", (adress, user_id))
        await self.db.commit()

    async def get_count(self, user_id):
        info = await (await self.db.execute("SELECT * FROM history WHERE user_id = ?", (user_id,))).fetchall()
        return len(info)
    
    async def get_history(self):
        info = await (await self.db.execute("SELECT * FROM history")).fetchall()
        return info[::-1]

    async def change_accept(self, user_id):
        await self.db.execute("UPDATE users SET accept = 1 WHERE user_id = ?", (user_id,))
        await self.db.commit()

    async def get_all_info(self):
        a = len(await (await self.db.execute("SELECT * FROM history")).fetchall())
        b = (await (await self.db.execute("SELECT SUM(RUB) FROM history")).fetchone())[0] or 0
        c = (await (await self.db.execute("SELECT SUM(balance) FROM users")).fetchone())[0] or 0
        d = len(await (await self.db.execute("SELECT * FROM users WHERE first_time > ?", (time.time() - 86400,))).fetchall())
        e = len(await (await self.db.execute("SELECT * FROM users WHERE first_time > ?", (time.time() - 7*86400,))).fetchall())
        f = len(await (await self.db.execute("SELECT * FROM users WHERE first_time > ?", (time.time() - 30*86400,))).fetchall())
        g = len(await (await self.db.execute("SELECT * FROM users WHERE banned = 1")).fetchall())
        h = len(await (await self.db.execute("SELECT * FROM users")).fetchall())
        return a, b, c, d, e, f, g, h
    
    async def get_all_users(self):
        return await (await self.db.execute("SELECT * FROM users")).fetchall()

    async def update_banned(self, user_id, banned):
        await self.db.execute("UPDATE users SET banned = ? WHERE user_id = ?", (banned, user_id))
        await self.db.commit()

db = DataBase("db.db")