from django.urls import path
from gateway import template_views as v

urlpatterns = [
    # Default = Customer home
    path('', v.cust_home, name='home'),

    # Auth
    path('login/', v.login_page, name='login'),
    path('register/', v.register_page, name='register'),
    path('logout/', v.logout_page, name='logout'),

    # Customer portal
    path('customer/', v.cust_home, name='cust_home'),
    path('customer/cart/', v.cust_cart, name='cust_cart'),
    path('customer/orders/', v.cust_orders, name='cust_orders'),
    path('customer/reviews/', v.cust_reviews, name='cust_reviews'),
    path('customer/recommendations/', v.cust_recommendations, name='cust_recommendations'),
    path('customer/profile/', v.cust_profile, name='cust_profile'),

    # Staff portal
    path('staff/', v.staff_dashboard, name='staff_dashboard'),
    path('staff/orders/', v.staff_orders, name='staff_orders'),
    path('staff/shipments/', v.staff_shipments, name='staff_shipments'),
    path('staff/books/', v.staff_books, name='staff_books'),
    path('staff/customers/', v.staff_customers, name='staff_customers'),

    # Manager portal
    path('manager/', v.mgr_dashboard, name='mgr_dashboard'),
    path('manager/staff/', v.mgr_staff, name='mgr_staff'),
    path('manager/customers/', v.mgr_customers, name='mgr_customers'),
    path('manager/books/', v.mgr_books, name='mgr_books'),
    path('manager/categories/', v.mgr_categories, name='mgr_categories'),
    path('manager/authors/', v.mgr_authors, name='mgr_authors'),
    path('manager/publishers/', v.mgr_publishers, name='mgr_publishers'),
    path('manager/orders/', v.mgr_orders, name='mgr_orders'),
    path('manager/payments/', v.mgr_payments, name='mgr_payments'),
    path('manager/shipments/', v.mgr_shipments, name='mgr_shipments'),
    path('manager/reviews/', v.mgr_reviews, name='mgr_reviews'),
]
