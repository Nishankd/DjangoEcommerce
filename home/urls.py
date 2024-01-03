from django.urls import path, include
from .views import *
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug>', CategoryView.as_view(), name='category'),
    path('productdetail/<slug>', ProductDetailView.as_view(), name='details'),
    path('search', SearchView.as_view(), name='search'),
    path('signup', signup, name='signup'),
]
