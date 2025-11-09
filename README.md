# Console Commerce

A simple, interactive console-based e-commerce backend system built with Python and SQLite. This project demonstrates core backend concepts including user authentication, product management, shopping cart functionality, and order processing through a clean, modular architecture.

---

##  Overview

Console Commerce is a learning-focused e-commerce application that runs entirely in the terminal. It provides a complete shopping experience with separate interfaces for customers and administrators, showcasing fundamental backend development patterns without external dependencies.

**Key Highlights:**
- Built with **Python 3** and **SQLite** (no external dependencies)
- Modular architecture separating models, services, and database layers
- Interactive console-based user interface
- Full CRUD operations for products, users, and orders
- Role-based access control (Customer/Admin)

---

##  Features

### Customer Features
-  User registration and login
-  Browse and search products
-  Add/remove items from shopping cart
-  Checkout and order creation
-  View order history
-  Guest browsing (view products without login)

### Admin Features
-  Product management (Create, Read, Update, Delete)
-  Stock management (Increase/Reduce inventory)
-  Order management (View all orders, update status, cancel orders)
-  User management (View users, promote to admin)
-  Default admin account (username: `admin`, password: `admin123`)

### Technical Features
-  Role-based authentication
-  Automatic stock reduction on checkout
-  SQLite database with automatic table creation
-  Clean separation of concerns (Models, Services, Database)
-  JSON-based order item storage

---

##  Folder Structure

```
ConsoleCommerce/
│
├── core/
│   ├── models/
│   │   ├── order.py          # Order data model and operations
│   │   ├── product.py        # Product data model and operations
│   │   └── user.py           # User data model and operations
│   │
│   ├── services/
│   │   ├── admin_service.py  # Admin-specific business logic
│   │   ├── auth_service.py   # Authentication and session management
│   │   └── cart_service.py   # Shopping cart operations
│   │
│   └── database.py           # Database connection and table management
│
├── data/
│   └── ecommerce.db          # SQLite database file (auto-created)
│
├── main.py                   # Application entry point and UI
└── README.md                 # Project documentation
```

---

##  Installation & Setup

### Prerequisites
- **Python 3.6+** (uses only built-in libraries)
- No additional packages required!

### Setup Steps

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd ConsoleCommerce
   ```

2. **Verify Python installation**
   ```bash
   python --version
   # or
   python3 --version
   ```

3. **Run the application**
   ```bash
   python main.py
   # or
   python3 main.py
   ```

4. **First-time setup**
   - The application will automatically create the `data/` directory
   - SQLite database (`ecommerce.db`) will be created automatically
   - Default admin account will be created:
     - **Username:** `admin`
     - **Password:** `admin123`

That's it! No package installation or configuration needed.

---

## ▶ Usage Instructions

### Starting the Application

Run `main.py` to launch the interactive console interface:

```bash
python main.py
```

### Main Menu Options

Upon startup, you'll see the main menu:

1. **Register** - Create a new customer or admin account
2. **Login** - Sign in with existing credentials
3. **Browse Products (Guest)** - View products without logging in
4. **Exit** - Close the application

### Customer Workflow

1. **Register/Login**
   - Choose option `1` to register a new account
   - Choose option `2` to login with existing credentials
   - Default role is `customer` (or specify `admin` during registration)

2. **Browse Products**
   - Select option `1` to view all available products
   - Select option `2` to search products by keyword

3. **Shopping Cart**
   - Select option `3` to view your cart
   - Select option `4` to add items (enter product ID and quantity)
   - Select option `5` to remove items from cart

4. **Checkout**
   - Select option `6` to proceed with checkout
   - Confirm the order to complete the purchase
   - Stock is automatically reduced upon successful checkout

5. **Order History**
   - Select option `7` to view all your past orders

6. **Logout**
   - Select option `8` to return to the main menu

### Admin Workflow

1. **Login as Admin**
   - Use the default admin account or any account with `admin` role
   - Default credentials: `admin` / `admin123`

2. **Product Management**
   - **View All Products** (option `1`) - See complete product catalog
   - **Add Product** (option `2`) - Create new products with name, price, stock, description
   - **Update Product** (option `3`) - Modify existing product details
   - **Delete Product** (option `4`) - Remove products from catalog
   - **Manage Stock** (option `5`) - Increase or reduce inventory levels

3. **Order Management**
   - **View All Orders** (option `6`) - See all customer orders
   - **Update Order Status** (option `7`) - Change order status (pending, processing, shipped, delivered, cancelled)
   - **Cancel Order** (option `8`) - Cancel specific orders

4. **User Management**
   - **View All Users** (option `9`) - List all registered users
   - **Promote User to Admin** (option `10`) - Grant admin privileges to customers

---

##  Example Workflows

### Example 1: Customer Purchase Flow

```
1. Start application: python main.py
2. Register new account:
   - Choose option 1 (Register)
   - Enter username: john_doe
   - Enter password: secure123
   - Role: customer (default)
3. Login:
   - Choose option 2 (Login)
   - Enter credentials
4. Browse products:
   - Choose option 1 (Browse Products)
   - Note product IDs you want
5. Add to cart:
   - Choose option 4 (Add to Cart)
   - Enter product ID: 1
   - Enter quantity: 2
6. View cart:
   - Choose option 3 (View Cart)
7. Checkout:
   - Choose option 6 (Checkout)
   - Confirm: yes
8. View orders:
   - Choose option 7 (My Orders)
```

### Example 2: Admin Product Management

```
1. Login as admin:
   - Username: admin
   - Password: admin123
2. Add new product:
   - Choose option 2 (Add Product)
   - Name: Laptop
   - Price: 999.99
   - Stock: 10
   - Description: High-performance laptop
3. View all products:
   - Choose option 1 (View All Products)
4. Update stock:
   - Choose option 5 (Manage Stock)
   - Product ID: 1
   - Action: 1 (Increase)
   - Quantity: 5
5. View orders:
   - Choose option 6 (View All Orders)
   - Update order status as needed
```

### Example 3: Guest Browsing

```
1. Start application: python main.py
2. Browse without login:
   - Choose option 3 (Browse Products - Guest)
   - View available products
   - Note: Cannot add to cart or purchase without login
```

---

##  Future Improvements

Potential enhancements for expanding the project:

- [ ] **Password Hashing** - Implement secure password hashing (bcrypt, hashlib)
- [ ] **Input Validation** - Add comprehensive input validation and sanitization
- [ ] [ ] **Error Handling** - Enhanced error handling and user-friendly error messages
- [ ] **Product Categories** - Add product categorization and filtering
- [ ] **Order Status Tracking** - Real-time order status updates and notifications
- [ ] **Payment Integration** - Simulate payment processing workflow
- [ ] **Discounts & Coupons** - Add promotional codes and discount management
- [ ] **Product Reviews** - Allow customers to rate and review products
- [ ] **Wishlist Feature** - Save products for later purchase
- [ ] **Export Functionality** - Export orders/products to CSV/JSON
- [ ] **Database Migrations** - Version control for database schema changes
- [ ] **Unit Tests** - Add comprehensive test coverage
- [ ] **REST API** - Convert to RESTful API with Flask/FastAPI
- [ ] **Web Interface** - Build a web frontend (HTML/CSS/JavaScript)
- [ ] **Multi-currency Support** - Support for different currencies
- [ ] **Inventory Alerts** - Low stock notifications for admins

---

##  License

This project is provided as-is for educational and learning purposes. Feel free to use, modify, and distribute as needed.

---

##  Contributing

This is a learning/demo project. Suggestions and improvements are welcome! Feel free to fork, experiment, and enhance the codebase.

---

**Built with ❤️ using Python and SQLite**
