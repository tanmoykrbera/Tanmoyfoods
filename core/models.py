import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='customer/avatars/', blank=True, null=True)


    def __str__(self):
        return self.user.get_full_name()

class Courier(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  lat = models.FloatField(default=0)
  lng = models.FloatField(default=0)
  

  def __str__(self):
    return self.user.get_full_name()        


class Category(models.Model):
  slug = models.CharField(max_length=255, unique=True)
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name

class Job(models.Model):
  SMALL_SIZE = "small"
  MEDIUM_SIZE = "medium"
  LARGE_SIZE = "large"
  SIZES = (
    (SMALL_SIZE, 'Small'),
    (MEDIUM_SIZE, 'Medium'),
    (LARGE_SIZE, 'Large'),
  )

  CREATING_STATUS = 'creating'
  PROCESSING_STATUS = 'processing'
  PICKING_STATUS = 'picking'
  DELIVERING_STATUS = 'delivering'
  COMPLETED_STATUS = 'completed'
  CANCELED_STATUS = 'canceled'
  STATUSES = (
    (CREATING_STATUS, 'Creating'),
    (PROCESSING_STATUS, 'Processing'),
    (PICKING_STATUS, 'Picking'),
    (DELIVERING_STATUS, 'Delivering'),
    (COMPLETED_STATUS, 'Completed'),
    (CANCELED_STATUS, 'Canceled'),
  )



  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  courier = models.ForeignKey(Courier, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=255)
  description = models.CharField(max_length=255)
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
  size = models.CharField(max_length=20, choices=SIZES, default=MEDIUM_SIZE)
  quantity = models.IntegerField(default=1)
  photo = models.ImageField(upload_to='job/photos/')
  status = models.CharField(max_length=20, choices=STATUSES, default=CREATING_STATUS)
  created_at = models.DateTimeField(default=timezone.now) 

  pickup_address = models.CharField(max_length=255, blank=True)
  pickup_lat = models.FloatField(default=0)
  pickup_lng = models.FloatField(default=0)
  pickup_name = models.CharField(max_length=255, blank=True)
  pickup_phone = models.CharField(max_length=50, blank=True)

  delivery_address = models.CharField(max_length=255, blank=True)
  delivery_lat = models.FloatField(default=0)
  delivery_lng = models.FloatField(default=0)
  delivery_name = models.CharField(max_length=255, blank=True)
  delivery_phone = models.CharField(max_length=50, blank=True)



  def __str__(self):
    return self.name          
    




