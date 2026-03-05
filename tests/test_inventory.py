import unittest
from services.inventory_service import InventoryService


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.service = InventoryService()
        # start with fresh DB by deleting existing products for testing
        products = self.service.get_all_products()
        for p in products:
            self.service.delete_product(p['id'])

    def test_add_and_get_product(self):
        pid = self.service.add_product('Test', 10, 2)
        prod = self.service.get_product(pid)
        self.assertIsNotNone(prod)
        self.assertEqual(prod['name'], 'Test')

    def test_record_sale_updates_stock(self):
        pid = self.service.add_product('Test', 10, 2)
        self.service.record_sale(pid, 3)
        prod = self.service.get_product(pid)
        self.assertEqual(prod['stock'], 7)

    def test_low_stock_detection(self):
        pid = self.service.add_product('Test', 1, 5)
        low = self.service.low_stock_products()
        self.assertTrue(any(p['id'] == pid for p in low))

    def test_reorder_suggestion(self):
        pid = self.service.add_product('Test', 1, 5)
        # simulate sales history
        self.service.record_sale(pid, 1)
        suggestions = self.service.reorder_suggestions(lead_time_days=1)
        self.assertTrue(any(s['product']['id'] == pid for s in suggestions))


    def test_recommendations_route(self):
        # ensure Flask app can render recommendations page
        from app import create_app
        app = create_app()
        with app.test_client() as client:
            resp = client.get('/recommendations')
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Inventory Recommendations', resp.data)


if __name__ == '__main__':
    unittest.main()