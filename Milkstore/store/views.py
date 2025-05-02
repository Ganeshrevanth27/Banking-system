from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product,Category,cartitem,orderitem # ✅ FIXED: Import Category from models
from django.db import transaction
import random
from django.core.mail import send_mail
from .models import OTPverification

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')
def logout_view(request):
    return redirect('login')

@login_required
def home_view(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'buy_now.html', {'product': product})

def add_to_cart(request, product_id):
    product=get_object_or_404(Product, id=product_id)
    cart_item,created=cartitem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')

def view_cart(request):
    cart_items = cartitem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_price': total_price})
@login_required
def checkout(request):
    cart_items = cartitem.objects.filter(user=request.user)

    if not cart_items:
        return redirect('view_cart')
    

    total_price = sum(item.product.price * item.quantity for item in cart_items)
    if request.method == 'POST':
        with transaction.atomic():
            order = order.objects.create(
                user=request.user,
                total_price=total_price,
                is_completed=True,
            )   
            
            for items in cart_items:
                order_item = orderitem.objects.create(
                    order=order,
                    product=items.product,
                    quantity=items.quantity,
                    price=items.product.price,
                )
                
                cart_items.delete()

            return render(request, 'order_success.html', {'order': order})
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})
# Add this import at the top

# ✅ Corrected register_view
def register_view(request):
    if request.method == 'POST':
        # create user
        create_user = User.objects.create_user(...)
        create_user.is_active = False
        create_user.save()
        send_otp_email(create_user)
        return redirect('verify_otp', user_id=create_user.id)
    return render(request, 'register.html')

# ✅ Corrected send_otp_email
def send_otp_email(request,user):
    user_id = request.POST.get('user_id')  # or however you're sending it
    user = User.objects.get(id=user_id)

    otp = str(random.randint(100000, 999999))
    OTPverification.objects.update_or_create(user=user, defaults={'otp_code': otp})  # ✅ FIXED model name

    send_mail(
        'Your OTP Code',
        f'Hello {user.username}, your OTP is {otp}',
        'ganeshgorriupudi.com',
        [user.email],
        fail_silently=False,
    )

# ✅ Corrected verify_otp
def verify_otp(request, user_id):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        try:
            otp_record = OTPverification.objects.get(user__id=user_id)
        except OTPverification.DoesNotExist:
            return render(request, 'verify_otp.html', {'error': 'OTP record not found', 'user_id': user_id})

        if entered_otp == otp_record.otp_code:
            user = otp_record.user
            user.is_active = True
            user.save()
            otp_record.delete()
            return redirect('login')
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP', 'user_id': user_id})
    
    return render(request, 'verify_otp.html', {'user_id': user_id})
