from django.core.management.base import BaseCommand
import random
from faker import Faker
from expenses.models import User,Category,Transaction

class Command(BaseCommand):
    help='generate data for testing'
    
    
    def handle(self, *args, **options):
          
        faker=Faker()
        category_icon_map = {
    'Food': 'fa-solid fa-utensils',
    'Bills': 'fa-solid fa-file-invoice',
    'Cloths': 'fa-solid fa-shirt',
    'Medical': 'fa-solid fa-kit-medical',
    'Housing': 'fa-solid fa-house-user',
    'Salary': 'fa-solid fa-money-bill-wave',
    'Social': 'fa-solid fa-users',
    'Transport': 'fa-solid fa-car-side',
    'Vacation': 'fa-solid fa-umbrella-beach',
}
  
        for name, icon in category_icon_map.items():
            Category.objects.create(name=name, icon=icon)
        category=Category.objects.all()
    
        user=User.objects.filter(username='arwa').first()
        if not user:
            user=User.objects.create_superuser(username='arwa',password='172004')
        
        types=[x[0] for x in Transaction.TRANSACTION_TYPE]   
        for i in range(20):
            Transaction.objects.create(
                user=user,
                category=random.choice(category),
                type=random.choice(types),
                amount=random.uniform(1,2500),
                time=faker.date_between(start_date='-1y',end_date='today')
            
        )
    
