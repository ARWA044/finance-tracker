import pytest
from expenses.models import Transaction

@pytest.mark.django_db
def test_queryset_income_method(transactions):
    qs=Transaction.objects.income()
    assert qs.count()>0
    assert all(
        [t.type=='income' for t in qs]
    )
@pytest.mark.django_db
def test_queryset_expense_method(transactions):
    qs=Transaction.objects.expense()
    assert qs.count()>0
    assert all(
        [t.type=='expense' for t in qs]
    )
@pytest.mark.django_db
def test_queryset_Total_income_method(transactions):
    Total_income=Transaction.objects.Total_income()
    assert Total_income==sum([t.amount for t in transactions if t.type=='income'])
    
@pytest.mark.django_db
def test_queryset_Total_expense_method(transactions):
    Total_expense=Transaction.objects.Total_expense()
    assert Total_expense==sum([t.amount for t in transactions if t.type=='expense'])