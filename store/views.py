import logging
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, LogoutView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import views as auth_views, login
from django.views.generic import CreateView
from .forms import LogInForm, SignUpForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Profile
from django.http import JsonResponse
from django.db.models import Exists, OuterRef, Value, BooleanField
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product


def product_list(request):
    products = Product.objects.all()
    cart = request.session.get('cart', {})

    if request.user.is_authenticated:
        products = products.annotate(
            is_favorited=Exists(
                request.user.favorite_products.filter(id=OuterRef('id'))
            )
        )
        # Check if product is in user's cart
        products = products.annotate(
            is_in_cart=Exists(
                request.user.cart_products.filter(id=OuterRef('id'))
            )
        )
    else:
        products = products.annotate(
            is_favorited=Value(False, output_field=BooleanField()),
            is_in_cart=Value(False, output_field=BooleanField()))

    context = {
        'products': products,
        'cart': cart
    }
    return render(request, 'product_list.html', context)


def navbar(request):
    return render(request, 'navbar.html')


class Login(auth_views.LoginView):
    form_class = LogInForm
    template_name = 'registration/login.html'


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("signup_confirmation")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        # Save the user
        user = form.save()

        # Create a profile for the user
        Profile.objects.create(user=user)

        # Optionally, log the user in after successful sign-up
        login(self.request, user)
        return redirect(self.success_url)

    def form_invalid(self, form):
        # If the form is invalid, render the page with form errors
        return self.render_to_response(self.get_context_data(form=form))


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        # Clear cart from session
        request.session.pop('cart', None)
        request.session.modified = True
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def get_next_page():
        # Redirect to the login page or another desired page after logout
        return reverse('product_list')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'  # Form page for password reset
    email_template_name = 'registration/password_reset_email.txt'  # Plain text fallback
    html_email_template_name = 'registration/password_reset_email.html'  # HTML email template
    subject_template_name = 'registration/password_reset_subject.txt'  # Subject template
    success_url = reverse_lazy('password_reset_done')  # Redirect after form submission


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Add the product to the user's cart
    product.cart.add(request.user)

    return JsonResponse({'message': 'Product added to cart'})


@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Remove the product from the user's cart
    product.cart.remove(request.user)

    return JsonResponse({'message': 'Product removed from cart'})


def clear_cart(request):
    request.session['cart'] = {}  # Clear the entire cart
    return JsonResponse({'message': 'Cart cleared'})


@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.favorite.filter(id=request.user.id).exists():
        product.favorite.remove(request.user)
        favorited = False
    else:
        product.favorite.add(request.user)
        favorited = True

    return JsonResponse({'success': True, 'favorited': favorited})


@csrf_exempt
def update_stock(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        products = data.get('products', [])

        insufficient_stock_errors = []

        try:
            for product in products:
                product_name = product['productName']
                quantity_ordered = product['quantityOrdered']
                new_stock = product['newStock']

                # Find the product by name
                product_instance = Product.objects.get(name=product_name)

                # Check if the current stock allows for the quantity ordered
                if product_instance.stock < quantity_ordered:
                    insufficient_stock_errors.append({
                        'productId': product_instance.id,
                        'remainingStock': product_instance.stock
                    })
                elif new_stock >= 0:  # Update stock only if stock is sufficient and non-negative
                    product_instance.stock = new_stock
                    product_instance.save()
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Stock cannot be negative.'
                    }, status=400)

            # Return errors if any products are out of stock
            if insufficient_stock_errors:
                return JsonResponse({
                    'success': False,
                    'message': 'Some products are out of stock.',
                    'errors': insufficient_stock_errors  # Multiple stock issues
                }, status=400)

            # If no errors, stock update was successful for all products
            return JsonResponse({'success': True, 'message': 'Stock updated successfully!'})

        except Product.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Product does not exist.'
            }, status=404)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    }, status=400)


# # Set up logging
logger = logging.getLogger(__name__)


@csrf_exempt
@login_required
def submit_order(request):
    if request.method == 'POST':
        try:
            # Parse the cart from the request body
            data = json.loads(request.body)

            cart = data.get('cart')
            total = data.get('total')
            user_email = data.get('user_email')

            # Extract delivery, billing, and payment details
            delivery_info = data.get('delivery', {})
            billing_info = data.get('billing', {})
            payment_method = data.get('payment', 'cash_on_delivery')  # Extract payment method
            save_for_next_order = data.get('save_for_next_order', False)  # Get the checkbox value

            # Map payment method value to a user-friendly description
            payment_method_display = {
                'cash_on_delivery': 'Numerar sau card la livrare',
                'online_payment': 'Plată online'
            }.get(payment_method, 'Numerar sau card la livrare')  # Default if not found

            # Add validation for required fields
            if not all([cart, total, user_email, delivery_info, payment_method]):
                return JsonResponse({'error': 'Missing required fields.'}, status=400)

                # Build absolute URLs for product images
            for item in cart:
                if 'image' in item and 'url' in item['image']:
                    item['image']['absolute_url'] = request.build_absolute_uri(item['image']['url'])

                # Save or clear delivery information based on the checkbox
            profile = request.user.profile  # Get the user's profile

            if save_for_next_order:
                # Save delivery information
                profile.delivery_address = delivery_info.get('address', '')
                profile.delivery_name = delivery_info.get('name', '')
                profile.delivery_phone = delivery_info.get('phone', '')
                profile.save_for_next_order = True
                profile.save()
            else:
                # Clear delivery information if the checkbox is unchecked
                profile.delivery_address = ''
                profile.delivery_name = ''
                profile.delivery_phone = ''
                profile.save_for_next_order = False
                profile.save()

            # Compose email content
            subject = 'Bacania Gradina Craciun - Comanda Inregistrata'
            html_message = render_to_string('email/order_confirmation.html', {
                'cart': cart,
                'total': total,
                'user_email': user_email,
                'delivery_info': delivery_info,  # Include delivery details
                'billing_info': billing_info,  # Include billing details
                'payment_method_display': payment_method_display,  # Include payment method
            })
            plain_message = strip_tags(html_message)

            # Send the email to the user
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user_email],
                html_message=html_message,
                fail_silently=False
            )

            # Log the successful order submission
            logger.info(f'Order submitted successfully for {user_email}')

            # Return success response
            return JsonResponse({'message': 'Order submitted successfully!'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            logger.error(f'Error submitting order: {str(e)}')
            return JsonResponse({'error': 'An error occurred while processing your order.'}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


@login_required
def order_summary(request):
    products = Product.objects.all()
    cart = request.session.get('cart', {})

    if request.user.is_authenticated:
        # Annotate products for favorites and cart status like in product_list
        products = products.annotate(
            is_favorited=Exists(
                request.user.favorite_products.filter(id=OuterRef('id'))
            )
        )
        products = products.annotate(
            is_in_cart=Exists(
                request.user.cart_products.filter(id=OuterRef('id'))
            )
        )
    else:
        products = products.annotate(
            is_favorited=Value(False, output_field=BooleanField()),
            is_in_cart=Value(False, output_field=BooleanField())
        )

    context = {
        'products': products,
        'cart': cart
    }

    return render(request, 'order_summary.html', context)


def confidentiality(request):
    return render(request, 'footer/confidentiality.html')


def how_to_buy(request):
    return render(request, 'footer/how_to_buy.html')


def delivery_info(request):
    return render(request, 'footer/delivery_info.html')


def about_us(request):
    return render(request, 'footer/about_us.html')


def payment_methods(request):
    return render(request, 'footer/payment_methods.html')


def return_policy(request):
    return render(request, 'footer/return_policy.html')


def terms_and_conditions(request):
    return render(request, 'footer/terms_and_conditions.html')


@csrf_exempt
def check_batch_stock(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        products = data.get('products', [])

        if not products:
            return JsonResponse({'success': False, 'message': 'No products provided.'}, status=400)

        stock_info = []
        for product in products:
            product_name = product.get('productName')
            if product_name is None:
                continue

            try:
                product_instance = Product.objects.get(name=product_name)
                stock_info.append({
                    'productName': product_instance.name,
                    # 'productId': product_instance.id,  # include product ID for reference
                    'remainingStock': product_instance.stock
                })
            except Product.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': f'Product with name {product_name} not found.'
                }, status=404)
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'An error occurred: {str(e)}'
                }, status=500)

        return JsonResponse({'success': True, 'stockInfo': stock_info})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)


@csrf_exempt
@login_required
def save_cart_to_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart = data.get('cart', '')

            # Save the cart to the user's profile
            profile = request.user.profile
            if cart == '[]':  # If the cart is empty, clear the old_cart field
                profile.old_cart = None
            else:
                profile.old_cart = cart
            profile.save()

            return JsonResponse({'message': 'Cart saved successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def get_old_cart(request):
    try:
        profile = request.user.profile
        old_cart = profile.old_cart  # This will be a JSON string or None
        cart = json.loads(old_cart) if old_cart else []  # Convert JSON string to Python list

        # Synchronize cart with current stock
        for item in cart:
            product = Product.objects.get(name=item['productName'])
            item['stock'] = product.stock  # Update stock in cart

        return JsonResponse({'cart': cart}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
