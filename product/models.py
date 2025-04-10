from django.db import models
from user_application.models import User

class Category(models.Model):
  name = models.CharField(max_length=100)
  
  description = models.TextField()
  
  
  def __str__(self):
    return self.name
  
  
class Product(models.Model):
  
  name = models.CharField(max_length=100)
  
  description = models.TextField()
  
  price = models.DecimalField(max_digits=10, decimal_places=2)
  
  stock = models.PositiveIntegerField()
  
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  
  image = models.ImageField(upload_to='product_images')
  
  created_at = models.DateTimeField(auto_now_add=True)
  
  
  def __str__(self):
    return self.name
 


class Review(models.Model):
  
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  
  rating = models.IntegerField(default=0, choices=[(i,i) for i in range(1, 6)])
  
  comment = models.TextField()
  
  created_at = models.DateField(auto_now=True)
  
  updated_at = models.DateField(auto_now=True)
  
  def __str__(self):
    return self.user.username


class Cart(models.Model):
  
  user  = models.OneToOneField(User, on_delete=models.CASCADE)
  
  created_at = models.DateTimeField(auto_now_add=True)
  
  @property
  def total_price(self):
    return sum(i.cart_item.price * i.quantity for i in self.cartitem_set.all())
  
  
  @property
  def total_quantity(self):
    return sum(1 for i in self.cartitem_set.all())
  

class CartItem(models.Model):
  
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  
  cart_item = models.ForeignKey(Product, on_delete=models.CASCADE)
  
  quantity = models.PositiveIntegerField(default=1)
  