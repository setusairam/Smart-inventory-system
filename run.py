#!/usr/bin/env python
"""
Smart Inventory Management System - Run Script
Start the Flask application from here
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import init_db, create_app

if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    print("✅ Database initialized!")
    
    print("Starting Smart Inventory Management System...")
    app = create_app()
    
    print("\n" + "="*60)
    print("🚀 Server running at: http://127.0.0.1:5000")
    print("📊 Analytics at: http://127.0.0.1:5000/analytics")
    print("💼 Recommendations at: http://127.0.0.1:5000/recommendations")
    print("Press CTRL+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True)
