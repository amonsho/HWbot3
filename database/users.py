from .db import db


class User:
    def __init__(self, tg_id, fullname, db):
        self.tg_id = tg_id
        self.fullname = fullname
        self.db = db

    async def add_user(self):
        try:
            async with self.db.pool.acquire() as conn:
                await conn.execute("""
        INSERT INTO users (tg_id, fullname)
        VALUES($1, $2)
        """,self.tg_id, self.fullname)
        except Exception as e:
            print('Error from add users', e)

    async def get_user(self) -> bool:
        try:
            async with self.db.pool.acquire() as conn:
                user = await conn.fetchrow("""
        SELECT id FROM users WHERE tg_id = $1
    """,self.tg_id)
                return True if user else False
        except Exception as e:
            print('Error from get user',e)

    async def check_status(self):
        try:
            async with self.db.pool.acquire() as conn:
                is_admin = await conn.fetchrow("""
        SELECT is_admin FROM users WHERE tg_id = $1
    """,self.tg_id)
                return is_admin['is_admin'] if is_admin else False
        except Exception as e:
            print('error from check status',e)

    async def get_user_row(self):
        try:
            async with self.db.pool.acquire() as conn:
                user = await conn.fetchrow(
                "SELECT * FROM users WHERE tg_id = $1", self.tg_id
                )
            return user
        except Exception as e:
            print("❌ Error get_user_row:", e)
            