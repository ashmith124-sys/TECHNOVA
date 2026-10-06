from django.db import models
from django.utils.text import slugify
# Create your models here.
class category(models.Model):
    name= models.CharField(max_length=100)
    slug= models.SlugField(unique=True,blank=True)
    description=models.TextField(blank=True)
    activate=models.BooleanField(default=True)

    def save(self,*args,**kwargs):
        if not self.slug :
            self.slug=slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name
class product(models.Model):
    category=models.ForeignKey(category,on_delete=models.CASCADE,related_name="product")
    name=models.CharField(max_length=200)
    slug= models.SlugField(unique=True,blank=True)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField(default=0)
    image=models.ImageField(upload_to="products/")
    active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name

class banner(models.Model):
    title=models.CharField(max_length=200)
    content = models.TextField(blank= True)
    image=models.ImageField(upload_to="banners/")
    active=models.BooleanField(default=True)
    create_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Order(models.Model):
    user = models.ForeignKey(
    'auth.User',
    on_delete=models.CASCADE,
    related_name='orders',
    null=True,
    blank=True
)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Processing', 'Processing'),
            ('Shipped', 'Shipped'),
            ('Delivered', 'Delivered'),
            ('Cancelled', 'Cancelled'),
        ],default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name