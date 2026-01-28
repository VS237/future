from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid
from uuid import uuid4

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Customer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=100, default=" ")
    first_name = models.CharField(max_length=100, default=" ")
    last_name = models.CharField(max_length=100, default=" ")
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    address = models.TextField(max_length=100, default=" ")
    city = models.CharField(max_length=100, default="Douala")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Message(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=200) # We will map Project Scope here
    message = models.TextField()
    email_at_time = models.EmailField(null=True, blank=True) # Backup if guest
    
    def __str__(self):
        return f"{self.subject} from {self.customer}"