from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.inventory_service import InventoryService
from datetime import datetime

inventory_bp = Blueprint('inventory', __name__)
service = InventoryService()


# ==============================
# Dashboard
# ==============================
@inventory_bp.route('/')
def dashboard():

    products = service.get_all_products()
    sales = service.get_sales()

    sales_data = {}

    for s in sales:
        date_str = datetime.strptime(
            s['sale_date'], '%Y-%m-%d %H:%M:%S'
        ).strftime('%Y-%m-%d')

        sales_data[date_str] = sales_data.get(date_str, 0) + s['quantity']

    labels = list(sales_data.keys())
    values = list(sales_data.values())

    return render_template(
        'dashboard.html',
        products=products,
        labels=labels,
        values=values
    )


# ==============================
# Add Product
# ==============================
@inventory_bp.route('/product/add', methods=['GET', 'POST'])
def add_product():

    if request.method == 'POST':

        name = request.form.get('name')
        stock = int(request.form.get('stock'))
        min_threshold = int(request.form.get('min_threshold'))

        existing = service.product_model.get_product_by_name(name)

        if existing:
            flash(f'Product "{name}" already exists. Stock updated.', 'info')
        else:
            flash('Product added successfully', 'success')

        service.add_product(name, stock, min_threshold)

        return redirect(url_for('inventory.dashboard'))

    return render_template('add_product.html')


# ==============================
# Edit Product
# ==============================
@inventory_bp.route('/product/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):

    product = service.get_product(product_id)

    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('inventory.dashboard'))

    if request.method == 'POST':

        name = request.form.get('name')
        stock = int(request.form.get('stock'))
        min_threshold = int(request.form.get('min_threshold'))

        service.update_product(product_id, name, stock, min_threshold)

        flash('Product updated successfully', 'success')

        return redirect(url_for('inventory.dashboard'))

    return render_template('add_product.html', product=product)


# ==============================
# Delete Product
# ==============================
@inventory_bp.route('/product/delete/<int:product_id>')
def delete_product(product_id):

    service.delete_product(product_id)

    flash('Product deleted', 'info')

    return redirect(url_for('inventory.dashboard'))


# ==============================
# Record Sale
# ==============================
@inventory_bp.route('/sale', methods=['GET', 'POST'])
def record_sale():

    products = service.get_all_products()

    if request.method == 'POST':

        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity'))

        try:
            service.record_sale(product_id, quantity)
            flash('Sale recorded successfully', 'success')

        except ValueError as e:
            flash(str(e), 'danger')

        return redirect(url_for('inventory.dashboard'))

    return render_template('sales.html', products=products)


# ==============================
# Recommendations
# ==============================
@inventory_bp.route('/recommendations')
def recommendations():

    low_stock = service.low_stock_products()
    suggestions = service.reorder_suggestions()

    return render_template(
        'recommendations.html',
        low_stock=low_stock,
        suggestions=suggestions
    )


# ==============================
# Analytics Dashboard
# ==============================
@inventory_bp.route('/analytics')
def analytics():

    products = service.get_all_products()
    all_sales = service.get_sales()

    # ------------------------------
    # Sales by Product
    # ------------------------------
    product_sales_map = {}

    for s in all_sales:

        product_id = s['product_id']

        product_sales_map[product_id] = (
            product_sales_map.get(product_id, 0) + s['quantity']
        )

    top_sellers = []

    for p in products:

        total_sold = product_sales_map.get(p['id'], 0)

        top_sellers.append({
            'id': p['id'],
            'name': p['name'],
            'total_sold': total_sold,
            'stock': p['stock'],
            'min_threshold': p['min_threshold']
        })

    top_sellers.sort(key=lambda x: x['total_sold'], reverse=True)

    product_names = [ts['name'] for ts in top_sellers]
    product_sales = [ts['total_sold'] for ts in top_sellers]

    # ------------------------------
    # Sales Trend (Daily)
    # ------------------------------
    sales_data = {}

    for s in all_sales:

        date_str = datetime.strptime(
            s['sale_date'], '%Y-%m-%d %H:%M:%S'
        ).strftime('%Y-%m-%d')

        sales_data[date_str] = sales_data.get(date_str, 0) + s['quantity']

    sorted_dates = sorted(sales_data.keys())

    date_labels = sorted_dates
    daily_sales = [sales_data[d] for d in sorted_dates]

    # ------------------------------
    # Summary Statistics
    # ------------------------------
    total_units_sold = sum(product_sales)
    total_products = len(products)
    total_sales_count = len(all_sales)

    low_stock_items = service.low_stock_products()
    low_stock_count = len(low_stock_items)

    return render_template(
        'sales_insights.html',
        product_names=product_names,
        product_sales=product_sales,
        date_labels=date_labels,
        daily_sales=daily_sales,
        top_sellers=top_sellers,
        total_units_sold=total_units_sold,
        total_products=total_products,
        total_sales_count=total_sales_count,
        low_stock_count=low_stock_count
    )