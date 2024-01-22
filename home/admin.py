from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Slider)
admin.site.register(Ad)
admin.site.register(Brand)
admin.site.register(Feedback)
admin.site.register(Wishlist)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "brand", "price")
    list_filter = ("name", "price")
    search_fields = ("name", "stock")

    class Meta:
        ordering = ("name", "category", "brand", "price")


admin.site.register(Contact)
admin.site.register(ContactInfo)
admin.site.register(ProductReview)
admin.site.register(Cart)