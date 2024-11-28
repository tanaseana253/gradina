from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import Login, CustomPasswordResetView, get_old_cart, CustomLogoutView

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('navbar/', views.navbar, name='navbar'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('signup/confirmation/',  views.SignUpView.as_view(template_name='registration/signup_confirmation.html'), name='signup_confirmation'),

    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('toggle_favorite/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('api/updateStock/', views.update_stock, name='update_stock'),
    path('confidentiality/', views.confidentiality, name='confidentiality'),
    path('how_to_buy/', views.how_to_buy, name='how_to_buy'),
    path('delivery_info/', views.delivery_info, name='delivery_info'),
    path('about_us/', views.about_us, name='about_us'),
    path('payment_methods/', views.payment_methods, name='payment_methods'),
    path('return_policy/', views.return_policy, name='return_policy'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),

# This was added for email Comanda ta
    path('submit-order/', views.submit_order, name='submit_order'),

    path('order-summary/', views.order_summary, name='order_summary'),
    path('api/checkBatchStock/', views.check_batch_stock, name='check_batch_stock'),
    path('save-cart-to-profile/', views.save_cart_to_profile, name='save_cart_to_profile'),
    path('get-old-cart/', get_old_cart, name='get_old_cart'),
]

    # path('populate/', views.populate_products, name='populate_products'),





