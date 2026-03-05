import sqlite3
from config import DATABASE_PATH


class SalesModel:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            sale_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def record_sale(self, product_id, quantity):
        query = 'INSERT INTO sales (product_id, quantity) VALUES (?, ?)'
        cur = self.conn.cursor()
        cur.execute(query, (product_id, quantity))
        self.conn.commit()
        return cur.lastrowid

    def get_sales_by_product(self, product_id):
        query = 'SELECT * FROM sales WHERE product_id = ? ORDER BY sale_date ASC'
        cur = self.conn.cursor()
        cur.execute(query, (product_id,))
        return cur.fetchall()

    def get_all_sales(self):
        query = 'SELECT * FROM sales ORDER BY sale_date ASC'
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()
