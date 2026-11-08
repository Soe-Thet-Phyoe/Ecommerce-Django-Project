from django.shortcuts import render,redirect, get_object_or_404
from apps.products.models import ProductModel
from apps.categories.models import CategoryModel
from apps.cart.models import CartModel

from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required, permission_required


from django.core.mail import send_mail
from django.conf import settings
import string
import secrets



def index(request):
    return render(request, "index.html")


def shop(request):

    products = ProductModel.objects.all()
    category_data = CategoryModel.objects.all()


    category_id = request.GET.get("user_select_category", "")
    search = request.GET.get("user_input_search", "").strip()

    # Search
    if search:
        products = products.filter(Q(title__icontains=search)|Q(description__icontains=search)|Q(category__name__icontains=search))

    # Filter
    if category_id:
        products = products.filter(category_id = category_id)

    # Pagination
    paginator = Paginator(products, 3)
    page_number = request.GET.get("get_page_num")
    product_page = paginator.get_page(page_number)

    product_data = {
            "product_key" : product_page,
            "category_key" : category_data,
            "selected_category" : category_id,
            "search_kw" : search
        }
    

    
    return render(request, "shop.html", product_data)


def user_register(request):

    if request.method == "POST":
        username = request.POST.get("user_input_username")
        email = request.POST.get("user_input_email")
        password = request.POST.get("user_input_pw")
        comfirm_password = request.POST.get("user_input_cpw")

        if password != comfirm_password:
            messages.error(request, "Password does not match!")
            return redirect("ur")

        if User.objects.filter(username = username).exists():
            messages.error(request, "User already exist!")
            return redirect("ur")
        
        else:
            alphabet = string.ascii_uppercase + string.digits
            otp = ''.join(secrets.choice(alphabet) for i in range(6))

            request.session['reg_data'] = {
                'username' : username,
                'email' : email,
                'password' : password,
                'otp' : otp
            }

            send_mail (
                'Your varification Code',
                f"Your OTP is {otp}",
                settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False
            )
            messages.success(request,'Verification code send successfully')
            return redirect("otp")


    return render (request, "register.html")

def verify_otp(request):
    if 'reg_data' not in request.session:
        messages.error(request, "Error Please try again")
        return redirect("ur") 
    
    if request.method == 'POST':
        user_otp = request.POST.get("user_input_otp")
        reg_data = request.session.get("reg_data")

        if user_otp == reg_data['otp']:
            user = User.objects.create_user(
                username = reg_data['username'],
                email = reg_data['email'],
                password = reg_data['password'],
            )
            del request.session['reg_data']
            messages.success(request,'Registered successfully')
            return redirect("ul")

        else:
            messages.error(request,"OTP code is wrong")

    return render(request,'verify_otp.html')


def user_login(request):

    if request.method == "POST":
        username = request.POST.get("user_input_username")
        password = request.POST.get("user_input_pw")

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login Succesfully!")
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password!")
            return redirect("ul")
    return render (request, "login.html")

def user_logout(request):
    logout(request)
    messages.success(request, "Logout Succesfully!")
    return redirect("ul")

@login_required
def cart_list(request):
    cart, created = CartModel.objects.get_or_create(user = request.user)

    products =  cart.products.all()

    total_price = sum(i.price for i in products)

    context = {
        "products_data" : products,
        "total_price" : total_price,
    }
    return render(request, "cart.html", context)

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(ProductModel, id=pk)

    cart, created = CartModel.objects.get_or_create(user=request.user)

    cart.products.add(product)
    
    return redirect('cart')

def remove_from_cart(request, pk):
    product = get_object_or_404(ProductModel, id=pk)

    cart, created = CartModel.objects.get_or_create(user = request.user)

    cart.products.remove(product)

    return redirect("cart")

def page_not_found(request):
    return render(request, "page_not_found.html")