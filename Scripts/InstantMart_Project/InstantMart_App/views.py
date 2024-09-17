from django.shortcuts import render,redirect,get_object_or_404
# from .models import SignUp
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import AddressForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings



# Create your views here.
def home(request):
    card=Product.objects.all()
    category=Category.objects.all()
    fname=request.session.get('fname',None)
    context={'Card':card,'fname':fname,'Cate':category}
    return render(request,'../templates/home.html',context)

def search_product(request):
    query=request.GET.get('query')
    product=Product.objects.all()
    fname=request.session.get('fname',None)
    if query:
        results= Product.objects.filter(product_name__icontains=query)
    else:
        messages.warning(request,'Please enter valid product name!')
        return redirect('/')
        
    context={'product':product,'fname':fname,'results':results,'query':query,'no_results':len(results)==0}
    return render(request,'search.html',context)

def sign_up(request):
    if request.method=='POST':
        username=request.POST.get('username')
        fname=request.POST.get('firstname')
        lname=request.POST.get('lastname')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm-password')
        
        if User.objects.filter(username=username):
            messages.error(request,'Username is already exist!')
            return redirect('/signup')
        if User.objects.filter(email=email):
            messages.error(request,'Email Address is already Registered!')
            return redirect('/signup')
        if len(username)>10:
            messages.error(request,'Username must be 10 Charater or less!')
            return redirect('/signup')
        if confirm_password!=password:
            messages.error(request,"Password Doesn't Matched!")
            return redirect('/signup')
        if not username.isalnum():
            messages.error(request,"Username must be Alpha-Numeric!")
            return redirect('/signup')
        if len(password)<=7:
            messages.error(request,'Password Should be atleast 7 Character!')
            return redirect(request,'/signup')
        # s.username=username
        # s.full_name=full_name
        # s.email=email
        # s.password=password
        # s.confirm_password=confirm_password
        # s.save()

        myuser=User.objects.create_user(username,email,password)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()


        messages.success(request,'Your Account has been created!')
        messages.info(request,'Please Login!')
        return redirect('/signin')
    else:
        return render(request,'../templates/signup.html')

def sign_in(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            fname=user.first_name
            request.session['fname']=fname
            request.session['uid']=user.id
            messages.success(request,"Sign In Successfully!")
            return redirect('/')
        else:
            messages.error(request,'Wrong Credentials!')
            return render(request,'signin.html')
    else:
        return render(request,'signin.html')

def sign_out(request):
    logout(request)
    messages.warning(request,"You've been Sign Out!")
    return redirect('/')

@login_required
def account(request):
    fname=request.session.get('fname',None)
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('/account')  # Redirect to the same page after saving
    else:
        form = AddressForm()

    user_addresses = Address.objects.filter(user=request.user)
    context={'fname':fname,'form': form,'user_addresses': user_addresses}  #'form': form,'user_addresses': user_addresses
    return render(request,'account.html',context)

def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    return redirect('/account')

def category(request):
    fname=request.session.get('fname',None)
    cate=Category.objects.all()
    card=Product.objects.all()
    context={'fname':fname,'Cate':cate,'Card':card}
    return render(request,'category.html',context)

def category_page(request,category_name):
    fname=request.session.get('fname',None)
    cate=Category.objects.all()
    card=Product.objects.all()
    filtered_product=Product.objects.filter(category_name=category_name)
    context={'fname':fname,'Cate':cate,'f_product':filtered_product,'Card':card}
    return render(request,'category.html',context)

def filter_cate(request,pid):
    # cateid=Category.objects.get(id=pid)
    fname=request.session.get('fname',None)
    product=Product.objects.filter(category_id=pid)
    cate=Category.objects.all()
    card=Product.objects.all()
    context={'Cate':cate,'product':product,'fname':fname,'Card':card}
    return render(request,'cat.html',context)

def sidebar(request):
    fname=request.session.get('fname',None)
    cate=Category.objects.all()
    context={'Cate':cate,'fname':fname}
    return render(request,'category_list.html',context)

def add_to_cart(request, pid):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=pid)
        user = request.user

        # Try to get the existing cart item for this product and user
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            # If the cart item already exists, increase the quantity
            cart_item.quantity += 1
            cart_item.subtotalprice = int(cart_item.quantity) * int(cart_item.product.product_price)
        cart_item.save()

        return redirect('/category')
    else:
        return render(request, 'signin.html')




import paypalrestsdk
from django.conf import settings
from django.urls import reverse
import requests

@login_required
def cart_item(request):
    uid = request.session.get('uid')
    if request.user.is_authenticated:
        cl = Cart.objects.filter(user=uid)
        total_price = sum(i.subtotalprice for i in cl)
        fname = request.session.get('fname', None)
        num_item = cl.count()

        context = {
            'cl': cl,
            'fname': fname,
            'num_item': num_item,
            'total_price': total_price,
        }

        # Only configure PayPal SDK if there are items in the cart
        if num_item > 0:
            paypalrestsdk.configure({
                "mode": 'sandbox',  # sandbox or live
                "client_id": settings.PAYPAL_CLIENT_ID,
                "client_secret": settings.PAYPAL_CLIENT_SECRET,
            })

            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": request.build_absolute_uri(reverse('InstantMart_App:payment_success')),
                    "cancel_url": request.build_absolute_uri(reverse('InstantMart_App:payment_cancel'))
                },
                "transactions": [{
                    "item_list": {
                        "items": [{
                            "name": "Cart Items",
                            "sku": "item",
                            "price": str(total_price),
                            "currency": "USD",
                            "quantity": 1
                        }]
                    },
                    "amount": {
                        "total": str(total_price),
                        "currency": "USD"
                    },
                    "description": "Payment for cart items."
                }]
            })

            if payment.create():
                # Handle approval URL in case you want to redirect users for payment authorization
                for link in payment.links:
                    if link.rel == "approval_url":
                        context['approval_url'] = str(link.href)
                        break
            else:
                context['error'] = payment.error

        return render(request, 'cart.html', context)
    else:
        return render(request, 'signin.html')

@csrf_exempt
def payment_success(request):
    order_id = request.GET.get('paymentId')  # This is actually the order ID
    payer_id = request.GET.get('PayerID')

    if order_id and payer_id:
        # Prepare the request URL
        url = f"https://api.sandbox.paypal.com/v2/checkout/orders/{order_id}"
        
        # Set up headers with your credentials
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_paypal_access_token()}",  # You'll need a function to get the access token
        }

        # Make the request to PayPal
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            order_data = response.json()
            if order_data['status'] == "COMPLETED":
                # Delete items from the cart
                cart = Cart.objects.filter(user=request.user)  # Adjust according to your Cart model
                cart.delete()

                # Redirect to the home page
                return redirect('/success')  # Replace 'home' with your home page URL name
                
            else:
                return JsonResponse({'status': 'Payment not completed'})
        else:
            return JsonResponse({'status': 'Order not found', 'error': response.json()})

    return JsonResponse({'status': 'Invalid request method'})

def get_paypal_access_token():
    url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET)
    data = {"grant_type": "client_credentials"}
    
    response = requests.post(url, data=data, auth=auth, headers={"Content-Type": "application/x-www-form-urlencoded"})
    
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception("Failed to obtain access token from PayPal")

@csrf_exempt
def payment_cancel(request):
    return JsonResponse({'status': 'Payment cancelled'})


def decrease_cart_item(request,pid):
    uid=request.session.get('uid')
    product = get_object_or_404(Product, id=pid)
    cart_item = get_object_or_404(Cart, product=product, user_id=uid)
    if (cart_item.quantity > 1):
        cart_item.quantity -= 1
        cart_item.subtotalprice = int(cart_item.quantity) * int(cart_item.product.product_price)
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('/cart')




def increase_cart_item(request,pid):
    uid = request.session.get('uid')
    product = get_object_or_404(Product, id=pid)
    cart_item, created = Cart.objects.get_or_create(product=product, user_id=uid)
    cart_item.quantity += 1
    cart_item.subtotalprice = int(cart_item.quantity) * int(cart_item.product.product_price)
    cart_item.save()
    return redirect('/cart')
    
def delete_cart_item(request,Cid):
    del_cart_item = get_object_or_404(Cart, id=Cid, user=request.user)
    del_cart_item.delete()
    return redirect('/cart')


def success(request):
    return render(request,'success.html')




# @login_required
# def place_order(request):
#     user=request.user
#     uid = request.session.get('uid')
#     try:
#         add=Address.objects.filter(user=user)
#     except Address.DoesNotExist:
#         messages.error(request,'No Address Found!')
#         return render(request,'account.html')
#     cart_item=Cart.objects.filter(id=uid)

#     order_amount= total_price * 100
#     order_currency = 'INR'

#     client.order.create(dict(amount = order_amount,currency= order_currency,payment_capture='1'))

#     cl=Cart.objects.filter(user=user)
#     total_price=sum(i.subtotalprice for i in cl)

#     context={'add':add,'cart_item':cart_item,'total_price':total_price,}
#     return redirect('/order',context)





# @login_required
# def order_placed(request):
#     uid = request.session.get('uid')
#     cl=Cart.objects.filter(user=uid)
#     total_price=sum(i.subtotalprice for i in cl)

#     return render(request,'order.html')