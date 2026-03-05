import sqlite3
from config import DATABASE_PATH


class ProductModel:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            stock INTEGER NOT NULL,
            min_threshold INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def add_product(self, name, stock, min_threshold):
        # Check if product with same name already exists
        query_check = 'SELECT * FROM products WHERE name = ?'
        cur = self.conn.cursor()
        cur.execute(query_check, (name,))
        existing = cur.fetchone()
        
        if existing:
            # Product exists, add to existing stock
            new_stock = existing['stock'] + stock
            query_update = 'UPDATE products SET stock = ? WHERE name = ?'
            cur.execute(query_update, (new_stock, name))
            self.conn.commit()
            return existing['id']
        else:
            # Find lowest available ID
            query_max = 'SELECT MAX(id) as max_id FROM products'
            cur.execute(query_max)
            result = cur.fetchone()
            max_id = result['max_id'] if result['max_id'] else 0
            
            # Check for gaps in IDs
            for check_id in range(1, max_id + 2):
                query_check_id = 'SELECT id FROM products WHERE id = ?'
                cur.execute(query_check_id, (check_id,))
                if not cur.fetchone():
                    # Found available ID
                    query = 'INSERT INTO products (id, name, stock, min_threshold) VALUES (?, ?, ?, ?)'
                    cur.execute(query, (check_id, name, stock, min_threshold))
                    self.conn.commit()
                    return check_id
            
            # Fallback: use max_id + 1
            new_id = max_id + 1
            query = 'INSERT INTO products (id, name, stock, min_threshold) VALUES (?, ?, ?, ?)'
            cur.execute(query, (new_id, name, stock, min_threshold))
            self.conn.commit()
            return new_id

    def get_all_products(self):
        query = 'SELECT * FROM products'
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()

    def get_product(self, product_id):
        query = 'SELECT * FROM products WHERE id = ?'
        cur = self.conn.cursor()
        cur.execute(query, (product_id,))
        return cur.fetchone()

    def get_product_by_name(self, name):
        query = 'SELECT * FROM products WHERE name = ?'
        cur = self.conn.cursor()
        cur.execute(query, (name,))
        return cur.fetchone()

    def update_product(self, product_id, name, stock, min_threshold):
        query = 'UPDATE products SET name = ?, stock = ?, min_threshold = ? WHERE id = ?'
        self.conn.execute(query, (name, stock, min_threshold, product_id))
        self.conn.commit()

    def delete_product(self, product_id):
        query = 'DELETE FROM products WHERE id = ?'
        self.conn.execute(query, (product_id,))
        self.conn.commit()
