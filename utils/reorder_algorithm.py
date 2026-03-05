from datetime import datetime


def calculate_average_daily_sales(sales):

    if not sales:
        return 0

    dates = [
        datetime.strptime(s["sale_date"], "%Y-%m-%d %H:%M:%S")
        for s in sales
    ]

    first = min(dates)
    last = max(dates)

    days = (last - first).days + 1

    total_qty = sum(s["quantity"] for s in sales)

    if days <= 0:
        return total_qty

    return total_qty / days


def calculate_safety_stock(avg_daily_sales, lead_time_days):

    safety_factor = 1.5

    return int(avg_daily_sales * lead_time_days * safety_factor)


def suggest_reorder(sales, current_stock, lead_time_days=7):

    avg_daily = calculate_average_daily_sales(sales)

    safety_stock = calculate_safety_stock(avg_daily, lead_time_days)

    reorder_point = (avg_daily * lead_time_days) + safety_stock

    reorder_qty = int(reorder_point - current_stock)

    return max(reorder_qty, 0)