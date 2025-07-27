from django.db import models
from django.contrib.auth.models import AbstractUser
from expenses.manager import TransactionQuerySet

# Create your models here.
class User(AbstractUser):
    pass

class Category(models.Model):
    name=models.CharField(max_length=10)
    icon = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural='categories'
    def __str__(self):
        return self.name 
        
class Transaction(models.Model):
    TRANSACTION_TYPE=(
        ('income','Income'),
        ('expense','Expense'),
    )
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    type=models.CharField( max_length=10,choices=TRANSACTION_TYPE)
    amount=models.DecimalField( max_digits=10, decimal_places=2)
    time=models.DateField()  
    objects=TransactionQuerySet.as_manager()
    def __str__(self):
        return f"{self.type} of {self.amount} on {self.time} by {self.user}" 
    class Meta: 
        ordering=['-time']   