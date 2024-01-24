from django.shortcuts import render, redirect, get_object_or_404
from .views import *
from django.views.generic import View
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


class BaseView(View):
    views = {}
    views['categories'] = Category.objects.all()
    views['brands'] = Brand.objects.all()
    views['sale_products'] = Product.objects.filter(label='sale')


class HomeView(BaseView):
    def get(self, request):
        self.views
        self.views['sliders'] = Slider.objects.all()
        self.views['ads'] = Ad.objects.all()
        self.views['hot_news'] = Product.objects.filter(label='hot')
        self.views['new_news'] = Product.objects.filter(label='new')
        return render(request, 'index.html', self.views)


class CategoryView(BaseView):
    def get(self, request, slug):
        cat_id = Category.objects.get(slug=slug).id
        self.views['product_category'] = Product.objects.filter(category_id = cat_id)
        return render(request, 'category.html', self.views)


class ProductDetailView(BaseView):
    def get(self, request, slug):
        self.views
        self.views['product_details'] = Product.objects.filter(slug=slug)
        cat_id = Product.objects.get(slug=slug).category_id
        self.views['related_products'] = Product.objects.filter(category_id=cat_id)
        self.views['product_review'] = ProductReview.objects.filter(slug=slug) #yo slug vayeko product ko reiview dekhau
        return render(request, 'product-detail.html', self.views)


class SearchView(BaseView):
    def get(self, request):
        self.views
        if request.method == 'GET': #backend ma pathauda chai post method
            query = request.GET['query']
            if query == '':
                return redirect('/')
            self.views['search_products'] = Product.objects.filter(name__icontains=query) #mildojuldo vanna khojeko icontains
        return render(request, 'search.html', self.views)


def signup(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
                return redirect('/signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already in use")
                return redirect('/signup')
            else:
                User.objects.create_user(
                    first_name = fname,
                    last_name = lname,
                    username = username,
                    email = email,
                    password = password,
                ).save()

        else:
            messages.error(request, "Password did not match")
            return redirect('/signup')
    return render(request, 'signup.html')


def product_review(request, slug):
    if request.method=="POST":
        username = request.user.username #session ma vako user taneko
        email = request.user.email
        rating = request.POST['rating']
        review = request.POST['review']
        ProductReview.objects.create(
            username=username,
            email=email,
            rating=rating,
            review=review,
            slug=slug #kun product ko review deko ho ta

        ).save()
    return redirect(f'/productdetail/{slug}')


def add_to_cart(request, slug):
    username = request.user.username
    price = Product.objects.get(slug=slug).price
    discounted_price = Product.objects.get(slug=slug).discounted_price
    if discounted_price > 0:
        original_price = discounted_price
    else:
        original_price = price

    if Cart.objects.filter(slug=slug, username=username, checkout=False).exists(): #already cart ma xa vane kati wota xa yo slug vayeko product
        quantity = Cart.objects.get(slug=slug, username=username, checkout=False).quantity
        quantity += 1
        total = original_price * quantity
        Cart.objects.filter(slug=slug, username=username, checkout=False).update(
            quantity=quantity,
            total=total
        )
    else: #first time add to cart ko lagi tala ko value database ma halni
        Cart.objects.create(
            username=username,
            slug=slug,
            item=Product.objects.filter(slug=slug)[0], #we need dictionary not list, so zero index ko value pathako
            total=original_price
        ).save()

    return redirect('/cart')


class CartView(BaseView):
    def get(self, request):
        cart_total = 0
        username = request.user.username
        self.views['cart_view'] = Cart.objects.filter(username=username, checkout=False)
        for i in self.views['cart_view']:
            cart_total = cart_total + i.total
        self.views['cart_total'] = cart_total
        self.views['extra_charges'] = 50
        self.views['all_total'] = cart_total + 50
        return render(request, 'cart.html', self.views)


def reduce_qty(request, slug):
    username = request.user.username
    price = Product.objects.get(slug=slug).price
    discounted_price = Product.objects.get(slug=slug).discounted_price
    if discounted_price > 0:
        original_price = discounted_price
    else:
        original_price = price

    if Cart.objects.filter(slug=slug, username=username, checkout=False).exists(): #already cart ma xa vane kati wota xa yo slug vayeko product
        quantity = Cart.objects.get(slug=slug, username=username, checkout=False).quantity
        if quantity > 1:
            quantity -= 1
            total = original_price * quantity
            Cart.objects.filter(slug=slug, username=username, checkout=False).update(
                quantity=quantity,
                total=total
            )
        else:
            messages.error(request, "Quantity is already 1")
            return redirect('/cart')
    return redirect('/cart')


def delete_cart(request, slug):
    username = request.user.username
    Cart.objects.filter(slug=slug, username=username, checkout=False).delete() #object delete vayera janxa
    return redirect('/cart')


def checkout(request):
    return render(request, 'checkout.html')


class CheckoutView(View):
    def get(self, request):
        # Retrieve cart items for checkout
        cart_items = Cart.objects.filter(username=request.user.username, checkout=False)

        # Calculate total price
        cart_total = sum(item.total for item in cart_items)

        context = {
            'cart_items': cart_items,
            'cart_total': cart_total,
            'extra_charges': 50,
            'all_total': cart_total + 50,
        }
        return render(request, 'checkout.html', context)

def post(self, request):
    # Logic for handling the form submission goes here
    # For simplicity, let's mark the items as checked out in the database
    Cart.objects.filter(username=request.user.username, checkout=False).update(checkout=True)
    messages.success(request, 'Order placed successfully!')
    return redirect('checkout')

@login_required
def add_to_wishlist(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)

    # Check if the product is already in the wishlist
    if Wishlist.objects.filter(user=user, product=product).exists():
        # Product already in the wishlist, handle accordingly (e.g., display a message)
        messages.info(request, "This product is already in your wishlist.")
    else:
        # Add the product to the wishlist
        Wishlist.objects.create(user=user, product=product)
        messages.success(request, "Product added to your wishlist.")

    return redirect('home')

@login_required
def remove_from_wishlist(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)

    # Check if the product is in the wishlist before removing
    if Wishlist.objects.filter(user=user, product=product).exists():
        Wishlist.objects.filter(user=user, product=product).delete()
        messages.success(request, "Product removed from your wishlist.")
    else:
        messages.info(request, "This product is not in your wishlist.")

    return redirect('wishlist')

@login_required
def view_wishlist(request):
    user = request.user
    wishlist_items = Wishlist.objects.filter(user=user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})