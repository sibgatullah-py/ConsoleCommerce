# THIS FILE IS CREATED BY AI FOR TESTING PURPOSE IT"S NOT THE FINAL main.py FILE

import sys
from core.database import DatabaseManager
from core.models.user import User
from core.models.product import Product
from core.models.order import Order

# -------- Utility helpers --------
def pause():
    input("\nPress ENTER to continue...")

def clear():
    print("\033c", end="")

# --------- Menus ---------
def admin_menu(user, db, user_model, product_model, order_model):
    while True:
        clear()
        print(f"👑 ADMIN PANEL — Logged in as {user['username']}")
        print("=" * 40)
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. View Orders")
        print("6. Logout")
        print("=" * 40)
        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Product name: ")
            price = float(input("Price: "))
            stock = int(input("Stock: "))
            desc = input("Description: ")
            product_model.add_product(name, price, stock, desc)
            pause()

        elif choice == "2":
            products = product_model.list_products()
            if not products:
                print("No products found.")
            else:
                for p in products:
                    print(f"[{p['id']}] {p['name']} — ${p['price']} (Stock: {p['stock']})")
            pause()

        elif choice == "3":
            products = product_model.list_products()
            for p in products:
                print(f"[{p['id']}] {p['name']} — ${p['price']} (Stock: {p['stock']})")
                
            pid = int(input("Enter product ID to update: "))
            name = input("New name (leave empty to skip): ") or None
            price = input("New price (leave empty to skip): ")
            stock = input("New stock (leave empty to skip): ")
            desc = input("New description (leave empty to skip): ") or None

            product_model.update_product(
                pid,
                name=name,
                price=float(price) if price else None,
                stock=int(stock) if stock else None,
                description=desc,
            )
            pause()

        elif choice == "4":
            pid = int(input("Enter product ID to delete: "))
            product_model.delete_product(pid)
            pause()

        elif choice == "5":
            orders = order_model.get_all_orders()
            if not orders:
                print("No orders yet.")
            else:
                for o in orders:
                    print(f"Order {o['id']} | User {o['user_id']} | Items: {o['items']} | Status: {o['status']}")
            pause()

        elif choice == "6":
            print("Logging out...")
            pause()
            break

        else:
            print("Invalid choice.")
            pause()


def customer_menu(user, db, user_model, product_model, order_model):
    while True:
        clear()
        print(f"🛒 CUSTOMER MENU — Logged in as {user['username']}")
        print("=" * 40)
        print("1. View Products")
        print("2. Search Products")
        print("3. Place Order")
        print("4. View My Orders")
        print("5. Logout")
        print("=" * 40)
        choice = input("Enter choice: ")

        if choice == "1":
            products = product_model.list_products()
            if not products:
                print("No products available.")
            else:
                for p in products:
                    print(f"[{p['id']}] {p['name']} — ${p['price']} (Stock: {p['stock']})")
            pause()

        elif choice == "2":
            keyword = input("Enter search keyword: ")
            results = product_model.search_products(keyword)
            if not results:
                print("No matching products found.")
            else:
                for r in results:
                    print(f"[{r['id']}] {r['name']} — ${r['price']}")
            pause()

        elif choice == "3":
            products = product_model.list_products()
            for p in products:
                print(f"[{p['id']}] {p['name']} — ${p['price']} (Stock: {p['stock']})")
            print("Choose the product you want to order")
            pid = int(input("Product ID to order: "))
            qty = int(input("Quantity: "))
            product = product_model.get_by_id(pid)
            if not product:
                print("Invalid product.")
            elif product["stock"] < qty:
                print("Not enough in stock!")
            else:
                order_model.create_order(user["id"], [{"product_id": pid, "qty": qty}])
                product_model.reduce_stock(pid, qty)
            pause()

        elif choice == "4":
            orders = order_model.get_user_orders(user["id"])
            if not orders:
                print("You have no orders yet.")
            else:
                for o in orders:
                    print(f"Order {o['id']} | Items: {o['items']} | Status: {o['status']}")
            pause()

        elif choice == "5":
            print("Logging out...")
            pause()
            break

        else:
            print("Invalid choice.")
            pause()


def main_menu():
    with DatabaseManager() as db:
        user_model = User(db)
        product_model = Product(db)
        order_model = Order(db)

        while True:
            clear()
            print("🧭 ConsoleCommerce Main Menu")
            print("=" * 40)
            print("1. Login")
            print("2. Register")
            print("3. Exit")
            print("=" * 40)

            choice = input("Enter choice: ")

            if choice == "1":
                username = input("Username: ")
                password = input("Password: ")
                user = user_model.validate_login(username, password)
                if user:
                    if user["role"] == "admin":
                        admin_menu(user, db, user_model, product_model, order_model)
                    else:
                        customer_menu(user, db, user_model, product_model, order_model)

            elif choice == "2":
                username = input("Choose username: ")
                password = input("Choose password: ")
                user_model.register(username, password)

            elif choice == "3":
                print("👋 Exiting ConsoleCommerce.")
                sys.exit(0)

            else:
                print("Invalid choice.")
                pause()


if __name__ == "__main__":
    main_menu()
