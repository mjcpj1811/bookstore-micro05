from django.shortcuts import render


def _r(request, template, page):
    return render(request, template, {'active_page': page})


# Auth pages
def login_page(request):
    return render(request, 'login.html')


def register_page(request):
    return render(request, 'register.html')


def logout_page(request):
    return render(request, 'logout.html')


# Customer portal (default)
def cust_home(request):
    return _r(request, 'customer/home.html', 'home')


def cust_cart(request):
    return _r(request, 'customer/cart.html', 'cust_cart')


def cust_orders(request):
    return _r(request, 'customer/orders.html', 'cust_orders')


def cust_reviews(request):
    return _r(request, 'customer/reviews.html', 'cust_reviews')


def cust_recommendations(request):
    return _r(request, 'customer/recommendations.html', 'cust_recommend')


def cust_profile(request):
    return _r(request, 'customer/profile.html', 'cust_profile')


# Staff portal
def staff_dashboard(request):
    return _r(request, 'staff/dashboard.html', 'staff_dashboard')


def staff_orders(request):
    return _r(request, 'staff/orders.html', 'staff_orders')


def staff_shipments(request):
    return _r(request, 'staff/shipments.html', 'staff_shipments')


def staff_books(request):
    return _r(request, 'staff/books.html', 'staff_books')


def staff_customers(request):
    return _r(request, 'staff/customers.html', 'staff_customers')


# Manager portal
def mgr_dashboard(request):
    return _r(request, 'manager/dashboard.html', 'mgr_dashboard')


def mgr_staff(request):
    return _r(request, 'manager/staff.html', 'mgr_staff')


def mgr_customers(request):
    return _r(request, 'manager/customers.html', 'mgr_customers')


def mgr_books(request):
    return _r(request, 'manager/books.html', 'mgr_books')


def mgr_categories(request):
    return _r(request, 'manager/categories.html', 'mgr_categories')


def mgr_authors(request):
    return _r(request, 'manager/authors.html', 'mgr_authors')


def mgr_publishers(request):
    return _r(request, 'manager/publishers.html', 'mgr_publishers')


def mgr_orders(request):
    return _r(request, 'manager/orders.html', 'mgr_orders')


def mgr_payments(request):
    return _r(request, 'manager/payments.html', 'mgr_payments')


def mgr_shipments(request):
    return _r(request, 'manager/shipments.html', 'mgr_shipments')


def mgr_reviews(request):
    return _r(request, 'manager/reviews.html', 'mgr_reviews')
