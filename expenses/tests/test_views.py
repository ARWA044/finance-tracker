import pytest
from django.urls import reverse
import random
from datetime import datetime, timedelta
from  expenses.models import Category,Transaction


@pytest.mark.django_db
def test_total_values_views(user_transactions,client):
    user=user_transactions[0].user
    client.force_login(user)
    total_income=sum([t.amount for t in user_transactions if t.type=='income'])
    total_expense=sum([t.amount for t in user_transactions if t.type=='expense'])
    net=total_income-total_expense
    
    response=client.get(reverse('Transactions'))
    
    assert response.context['Totale_Income']==total_income
    assert response.context['Totale_Expense']==total_income
    assert response.context['Net_income']==net
    
@pytest.mark.django_db
def test_type_filter(user_transactions,client):
    user=user_transactions[0].user
    client.force_login(user)
    GET_PARAMS={'transaction_type':'income'}
    response=client.get(reverse('Transactions'),GET_PARAMS)
    qs=response.context['filter'].qs
    
    for t in qs:  
        assert t.type=='income'
        
    GET_PARAMS={'transaction_type':'expense'}
    response=client.get(reverse('Transactions'),GET_PARAMS)
    qs=response.context['filter'].qs
    
    for t in qs:  
        assert t.type=='expense'

@pytest.mark.django_db
def test_category_filter(user_transactions,client):
    user=user_transactions[0].user
    client.force_login(user) 
    category_name=Category.objects.all()[:2].values_list('pk',flat=True)
    GET_PARAMS={'category_type':category_name }
    response=client.get(reverse('Transactions'),GET_PARAMS)
    qs=response.context['filter'].qs
    
    for t in qs:  
        assert t.category.pk in  category_name  


@pytest.mark.django_db
def test_date_filter(user_transactions,client):
    user=user_transactions[0].user
    client.force_login(user)
    start_date=datetime.now().date()-timedelta(days=120)
    GET_PARAMS={'start_date':start_date}
    response=client.get(reverse('Transactions'),GET_PARAMS)
    qs=response.context['filter'].qs
    
    for t in qs:  
        assert t.time>=start_date
        
    end_date=datetime.now().date()-timedelta(days=20)
    GET_PARAMS={'end_date':end_date}
    response=client.get(reverse('Transactions'),GET_PARAMS)
    qs=response.context['filter'].qs
    
    for t in qs:  
        assert t.time<=end_date
        
@pytest.mark.django_db
def test_update_transaction(user,transaction_params,client):
    client.force_login(user)
    assert Transaction.objects.filter(user=user).count()==1
    
    transaction=Transaction.objects.first()
    
    now=datetime.now().date()
    transaction_params['amount']=40
    transaction_params['time']=now
    client.post(
        reverse('update_transaction',kwargs={'pk':transaction.pk}),
        transaction_params
        
    )
    
    assert Transaction.objects.filter(user=user).count()==1
    transaction=Transaction.objects.first()
    assert transaction.time==now
    assert transaction.amount==40
    
@pytest.mark.django_db
def test_delete_transaction(user,transaction_params,client):
    client.force_login(user)
    assert Transaction.objects.filter(user=user).count()==1
    transaction=Transaction.objects.first()
    client.delete(
        reverse('delete_transaction',kwargs={'pk':transaction.pk}),
        transaction_params
        
    )
    
    assert Transaction.objects.filter(user=user).count()==0
    


    
    
    
    
    