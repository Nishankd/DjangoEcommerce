from django.shortcuts import render
from .views import *
from django.views.generic import View
from .models import *
# Create your views here.


class BaseView(View):
    views = {}



class HomeView(BaseView):
    def get(self, request):
        self.views['categories'] = Category.objects.all()
        self.views['sliders'] = Slider.objects.all()
        self.views['brands'] = Brand.objects.all()
        return render(request, 'index.html', self.views)