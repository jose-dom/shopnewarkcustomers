"""shopnewark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from users.models import User

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('register-customer/', user_views.register_cus, name='register-customer'),
    path('register-vendor/', user_views.register_ven, name='register-vendor'),
    #path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path('profile-update/', user_views.profile_update, name='profile-update'),
    path('vendor-transactions/', user_views.vendor_transactions, name='vendor-transactions'),
    path('customer-transactions/', user_views.customer_transactions, name='customer-transactions'),
    ##reset password
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    ##create/update vendor
    path('vendor/new/', user_views.VendorCreateView.as_view(), name='vendor-create'),
    path('vendor/<int:pk>/update', user_views.VendorUpdateView.as_view(), name='vendor-update'),
    path('vendor/<int:pk>/', user_views.VendorDetailView.as_view(), name='vendor-detail'),
    path('vendor-update-limited/', user_views.vendor_update, name='vendor-update-limited'),
    path('vendor-update-admin/<int:ven_id>/', user_views.admin_vendor_update, name='vendor-update-admin'),
    ##admin dashboard
    path('admin-dashboard/', user_views.admin_dashboard, name='admin-dashboard'),
]


handler404 = 'users.views.error_view_400'
handler500 = 'users.views.error_view'
handler403 = 'users.views.error_view_400'
handler400 = 'users.views.error_view_400'


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
