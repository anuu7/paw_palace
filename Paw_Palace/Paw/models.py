from django.db import models

# Create your models here.


class Petshop(models.Model):
    shopname = models.CharField(max_length=20)
    ownername =models.CharField(max_length=20)
    adress = models.CharField(max_length=50)
    phone = models.BigIntegerField()
    email = models.CharField(max_length=30)
    username = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20)
    suspense = models.BooleanField(default=True)

    def __str__(self):
        return self.shopname


class Petuser(models.Model):
    name = models.CharField(max_length=20)
    phone = models.BigIntegerField()
    email = models.CharField(max_length=30)
    username = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20)



class Notification(models.Model):
    shop = models.ForeignKey(Petshop, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    def __str__(self):
        return self.message

class UserNotification(models.Model):
    user = models.ForeignKey(Petuser, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    def __str__(self):
        return self.seen


class Gallery(models.Model):
    category=models.CharField(max_length=20)
    breed=models.CharField(max_length=20)
    image=models.FileField()
    accept=models.BooleanField(default=False)
    def __str__(self):
        return self.breed

class Reviews(models.Model):
    user = models.ForeignKey(Petuser, on_delete=models.CASCADE)
    review = models.TextField()
    def __str__(self):
        return self.review
class Product(models.Model):
    shop = models.ForeignKey(Petshop, on_delete=models.CASCADE)
    prodname = models.CharField(max_length=20)
    price = models.IntegerField()
    category = models.CharField(max_length=20)
    qty = models.IntegerField()
    image = models.FileField()
    pettype = models.CharField(max_length=30, default='All Pets', blank=True)
    description = models.TextField(blank=True, default='')
    def __str__(self):
        return self.prodname

class Services(models.Model):
    shop = models.ForeignKey(Petshop, on_delete=models.CASCADE)
    servicename = models.CharField(max_length=20)
    price = models.IntegerField()
    desc = models.TextField()
    duration = models.CharField(max_length=30, blank=True, default='')
    image = models.FileField(upload_to='static')

    def __str__(self):
        return self.servicename

class Cart(models.Model):
    user = models.ForeignKey(Petuser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    total_price = models.IntegerField()
    def __str__(self):
        return self.user.name

class Placeanorder(models.Model):
    item_dtls=models.ForeignKey(Cart, on_delete=models.CASCADE)
    quant=models.IntegerField()
    total=models.IntegerField()


class Bookings(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('dispatched', 'Dispatched'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user_details=models.ForeignKey(Petuser,on_delete=models.CASCADE)
    item_details=models.ForeignKey(Product,on_delete=models.CASCADE)
    date=models.DateField()
    quantity=models.IntegerField()
    total_price=models.IntegerField()
    delivery_address=models.TextField(blank=True, null=True)
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

class ServiceBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(Petuser, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    pet_name = models.CharField(max_length=50)
    pet_type = models.CharField(max_length=50)
    booking_date = models.DateField()
    booking_slot = models.CharField(max_length=20)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet_name} - {self.service.servicename}"
