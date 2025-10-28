from django.shortcuts import render,redirect,get_object_or_404
from app1.models import Customer,Product,Category,Cart,Order
from django.contrib import messages
# Create your views here.

def home(request):
    username=request.session.get('username',default=None)
    products=Product.objects.all()
    categories = Category.objects.all()
    return render(request,'app1/home.html',{'products':products,'categories':categories,'username':username})
def category_products(request, category_name):
    username = request.session.get('username', None)
    categories = Category.objects.all()
    category = Category.objects.get(name=category_name)
    products = category.product_set.all()  # all products in this category
    return render(request, 'app1/category_products.html', {'category': category,'products': products,'categories':categories,'username': username
    })

def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        data=Customer.objects.filter(username=username , password=password).first()
        if(data):
            messages.success(request,'Logged In successfully ....')
            request.session['username']=username
            return redirect('home')
        else:
            messages.success(request,'Invalid Username and Password ....')
            return render(request,'app1/login.html')            
    return render(request,'app1/login.html')
def register(request):
    if request.method=='POST':
        f_name=request.POST.get('f_name')
        l_name=request.POST.get('l_name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')
        mobile_no=request.POST.get('mobile_no')
        if Customer.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'app1/register.html')
        if Customer.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'app1/register.html')
        if Customer.objects.filter(mobile_no=mobile_no).exists():
            messages.error(request, "Mobile number already exists")
            return render(request, 'app1/register.html')
        Customer.objects.create(f_name=f_name,l_name=l_name,username=username,password=password,email=email,mobile_no=mobile_no)
        messages.success(request, "Registered Successfully...")
        request.session['username']=username
        return redirect('home')
    return render(request,'app1/register.html')

def logout(request):
    del request.session['username']
    return redirect('home')

def view_product(request,pid,category):
    categories = Category.objects.all()
    username=request.session.get('username',default=None)
    product=Product.objects.get(pid=pid)
    category_obj=Category.objects.get(name=category)
    sizes=category_obj.sizes if category_obj.sizes else None
    related_products=Product.objects.filter(category=category_obj).exclude(pid=pid)
    return render(request,'app1/view_product.html',{'product':product,'related_products':related_products,'sizes':sizes,'username':username,'categories':categories})

def add_cart(request, pid):  
    categories = Category.objects.all()
    username = request.session.get('username')
    product = get_object_or_404(Product, pid=pid)

    if not username:
        messages.success(request, 'Login First....')
        return redirect('login')

    if request.method == 'POST':
        qty = int(request.POST.get('quantity') or 1)
        size = request.POST.get('size') or 'M'
        customer_obj = Customer.objects.get(username=username)

        cart = Cart.objects.filter(customer=customer_obj).first()
        if not cart:
            cart = Cart.objects.create(customer=customer_obj, products=[])

        if not isinstance(cart.products, list):
            cart.products = []

        product_found = False
        for item in cart.products:
            if item.get('pid') == product.pid and item.get('size') == size:
                item['quantity'] = int(item.get('quantity', 0)) + qty
                item['total'] = float(item.get('price', product.price)) * item['quantity']
                product_found = True
                break

        if not product_found:
            data = {
                'pid': product.pid,
                'pname': product.name,
                'size': size,
                'price': float(product.price),
                'quantity': qty,
                'total': float(product.price) * qty,
                'categories':categories
            }
            cart.products.append(data)

        cart.save()
        messages.success(request, 'Item Added to Cart')
        return redirect('home')

    return redirect('home')
def cart(request):
    categories = Category.objects.all()
    username = request.session.get('username')
    if not username:
        messages.info(request, "Please login to view your cart.")
        return redirect('login')

    customer_obj = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer_obj).first()

    if not cart:
        cart = Cart.objects.create(customer=customer_obj, products=[])

    products = cart.products or []
    total_amount = sum(float(item.get('total', 0)) for item in products)

    return render(request, 'app1/cart.html', {
        'cart': cart,
        'username': username,
        'total': total_amount,
        'categories':categories
    })

def del_cart(request, pid, size):
    categories = Category.objects.all()
    username = request.session.get('username', None)
    customer_obj = Customer.objects.get(username=username)
    cart, created = Cart.objects.get_or_create(customer=customer_obj)

    cart.products = [
        item for item in cart.products
        if not (item['pid'] == pid and item['size'] == size)
    ]

    cart.save()
    messages.success(request, 'Item Removed Successfully...')
    return redirect('cart')
def profile(request):
    categories = Category.objects.all()
    username = request.session.get('username')
    if not username:
        return redirect('login')

    data = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=data).first()
    if not cart:
        cart = Cart.objects.create(customer=data, products=[])

    order = Order.objects.filter(customer=data).order_by('-oid')

    return render(request,'app1/profile.html',{'data': data,'cart': cart,'username': username,'order': order,'categories':categories})
def buy(request):
    categories = Category.objects.all()
    username = request.session.get('username')
    if not username:
        return redirect('login')

    customer_obj = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer_obj).first()
    if not cart:
        messages.warning(request, "Your cart is empty!")
        return redirect('cart')

    if not cart.products:
        messages.warning(request, "Your cart is empty!")
        return redirect('cart')

    Order.objects.create(customer=customer_obj, products=cart.products)

    cart.products = []
    cart.save()
    messages.success(request, "Order placed successfully! Thank You...")
    return redirect('home')

def buy_one(request, pid, size):
    categories = Category.objects.all()
    username = request.session.get('username', None)
    if not username:
        messages.error(request, "You need to login first.")
        return redirect('login')
    customer_obj = get_object_or_404(Customer, username=username)
    cart, created = Cart.objects.get_or_create(customer=customer_obj)
    product_to_buy = None
    for item in cart.products:
        if item['pid'] == pid and item['size'] == size:
            product_to_buy = item
            break

    if not product_to_buy:
        messages.error(request, "Product not found in cart.")
        return redirect('cart')
    order = Order.objects.create(
        customer=customer_obj,
        products=[product_to_buy],   
        status="Ordered"             
    )
    order.save()
    cart.products = [
        item for item in cart.products
        if not (item['pid'] == pid and item['size'] == size)
    ]
    cart.save()

    messages.success(request, f"{product_to_buy['pname']} bought successfully!")
    return redirect('cart')

def about(request):
    categories = Category.objects.all()
    username=request.session.get('username',default=None)
    return render(request,'app1/about.html',{'username':username,'categories':categories})
    