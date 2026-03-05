# 🎯 Smart Inventory Management System

A complete Python Flask-based inventory management system with sales analytics, reorder suggestions, and real-time dashboard.

## 📋 Features

✅ **Product Management** - Add, edit, delete products  
✅ **Sales Tracking** - Record sales and auto-update stock  
✅ **Low Stock Detection** - Automatic alerts for low inventory  
✅ **Smart Reorder Suggestions** - AI-calculated reorder quantities  
✅ **Sales Analytics Dashboard** - Charts, trends, top sellers  
✅ **Beautiful UI** - Bootstrap + custom CSS design  
✅ **Database** - SQLite with ID reuse optimization  

## 🚀 Quick Start

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Run the Application
```bash
# From the project root directory:
python app.py
```

**OR use the run script:**
```bash
python run.py
```

### 3️⃣ Access the Application
Open your browser and go to: `http://127.0.0.1:5000`

### 4️⃣ Load Sample Data (Optional)
To populate with test data:
```bash
python seed_data.py
```

## 📊 Main Features & Routes

| Feature | URL | Description |
|---------|-----|-------------|
| **Dashboard** | `/` | View all products, inventory status, sales chart |
| **Add Product** | `/product/add` | Add new product or increase stock of existing |
| **Edit Product** | `/product/edit/<id>` | Modify product details |
| **Record Sale** | `/sale` | Record a product sale (auto-updates stock) |
| **Recommendations** | `/recommendations` | Low stock alerts & reorder suggestions |
| **Analytics** | `/analytics` | Sales insights with charts & trends |

## 🗂️ Project Structure

```
smart_inventory_system/
├── app.py                 # Flask application entry point
├── config.py             # Configuration settings
├── run.py                # Run script (alternative launcher)
├── requirements.txt      # Python dependencies
├── seed_data.py          # Sample data generator
│
├── database/
│   └── inventory.db      # SQLite database (auto-created)
│
├── models/
│   ├── __init__.py
│   ├── product_model.py  # Product database operations
│   └── sales_model.py    # Sales database operations
│
├── services/
│   ├── __init__.py
│   └── inventory_service.py  # Business logic layer
│
├── routes/
│   ├── __init__.py
│   └── inventory_routes.py   # Flask routes
│
├── utils/
│   ├── __init__.py
│   └── reorder_algorithm.py  # Reorder calculation logic
│
├── templates/
│   ├── base.html         # Base template with navbar
│   ├── dashboard.html    # Main dashboard
│   ├── add_product.html  # Add/edit product form
│   ├── sales.html        # Record sale form
│   ├── recommendations.html  # Alerts & reorder suggestions
│   └── sales_insights.html   # Analytics with charts
│
├── static/
│   ├── css/styles.css    # Custom CSS
│   └── js/scripts.js     # Client-side scripts
│
└── tests/
    └── test_inventory.py # Unit tests
```

## 🔧 How to Use

### Adding a Product
1. Click "Add Product" in navbar
2. Enter product name, current stock, minimum threshold
3. Click "Add" - system will merge if product exists
4. Stock updates automatically

### Recording a Sale
1. Click "Record Sale" in navbar
2. Select product and quantity
3. Click "Record" - stock updates automatically
4. View updated values on dashboard

### Viewing Analytics
1. Click "Analytics" in navbar
2. See:
   - 📊 Which products sell the most
   - 📈 Daily sales trends
   - 🏆 Top performers ranked
   - 💡 Sales insights with status badges

### Reorder Suggestions
1. Click "Recommendations" in navbar
2. View:
   - ⚠️ Items currently low in stock
   - 📋 How many units to reorder based on sales trends
   - Formula: `(avg_daily_sales × lead_time_days) - current_stock`

## 💾 Database Schema

### Products Table
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    stock INTEGER NOT NULL,
    min_threshold INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
```

### Sales Table
```sql
CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    sale_date TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(product_id) REFERENCES products(id)
)
```

## 🤖 Reorder Algorithm

The system calculates reorder quantities using:

```
reorder_quantity = (average_daily_sales × lead_time_days) - current_stock
```

**Example:**
- Average daily sales: 2 units
- Lead time: 7 days
- Current stock: 5 units
- Reorder: (2 × 7) - 5 = 9 units

## ⚡ Special Features

### ID Reuse
When you delete a product, its ID is reused for the next new product. This keeps IDs compact and organized.

### Duplicate Product Handling
If you add a product with an existing name, the system automatically merges the stock instead of creating duplicates.

### Low Stock Detection
Products below their minimum threshold are:
- Highlighted in red on dashboard
- Flagged in recommendations
- Listed in analytics with ⚠️ status

## 🧪 Testing

Run the test suite:
```bash
python -m unittest tests/test_inventory.py
```

Expected output:
```
Ran 5 tests in 0.280s
OK
```

## 🎨 UI Components

- **Bootstrap 4.5** - Responsive grid & components
- **Chart.js 3** - Beautiful data visualizations
- **Custom CSS** - Modern card-based design
- **Color Coding** - Status indicators (🔥 seller, ⚠️ low stock)

## 📱 Responsive Design

All pages are fully responsive and work on:
- 💻 Desktop browsers
- 📱 Tablets
- 📵 Mobile devices

## ⚙️ Configuration

Edit `config.py` to customize:
```python
DEBUG = True              # Debug mode
SECRET_KEY = 'your_key'   # Flask secret
DATABASE_PATH = '...'     # Database location
```

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'services'"
**Solution:** Always run from the project root:
```bash
cd "e:\4th year\HCL Training\inventory\smart_inventory_system"
python app.py
```

### Port 5000 already in use
**Solution:** Use a different port:
```python
app.run(port=5001)
```

### Database locked error
**Solution:** Ensure only one instance is running

## 📦 Dependencies

- **Flask** 2.0.1 - Web framework
- **SQLite3** - Built-in with Python
- **Jinja2** - Template engine (with Flask)
- **Chart.js** - CDN-loaded, no installation needed

## 🎓 Learning Resources

- Flask documentation: https://flask.palletsprojects.com/
- SQLite tutorial: https://www.sqlitetutorial.net/
- Chart.js docs: https://www.chartjs.org/

## 👨‍💼 Developer Notes

- Clean modular architecture separates concerns
- Service layer handles all business logic
- Models handle database operations
- Routes handle HTTP requests/responses
- Utility functions for algorithms

## 📄 License

This project is free to use for educational and commercial purposes.

---

**Created with ❤️ for efficient inventory management**

Need help? Check the inline code comments or run tests to verify functionality.
