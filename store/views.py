from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import category, product, banner, Order
from django.contrib.auth.decorators import login_required
# Create your views here.

def category_products(request, slug):
    category_obj = get_object_or_404(
        category,
        slug=slug,
        activate=True
    )

    products = product.objects.filter(
        category=category_obj,
        active=True
    ).order_by('-created_at')

    return render(request, 'category_products.html', {
        'category': category_obj,
        'products': products
    })

def home(request):
    banners=banner.objects.filter(active=True)
    categories=category.objects.filter(activate=True)
    products=product.objects.filter(active=True).order_by('-created_at')
    context={'banners':banners,
             'categories':categories,
             'products':products,}

    return render(request,'home.html',context)
def product_detail(request,slug):
    product_obj=get_object_or_404(product,slug=slug)
    return render(request,"product_detail.html",{'product':product_obj})

def add_to_cart(request, slug):
    cart = request.session.get('cart', {})
    if slug in cart:
        cart[slug] += 1
    else:
        cart[slug] = 1
    request.session['cart'] = cart
    return redirect('cart')
def cart(request):
    cart = request.session.get('cart', {})
    products = []

    for slug, quantity in cart.items():
        product_obj = get_object_or_404(product, slug=slug)
        total = product_obj.price * quantity

        products.append({
            'product': product_obj,
            'quantity': quantity,
            'total': total
        })

    grand_total = sum(item['total'] for item in products)

    return render(request, 'cart.html', {
        'products': products,
        'grand_total': grand_total
    })

def remove_from_cart(request,slug):
    cart=request.session.get('cart',{})
    if slug in cart:
        if cart[slug]>1:
            cart[slug]-=1
        else:
            del cart[slug]

    request.session['cart']=cart
    return redirect('cart')

def increase_quantity(request, slug):
    cart = request.session.get('cart', {})
    if slug in cart:
        cart[slug] += 1
    request.session['cart'] = cart
    return redirect('cart')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    products = []
    grand_total = 0
    for slug, quantity in cart.items():
       product_obj = get_object_or_404(product, slug=slug)
       if quantity > product_obj.stock:
          messages.error(
          request,
          f"{product_obj.name} is out of stock or has insufficient stock.")
          return redirect('cart')
       total = product_obj.price * quantity
       products.append({
        'product': product_obj,
        'quantity': quantity,
        'total': total
    })

    grand_total += total
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        for item in products:
            product_obj = item['product']
            quantity = item['quantity']
            if quantity > product_obj.stock:
                return redirect('cart')
        Order.objects.create(
            user=request.user,
            name=name,
            email=email,
            phone=phone,
            address=address,
            total_amount=grand_total)
        for item in products:
            product_obj = item['product']
            quantity = item['quantity']
            product_obj.stock -= quantity
            product_obj.save()
        request.session['cart'] = {}
        return redirect('order_success')
    return render(request, 'checkout.html', {
        'products': products,
        'grand_total': grand_total
    })

@login_required
def order_success(request):
    return render(request, 'order_success.html')

@login_required
def account(request):
    return render(request, 'account.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')
    return render(request, 'register.html')
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid username or password.')
        return redirect('login')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')