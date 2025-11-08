"""
===============================================================================
CONSOLE COMMERCE - INTERACTIVE E-COMMERCE APPLICATION
===============================================================================

A fully interactive console-based e-commerce application where you can:
    - Register and login as a customer or admin
    - Browse and search products
    - Add items to cart and checkout
    - View your order history
    - Admin: Manage products, orders, and users

Use this like a website - navigate through menus and interact with the system!
===============================================================================
"""

import os
import sys
from core.database import DatabaseManager
from core.models.user import User
from core.models.product import Product
from core.models.order import Order
from core.services.auth_service import AuthService
from core.services.cart_service import CartService
from core.services.admin_service import AdminService


def clear_screen():
    """Clear the console screen for better UX."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_menu(options: dict):
    """Print a menu with numbered options."""
    print("\nOptions:")
    for key, value in options.items():
        print(f"  {key}. {value}")
    print()


def get_user_input(prompt: str, input_type=str):
    """Get user input with type conversion."""
    try:
        value = input(prompt).strip()
        if input_type == int:
            return int(value)
        elif input_type == float:
            return float(value)
        return value
    except (ValueError, KeyboardInterrupt):
        return None


def display_products(products, show_stock=True):
    """Display a list of products in a formatted table."""
    if not products:
        print("\nNo products found.")
        return
    
    print("\n" + "-" * 70)
    print(f"{'ID':<5} {'Name':<25} {'Price':<12} {'Stock':<8} {'Description':<20}")
    print("-" * 70)
    
    for product in products:
        stock_display = f"{product['stock']}" if show_stock else "N/A"
        desc = (product['description'][:17] + "...") if product['description'] and len(product['description']) > 20 else (product['description'] or "")
        print(f"{product['id']:<5} {product['name']:<25} tk{product['price']:<11.2f} {stock_display:<8} {desc:<20}")
    print("-" * 70)


def display_orders(orders):
    """Display a list of orders."""
    if not orders:
        print("\nNo orders found.")
        return
    
    for order in orders:
        print(f"\n{'='*70}")
        print(f"Order ID: {order['id']} | Status: {order['status'].upper()} | Date: {order['created_at']}")
        print(f"{'-'*70}")
        total = 0
        for item in order['items']:
            subtotal = item['price'] * item['qty']
            total += subtotal
            print(f"  {item['name']:<30} x{item['qty']:<3} @ tk{item['price']:.2f} = tk{subtotal:.2f}")
        print(f"{'-'*70}")
        print(f"Total: tk{total:.2f}")
        print(f"{'='*70}")


def customer_menu(db, auth_service, cart_service, product_model, order_model):
    """Main menu for logged-in customers."""
    while True:
        user = auth_service.get_logged_in_user()
        if not user:
            break
        
        print_header(f"Welcome, {user['username']}! (Customer)")
        print_menu({
            "1": "Browse Products",
            "2": "Search Products",
            "3": "View Cart",
            "4": "Add to Cart",
            "5": "Remove from Cart",
            "6": "Checkout",
            "7": "My Orders",
            "8": "Logout"
        })
        
        choice = get_user_input("Enter your choice: ", int)
        
        if choice == 1:
            # Browse Products
            clear_screen()
            print_header("Browse Products")
            products = product_model.list_products()
            display_products(products)
            input("\nPress Enter to continue...")
            clear_screen()
        
        elif choice == 2:
            # Search Products
            clear_screen()
            print_header("Search Products")
            keyword = get_user_input("Enter search keyword: ")
            if keyword:
                results = product_model.search_products(keyword)
                display_products(results)
            else:
                print("Invalid keyword.")
            input("\nPress Enter to continue...")
            clear_screen()
        
        elif choice == 3:
            # View Cart
            clear_screen()
            print_header("Your Shopping Cart")
            cart_service.view_cart(user['id'])
            input("\nPress Enter to continue...")
            clear_screen()
        
        elif choice == 4:
            # Add to Cart
            clear_screen()
            print_header("Add to Cart")
            products = product_model.list_products()
            display_products(products)
            
            product_id = get_user_input("\nEnter product ID to add: ", int)
            if product_id:
                qty = get_user_input("Enter quantity: ", int) or 1
                cart_service.add_to_cart(user['id'], product_id, qty)
            else:
                print("Invalid product ID.")
            input("\nPress Enter to continue...")
            clear_screen()
        
        elif choice == 5:
            # Remove from Cart
            clear_screen()
            print_header("Remove from Cart")
            cart = cart_service.view_cart(user['id'])
            if cart:
                product_id = get_user_input("\nEnter product ID to remove: ", int)
                if product_id:
                    cart_service.remove_from_cart(user['id'], product_id)
                else:
                    print("Invalid product ID.")
            input("\nPress Enter to continue...")
            clear_screen()
        
        elif choice == 6:
            # Checkout
            clear_screen()
            print_header("Checkout")
            cart_service.view_cart(user['id'])
            confirm = get_user_input("\nProceed with checkout? (yes/no): ").lower()
            if confirm == 'yes':
                # The checkout method now handles stock reduction internally
                # It will check stock availability and reduce stock automatically
                cart_service.checkout(user['id'])
            else:
                print("Checkout cancelled.")
            input("\nPress Enter to continue...")
            clear_screen()
        
        elif choice == 7:
            # My Orders
            clear_screen()
            print_header("My Orders")
            orders = order_model.get_user_orders(user['id'])
            display_orders(orders)
            input("\nPress Enter to continue...")
            clear_screen()
        
        elif choice == 8:
            # Logout
            auth_service.logout_user()
            print("\nLogged out successfully!")
            input("Press Enter to continue...")
            clear_screen()
            break
        
        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")
            clear_screen()


def admin_menu(db, auth_service, admin_service, product_model, order_model, user_model):
    """Main menu for admin users."""
    while True:
        user = auth_service.get_logged_in_user()
        if not user or not auth_service.is_admin():
            break
        
        print_header(f"Admin Panel - {user['username']}")
        print_menu({
            "1": "View All Products",
            "2": "Add Product",
            "3": "Update Product",
            "4": "Delete Product",
            "5": "Manage Stock",
            "6": "View All Orders",
            "7": "Update Order Status",
            "8": "Cancel Order",
            "9": "View All Users",
            "10": "Promote User to Admin",
            "11": "Logout"
        })
        
        choice = get_user_input("Enter your choice: ", int)
        
        if choice == 1:
            # View All Products
            clear_screen()
            print_header("All Products")
            products = product_model.list_products()
            display_products(products)
            input("\nPress Enter to continue...")
            clear_screen()
        
        elif choice == 2:
            # Add Product
            clear_screen()
            print_header("Add New Product")
            name = get_user_input("Product name: ")
            if name:
                price = get_user_input("Price: ", float)
                stock = get_user_input("Stock quantity: ", int) or 0
                description = get_user_input("Description: ") or ""
                if price:
                    admin_service.add_product(name, price, stock, description)
            input("\nPress Enter to continue...")
            clear_screen()
        
        elif choice == 3:
            # Update Product
            clear_screen()
            print_header("Update Product")
            products = product_model.list_products()
            display_products(products)
            
            product_id = get_user_input("\nEnter product ID to update: ", int)
            if product_id:
                print("\nLeave blank to skip updating a field:")
                name = get_user_input("New name: ") or None
                price_str = get_user_input("New price: ")
                price = float(price_str) if price_str else None
                stock_str = get_user_input("New stock: ")
                stock = int(stock_str) if stock_str else None
                description = get_user_input("New description: ") or None
                
                admin_service.update_product(product_id, name, price, stock, description)
            input("\nPress Enter to continue...")
            clear_screen()
        
        elif choice == 4:
            # Delete Product
            clear_screen()
            print_header("Delete Product")
            products = product_model.list_products()
            display_products(products)
            
            product_id = get_user_input("\nEnter product ID to delete: ", int)
            if product_id:
                confirm = get_user_input("Are you sure? (yes/no): ").lower()
                if confirm == 'yes':
                    admin_service.delete_product(product_id)
            input("\nPress Enter to continue...")
            clear_screen()
        
        elif choice == 5:
            # Manage Stock
            clear_screen()
            print_header("Manage Stock")
            products = product_model.list_products()
            display_products(products)
            
            product_id = get_user_input("\nEnter product ID: ", int)
            if product_id:
                print("\n1. Increase stock")
                print("2. Reduce stock")
                action = get_user_input("Choose action: ", int)
                qty = get_user_input("Quantity: ", int)
                
                if action == 1 and qty:
                    admin_service.increase_stock(product_id, qty)
                elif action == 2 and qty:
                    admin_service.reduce_stock(product_id, qty)
            input("\nPress Enter to continue...")
            clear_screen()
        
        elif choice == 6:
            # View All Orders
            clear_screen()
            print_header("All Orders")
            orders = admin_service.list_orders()
            display_orders(orders)
            input("\nPress Enter to continue...")
            clear_screen()
        
        elif choice == 7:
            # Update Order Status
            clear_screen()
            print_header("Update Order Status")
            orders = admin_service.list_orders()
            if orders:
                for order in orders:
                    print(f"Order ID: {order['id']} | Status: {order['status']} | User ID: {order['user_id']}")
                
                order_id = get_user_input("\nEnter order ID: ", int)
                if order_id:
                    print("\nStatus options: pending, processing, shipped, delivered, cancelled")
                    new_status = get_user_input("New status: ")
                    if new_status:
                        admin_service.update_order_status(order_id, new_status)
            input("\nPress Enter to continue...")
            clear_screen()
        
        elif choice == 8:
            # Cancel Order
            clear_screen()
            print_header("Cancel Order")
            orders = admin_service.list_orders()
            if orders:
                for order in orders:
                    print(f"Order ID: {order['id']} | Status: {order['status']} | User ID: {order['user_id']}")
                
                order_id = get_user_input("\nEnter order ID to cancel: ", int)
                if order_id:
                    confirm = get_user_input("Are you sure? (yes/no): ").lower()
                    if confirm == 'yes':
                        admin_service.cancel_order(order_id)
            input("\nPress Enter to continue...")
            clear_screen()
        
        elif choice == 9:
            # View All Users
            clear_screen()
            print_header("All Users")
            users = db.fetch_all("SELECT id, username, role, created_at FROM users")
            if users:
                print(f"\n{'ID':<5} {'Username':<20} {'Role':<10} {'Created At':<20}")
                print("-" * 70)
                for u in users:
                    print(f"{u['id']:<5} {u['username']:<20} {u['role']:<10} {u['created_at']:<20}")
            input("\nPress Enter to continue...")
            clear_screen()
        
        elif choice == 10:
            # Promote User to Admin
            clear_screen()
            print_header("Promote User to Admin")
            users = db.fetch_all("SELECT id, username, role FROM users WHERE role = 'customer'")
            if users:
                print(f"\n{'ID':<5} {'Username':<20} {'Role':<10}")
                print("-" * 70)
                for u in users:
                    print(f"{u['id']:<5} {u['username']:<20} {u['role']:<10}")
                
                user_id = get_user_input("\nEnter user ID to promote: ", int)
                if user_id:
                    admin_service.promote_user_to_admin(user_id)
            else:
                print("No customers found.")
            input("\nPress Enter to continue...")
            clear_screen()
        
        elif choice == 11:
            # Logout
            auth_service.logout_user()
            print("\nLogged out successfully!")
            input("Press Enter to continue...")
            clear_screen()
            break
        
        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")
            clear_screen()


def main_menu(db, auth_service, cart_service, product_model, order_model, admin_service, user_model):
    """Main application menu (login/register)."""
    while True:
        print_header("Console Commerce - E-Commerce Platform")
        print_menu({
            "1": "Register",
            "2": "Login",
            "3": "Browse Products (Guest)",
            "4": "Exit"
        })
        
        choice = get_user_input("Enter your choice: ", int)
        
        if choice == 1:
            # Register
            clear_screen()
            print_header("Register New Account")
            username = get_user_input("Username: ")
            password = get_user_input("Password: ")
            if username and password:
                role = get_user_input("Role (customer/admin) [default: customer]: ").lower() or "customer"
                if role not in ['customer', 'admin']:
                    role = 'customer'
                success = auth_service.register_user(username, password, role)
                if success:
                    print("\nRegistration successful! Please login.")
            input("\nPress Enter to continue...")
            clear_screen()
        
        elif choice == 2:
            # Login
            clear_screen()
            print_header("Login")
            username = get_user_input("Username: ")
            password = get_user_input("Password: ")
            if username and password:
                success = auth_service.login_user(username, password)
                if success:
                    user = auth_service.get_logged_in_user()
                    clear_screen()
                    if auth_service.is_admin():
                        admin_menu(db, auth_service, admin_service, product_model, order_model, user_model)
                    else:
                        customer_menu(db, auth_service, cart_service, product_model, order_model)
                else:
                    print("\nLogin failed. Please check your credentials.")
                    input("Press Enter to continue...")
                    clear_screen()
        
        elif choice == 3:
            # Browse Products (Guest)
            clear_screen()
            print_header("Browse Products (Guest Mode)")
            products = product_model.list_products()
            display_products(products)
            print("\nNote: Please login to add items to cart and make purchases.")
            input("\nPress Enter to continue...")
            clear_screen()
        
        elif choice == 4:
            # Exit
            print("\nThank you for using Console Commerce!")
            print("Goodbye!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")
            clear_screen()


def main():
    """Main application entry point."""
    try:
        # Initialize database and services
        print("Initializing Console Commerce...")
        db = DatabaseManager()
        
        # Create model instances
        user_model = User(db)
        product_model = Product(db)
        order_model = Order(db)
        
        # Create service instances
        auth_service = AuthService(db)
        cart_service = CartService(db)
        admin_service = AdminService(db, auth_service)
        
        clear_screen()
        
        # Start the application
        main_menu(db, auth_service, cart_service, product_model, order_model, admin_service, user_model)
        
        # Close database connection
        db.close()
        
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
