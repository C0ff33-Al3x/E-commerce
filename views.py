from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Customer, Cart, OrderPlaced, Payment, Wishlist
from .forms import CustomerRegistrationform, CustomerProfileForm, OrderForm
from django.db.models import Count, Q
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
@login_required
def home(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/home.html", locals())

@login_required
def about(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/about.html", locals())

@login_required
def contact(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/contact.html", locals())

@method_decorator(login_required, name='dispatch')
class CategoryView(View):
    def get(self, request,val):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html",locals())

@method_decorator(login_required, name='dispatch')
class CategoryTitle(View):
    def get(self, request,val):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        return render(request, "app/category.html",locals())

@method_decorator(login_required, name='dispatch')
class ProductDetail(View):
    def get(self, request,pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(user=request.user) & Q(product=product))
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html",locals())


class CustomerRegistrationView(View): 
    def get(self, request):
        form = CustomerRegistrationform()
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, "app/customerregistration.html", locals())
    def post(self, request):
        form=CustomerRegistrationform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations!! Registered Successfully')
        else:
            messages.warning(request, 'Invalid Input Data')
        return render(request, "app/customerregistration.html", locals())


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, "app/profile.html", locals()) 
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile saved successfully!")
        else:
            messages.warning(request, "Invalid input data")

        return render(request, "app/profile.html", locals())

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/address.html', locals())

@method_decorator(login_required, name='dispatch')
class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, "app/updateAddress.html", locals())
    def post(self, request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.warning(request, "Profile Updated successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")

@login_required
def show_cart(request):
    user=request.user
    cart = Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity*p.product.discounted_price
        amount+=value
    totalamount=amount + 4
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/addtocart.html', locals())


@method_decorator(login_required, name='dispatch')
class checkout(View):
    def get(self, request):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        user=request.user
        add = [Customer.objects.get(user=user)]
        cart_items = Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value=p.quantity*p.product.discounted_price
            famount+=value
        totalamount=famount + 4

        order_form = OrderForm()
        
        context = {
            'user': user,
            'add': add,
            'cart_items': cart_items,
            'totalamount': totalamount,
            'order_form': order_form,
        }
        return render(request, 'app/checkout.html', context)

    def post(self, request):
        order_form = OrderForm(request.POST) 
        if order_form.is_valid():
            user = request.user
            add = Customer.objects.get(user=user)
            cart_items = Cart.objects.filter(user=user)
            famount = 0
            for p in cart_items:
                value = p.quantity * p.product.discounted_price
                famount += value
            totalamount = famount + 4

            # Create Payment instance
            payment = Payment.objects.create(user=user, amount=totalamount)

            # Create OrderPlaced instances for each product in the cart
            for c in cart_items:
                OrderPlaced.objects.create(
                    user=user,
                    customer=add,
                    product=c.product,
                    quantity=c.quantity,
                    payment=payment
                )
                c.delete()

            return redirect("orders")
        else:
            # Handle invalid form data
            pass


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount+=value
        totalamount=amount + 4
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
        
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount+=value
        totalamount=amount + 4
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
       
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user=request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount+=value
        totalamount=amount + 4
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

@login_required
def orders(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': order_placed})

@login_required
def payment_done(request):
    order_id=request.GET.get('order_id')
    customer_id=request.GET.get('customer_id')
    user=request.user
    customer=Customer.objects.get(id=cust_id)
    payment.paid=True
    payment.save()

    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer,product=c.product, quantity=c.quantity, payment=payment).save()
        c.delete()
    return redirect("orders")

def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data={
            'message':'Added to Wishlist'
        }
        return JsonResponse(data)

def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        user = request.user
        Wishlist.objects.filter(user=user, product_id=prod_id).delete()
        data={
            'message':'Removed to Wishlist'
        }
        return JsonResponse(data)

@login_required
def search(request):
    query = request.GET.get('search', '')  
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    products = Product.objects.filter(Q(title__icontains=query))
    return render(request, "app/search.html", {'products': products, 'totalitem': totalitem, 'wishitem': wishitem})


@login_required
def show_wishlist(request):
    user=request.user
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render(request, 'app/wishlist.html', locals())


