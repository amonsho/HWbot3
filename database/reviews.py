from .db import DatabaseConfig

class Review:
    def __init__(self,db:DatabaseConfig):
        self.db=db

    
    async def add_review(self, user_id, book_id, review_text):
        try:
            async with self.db.pool.acquire() as conn:
                await conn.execute("""
            INSERT INTO reviews (user_id, book_id, review_text)
            VALUES($1, $2, $3)
        """,user_id, book_id, review_text)
        except Exception as e:
            print('Error from add review',e)
    @staticmethod
    async def get_user_review(db:DatabaseConfig,user_id:int):
        try:
            async with db.pool.acquire() as conn:
                review = await conn.fetch("""
            SELECT r.id, b.title, r.review_text, r.created_at FROM reviews r
            JOIN books b ON r.book_id = b.id
            WHERE r.user_id = $1
            ORDER BY r.created_at DESC
        """,user_id)
                return review
        except Exception as e:
            print('Error from get user review',e)

    async def get_all_reviews(self):
        try:
            async with self.db.pool.acquire() as conn:
                all_r = await conn.fetch("""
            SELECT u.fullname, b.title, r.review_text, r.created_at FROM reviews r
            JOIN users u ON r.user_id = u.id
            JOIN books b ON r.book_id = b.id
            ORDER BY r.created_at DESC
        """)
                return all_r
        except Exception as e:
            print('Error from get all reviews',e)
            