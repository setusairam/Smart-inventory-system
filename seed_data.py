"""
Seed script to populate database with sample test data
Run with: python seed_data.py
"""

from models.product_model import ProductModel
from models.sales_model import SalesModel
from datetime import datetime, timedelta
import random

def seed_database():
    product_model = ProductModel()
    sales_model = SalesModel()
    
    # Sample products in different categories
    products = [
        # Groceries
        {'name': 'Rice (5kg)', 'stock': 50, 'min_threshold': 10},
        {'name': 'Milk (1L)', 'stock': 40, 'min_threshold': 15},
        {'name': 'Bread', 'stock': 30, 'min_threshold': 10},
        {'name': 'Eggs (Dozen)', 'stock': 25, 'min_threshold': 8},
        {'name': 'Chicken (1kg)', 'stock': 20, 'min_threshold': 5},
        
        # Electronics
        {'name': 'Laptop', 'stock': 8, 'min_threshold': 3},
        {'name': 'Mobile Phone', 'stock': 15, 'min_threshold': 5},
        {'name': 'Headphones', 'stock': 25, 'min_threshold': 8},
        {'name': 'USB Cable', 'stock': 100, 'min_threshold': 30},
        {'name': 'Charger', 'stock': 12, 'min_threshold': 4},
        
        # Daily Used Items
        {'name': 'Soap', 'stock': 80, 'min_threshold': 20},
        {'name': 'Toothpaste', 'stock': 35, 'min_threshold': 10},
        {'name': 'Shampoo', 'stock': 45, 'min_threshold': 12},
        {'name': 'Tissue Paper', 'stock': 60, 'min_threshold': 15},
        {'name': 'Hand Sanitizer', 'stock': 40, 'min_threshold': 10},
    ]
    
    print("Adding sample products...")
    for product in products:
        product_model.add_product(product['name'], product['stock'], product['min_threshold'])
    
    print(f"Added {len(products)} products!")
    
    # Add sample sales data for the last 14 days to show trends
    print("\nAdding sample sales data...")
    all_products = product_model.get_all_products()
    
    for i in range(14):  # Last 14 days
        date = datetime.now() - timedelta(days=i)
        # Random number of sales per day (1-5 sales)
        num_sales = random.randint(1, 5)
        
        for _ in range(num_sales):
            product = random.choice(all_products)
            quantity = random.randint(1, 5)
            
            # Record sale with specific date
            cur = sales_model.conn.cursor()
            query = 'INSERT INTO sales (product_id, quantity, sale_date) VALUES (?, ?, ?)'
            cur.execute(query, (product['id'], quantity, date.strftime('%Y-%m-%d %H:%M:%S')))
            sales_model.conn.commit()
    
    print(f"Added sales data for last 14 days!")
    
    print("\n✅ Database seeded successfully!")
    print("\nSample data overview:")
    for p in product_model.get_all_products():
        print(f"  • {p['name']}: {p['stock']} units (Min: {p['min_threshold']})")

if __name__ == '__main__':
    seed_database()
