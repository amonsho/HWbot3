from .db import DatabaseConfig

class Book:
    def __init__(self, db:DatabaseConfig):
        self.db = db

    async def add_books(self,title,author, year):
        try:
            async with self.db.pool.acquire() as conn :
                await conn.execute("""
            INSERT INTO books (title, author, year)
            VALUES($1, $2, $3)
        """,title,author, year)
        except Exception as e:
            print('Error from add books',e)

    async def delete_books(self,book_id):
        try:
            async with self.db.pool.acquire() as conn:
                await conn.execute("""
            DELETE FROM books WHERE id = $1
        """,book_id)
        except Exception as e:
            print('Error from delete books',e)
                
    async def get_books(self):
        try:
            async with self.db.pool.acquire() as conn:
                books = await conn.fetch("""
            SELECT * FROM books ORDER BY id
        """)
            return books
        except Exception as e:
            print('Error from get books',e)
        
