from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from shop.models import *
from shop.forms import *
from django.contrib.auth.models import User
from django.contrib import messages

# Home
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

# Register
def register(request):
    msg = ''
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                    msg = "Username or email already exists."
            else:
                    User.objects.create_user(username=username, email=email, password=password)
                    msg = "Account created! Please login."
                    return redirect('login')

    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form, 'msg': msg})

# Login
def user_login(request):
    msg = ''
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

            if user:
                login(request, user)
                return redirect('home')
            else:
                msg = "Invalid email or password."
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'msg': msg})

# Logout
def user_logout(request):
    logout(request)
    return redirect('login')

# Add to cart
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart_item = CartItem.objects.filter(user=request.user, product=product).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        CartItem.objects.create(user=request.user, product=product, quantity=1)

    return redirect('cart')

# Remove from cart
def remove_from_cart(request, id):
    item = get_object_or_404(CartItem, id=id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart')

# View cart
def cart(request):
    # Get all the cart items that belong to the current logged-in user
    items = CartItem.objects.filter(user=request.user)

    # Calculate total price (price × quantity for each item)
    total = 0
    for item in items:
        total += item.product.price * item.quantity

    # Send the items and total to the HTML page
    return render(request, 'cart.html', {'items': items, 'total': total})


def payment(request):
    # Step 1: Check if user is logged in
    if not request.user.is_authenticated:
        return redirect('login')

    # Step 2: Get user's cart items
    items = CartItem.objects.filter(user=request.user)

    # Step 3: Calculate total price
    total = 0
    for item in items:
        total += item.product.price * item.quantity

    # Step 4: Handle form submission
    if request.method == "POST":
        if "pay" in request.POST:
            # Simulate payment success — no order saving
            items.delete()  # clear cart
            return render(request, 'payment_success.html')  # show success page

        elif "continue" in request.POST:
            return redirect('home')

    # Step 5: Show payment page
    return render(request, "payment.html", {'items': items, 'total': total})
