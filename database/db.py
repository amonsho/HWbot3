import asyncpg

class DatabaseConfig:
    def __init__(self, user, password, db_name, port=5432, host='localhost'):
        self.user=user
        self.password=password
        self.db_name=db_name
        self.port=port
        self.host=host
        self.pool=None

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(
                user = self.user,
                password = self.password,
                database = self.db_name,
                port = self.port,
                host = self.host
            )
        except Exception as e:
            print('Error from connect',e)

    async def close(self):
        await self.pool.close()

    async def create_tables(self):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            tg_id BIGINT UNIQUE NOT NULL,
            fullname VARCHAR(100) NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE                       
            );
                                   
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            author VARCHAR(150),
            year INT
            );
                                   
        CREATE TABLE IF NOT EXISTS reviews (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(id) ON DELETE CASCADE,
            book_id INT REFERENCES books(id) ON DELETE CASCADE,
            review_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
            );
    """)
        except Exception as e:
            print('Error from create tables', e)

    
db = DatabaseConfig(
    user='postgres',
    password='Am.on$sh_op',
    db_name='book_club_bot'
)