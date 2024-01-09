from django.urls import path, include
from .views import *
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug>', CategoryView.as_view(), name='category'),
    path('productdetail/<slug>', ProductDetailView.as_view(), name='details'),
    path('search', SearchView.as_view(), name='search'),
    path('signup', signup, name='signup'),
    path('product_review/<slug>', product_review, name='product_review'),
    path('add_to_cart/<slug>', add_to_cart, name='add_to_cart'), #render nagarda function based view nai banaune ho
    path('cart', CartView.as_view(), name='cart'),
]
