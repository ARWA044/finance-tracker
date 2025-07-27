import factory
from .models import User,Transaction,Category
from datetime import datetime

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User  # Equivalent to ``model = myapp.models.User``
        django_get_or_create = ('username',)

    username =factory.sequence(lambda n:'user%d' %n)
    
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category # Equivalent to ``model = myapp.models.User``
        django_get_or_create = ('name',)

    name =factory.Iterator(
        ['Food','Bills','Cloths','Medical','Housing','Salary','Social','Transport','Vacation'] 
        
    )
class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction # Equivalent to ``model = myapp.models.User``
        
    user=factory.SubFactory(UserFactory)
    category=factory.SubFactory(CategoryFactory)
    type =factory.Iterator(
        [x[0] for x in Transaction.TRANSACTION_TYPE] 
        
    )   
    amount=6
    time=factory.Faker(
        'date_between',
        start_date=datetime(year=2022,month=2,day=3).date(),
        end_date=datetime.now().date(),
    )
     
    