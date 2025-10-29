# InstantMart - Online Grocery Shopping Application

## 1. Project Overview

InstantMart is a Django-based e-commerce platform for quick and convenient grocery shopping online. It supports user authentication, product search and filtering, category browsing, shopping cart management, address management, secure PayPal payment integration, and order tracking. The application employs a mobile-friendly and responsive frontend design.

## 2. Main Features

- User Registration, Login, Logout
- Browse and search for products
- Category browsing and filtering
- Shopping cart (add, remove, update quantities)
- Manage delivery addresses
- Checkout process with PayPal integration
- View order history and account management
- Admin panel for product, category, and order management

## 3. Tech Stack

- **Backend:** Python (Django Framework) [97.5%]
- **Frontend:** HTML, CSS, JavaScript (for templates and interactivity)
- **Database:** MySQL (for CRUD operations)
- **Payment Gateway:** PayPal (integrated in checkout)
- **Other:** Powershell scripts, MVC architecture
- Responsive UI for mobile and desktop devices

## 4. Project Structure

```
InstantMart/
├── Scripts/
│   └── InstantMart_Project/
│       ├── InstantMart_App/
│       │   ├── migrations/
│       │   ├── static/
│       │   │   ├── css/
│       │   │   ├── js/
│       │   │   └── media/
│       │   ├── templates/
│       │   ├── forms.py
│       │   ├── models.py
│       │   ├── views.py
│       │   └── urls.py
│       ├── InstantMart_Project/
│       │   ├── settings.py
│       │   ├── urls.py
│       │   ├── asgi.py
│       ├── manage.py
│       ├── requirements.txt
│       └── README.md
└── pyvenv.cfg
```

- **Static files:** CSS, JavaScript, images for frontend
- **Templates:** HTML templates for all pages
- **Migrations:** Django migration history for database schema

## 5. Key Models

- **User authentication:** Built-in Django User model
- **Product:** name, description, price, category, image, etc.
- **Address:** delivery address fields (address_line_1, line_2, city, state, zip_code)
- **Cart:** for per-user cart items and quantities
- **Order, Payment:** tracks order details and payment records

## 6. Key URLs & Endpoints

| URL | Functionality |
|-----|---------------|
| `/` | Home page (show featured products) |
| `/signup` | User registration |
| `/signin` | Login |
| `/signout` | Logout |
| `/search` | Search products |
| `/category` | List categories |
| `/category/<category>/` | View by category |
| `/addtocart/<pid>` | Add product to cart |
| `/cart` | View cart |
| `/account` | User account/profile |
| `/delete_address/<id>/` | Remove delivery address |
| `/payment_success/` | Payment success page |
| `/payment_cancel/` | Payment cancel page |
| `/success` | Order confirmation |
| `/in_cart_item/<pid>` | Increase item qty |
| `/de_cart_item/<pid>` | Decrease item qty |
| `/delete/<cid>` | Delete item from cart |

## 7. Forms

**AddressForm (in forms.py):**

```python
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'zip_code']
```

Used for delivery address management.

## 8. Frontend Templates & Static Assets

- **HTML templates:** Home, product listings, cart, checkout, payment, account, auth pages, navigation, footers
- **CSS/JS:** Custom styles and user interaction (search, cart, payment, etc.)
- **Media:** Product images and UI icons

## 9. Setup & Installation

**Prerequisites:**

- Python 3.8+
- MySQL server
- Virtualenv

**Setup Steps:**

```bash
git clone https://github.com/SableSuyash/InstantMart.git
cd InstantMart/Scripts/InstantMart_Project
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
# Configure MySQL creds in settings.py
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# Visit http://localhost:8000/
```

## 10. Usage Flow

1. Register or log in as a new user
2. Browse/search grocery products & filter by category
3. Add items to shopping cart
4. Go to cart, adjust quantities or remove items
5. Add/manage delivery addresses
6. Checkout and pay using PayPal
7. Receive confirmation and view order history in your account

## 11. Admin Features

Access **/admin** to manage products, categories, orders, and users

## 12. Security

- Django authentication system
- CSRF tokens for forms
- Passwords securely hashed
- SQL injection prevention via Django ORM
- Secured payment via PayPal

## 13. Potential Enhancements

- Product reviews & ratings
- Inventory management
- Email notifications
- Multiple payment gateways (Stripe, RazorPay)
- Order tracking and analytics dashboard
- Promo/discount codes, push notifications
- Product recommendations

## 14. Troubleshooting

| Problem | Solution |
|---------|----------|
| DB connection errors | Check settings.py MySQL credentials |
| Static files not loading | Run python manage.py collectstatic |
| Payment not working | Check PayPal API keys in settings |
| Migration issues | Delete migrations/ and redo migrations |
| Port in use | Change runserver port (e.g. runserver 8001) |

## 15. License & Author

- **Author:** SableSuyash
- **Repository:** [github.com/SableSuyash/InstantMart](https://github.com/SableSuyash/InstantMart)
