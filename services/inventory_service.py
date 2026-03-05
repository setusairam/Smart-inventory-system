from models.product_model import ProductModel
from models.sales_model import SalesModel
from utils.reorder_algorithm import suggest_reorder


class InventoryService:
    def __init__(self):
        self.product_model = ProductModel()
        self.sales_model = SalesModel()

    # Product operations
    def add_product(self, name, stock, min_threshold):
        return self.product_model.add_product(name, stock, min_threshold)

    def get_all_products(self):
        return self.product_model.get_all_products()

    def get_product(self, product_id):
        return self.product_model.get_product(product_id)

    def update_product(self, product_id, name, stock, min_threshold):
        return self.product_model.update_product(product_id, name, stock, min_threshold)

    def delete_product(self, product_id):
        return self.product_model.delete_product(product_id)

    # Sales operations
    def record_sale(self, product_id, quantity):
        product = self.product_model.get_product(product_id)
        if not product:
            raise ValueError("Product not found")
        # Update stock
        new_stock = product["stock"] - quantity
        if new_stock < 0:
            raise ValueError("Insufficient stock for sale")
        self.product_model.update_product(product_id, product["name"], new_stock, product["min_threshold"])
        return self.sales_model.record_sale(product_id, quantity)

    def get_sales(self):
        return self.sales_model.get_all_sales()

    def get_sales_by_product(self, product_id):
        return self.sales_model.get_sales_by_product(product_id)

    # Inventory checks
    def low_stock_products(self):
        products = self.product_model.get_all_products()
        return [p for p in products if p["stock"] <= p["min_threshold"]]

    def reorder_suggestions(self, lead_time_days=7):
        suggestions = []
        products = self.product_model.get_all_products()
        for p in products:
            sales = self.sales_model.get_sales_by_product(p["id"])
            qty = suggest_reorder(sales, p["stock"], lead_time_days)
            if qty > 0:
                suggestions.append({
                    "product": p,
                    "reorder_qty": qty
                })
        return suggestions
