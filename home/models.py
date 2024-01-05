from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    logo = models.CharField(max_length=200)
    slug = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Slider(models.Model):
    title = models.CharField(max_length=500)
    image = models.ImageField(upload_to='media')
    url = models.URLField(max_length=500,blank=True)

    def __str__(self):
        return self.title


class Ad(models.Model):
    title = models.CharField(max_length=500)
    image = models.ImageField(upload_to='media')
    url = models.URLField(max_length=500, blank=True)
    rank = models.IntegerField()

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=500)
    image = models.ImageField(upload_to='media')
    slug = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.title


class Feedback(models.Model):
    name = models.CharField(max_length=200)
    post = models.CharField(max_length=500)
    rating = models.IntegerField()
    Image = models.ImageField(upload_to='media')
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ContactInfo(models.Model):
    address = models.CharField(max_length=300)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.address


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.TextField(blank=True)
    message = models.TextField(blank=True)

    def __str__(self):
        return self.name


LABEL = (('new', 'new'), ('sale', 'sale'), ('hot', 'hot'))
STOCK = (('In Stock', 'In Stock'), ('Out of Stock', 'Out of Stock'))


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price = models.IntegerField()
    discounted_price = models.IntegerField()
    image = models.ImageField(upload_to='media')
    description = models.TextField(blank=True)
    specification = models.TextField(blank=True)
    slug = models.TextField()
    label = models.CharField(choices=LABEL, max_length=50)
    stock = models.CharField(choices=STOCK, max_length=50)

    def __str__(self):
        return self.name


class Cart(models.Model):
    username = models.CharField(max_length=200)
    slug = models.CharField(max_length=500)
    items = models.ForeignKey(Product, on_delete=models.CASCADE)
    total = models.FloatField()
    checkout = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True) #date database ma automatically aaidinxa
    quantity = models.FloatField(default=1)

    def __str__(self):
        return self.username


class ProductReview(models.Model):
    username = models.CharField(max_length=300)
    slug = models.CharField(max_length=500)
    email = models.EmailField(max_length=100)
    review = models.TextField(blank=True)
    rating = models.IntegerField(default=5)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

