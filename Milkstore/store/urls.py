from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path("buy_now/<int:product_id>/", views.buy_now, name="buy_now"),
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.view_cart, name="view_cart"),
    path("checkout/",views.checkout, name="checkout"),
    path('logout/',views.logout_view, name='logout'),

    path('send-otp/', views.send_otp_email, name='send_otp_email'),
    path('register/', views.register_view, name='register'),
    path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
