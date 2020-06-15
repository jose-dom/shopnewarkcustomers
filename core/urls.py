from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='core-home'),
    path('search-customer/', views.search_customer, name="search-customer"),
    path('search-customer-email/', views.search_customer_email, name="search-customer-email"),
    path('customer-results/', views.customer_results, name="customer-results"),
    path('customer-results-email/', views.customer_results_email, name="customer-results-email"),
    path('transactions/', views.transactions, name="transactions"),
]