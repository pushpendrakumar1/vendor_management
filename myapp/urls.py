from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView




urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgot/', views.forgot, name='forgot'),
    path('add_vendor', views.add_vendor, name='add_vendor'),
    path('add_vendor_details/', views.add_vendor_details, name='add_vendor_details'),
    path('vendor_list/', views.vendor_list, name='vendor_list'),
    path('delete_vendor/<int:vendor_id>/', views.delete_vendor, name='delete_vendor'),
    path('vendor_detail/<int:vendor_id>/', views.vendor_detail, name='vendor_detail'),
    path('order_list/', views.vendor_order_list, name='vendor_order_list'),
    path('vendor_order_detail/<int:vendor_id>/', views.vendor_order_detail, name='vendor_order_detail'),
    path('edit_vendor_order/<int:order_id>/', views.edit_vendor_order, name='edit_vendor_order'),
    path('delete_vendor_order/<int:order_id>/', views.delete_vendor_order, name='delete_vendor_order'),
    path('forgot-password/', views.CustomPasswordResetView.as_view(), name='forgot'),
    path('reset-password/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]

    




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


