import django_filters
from expenses.models import Transaction ,Category
from django import forms

class TransactionFilter(django_filters.FilterSet):
    transaction_type=django_filters.ChoiceFilter(
        choices=Transaction.TRANSACTION_TYPE,
        field_name='type',
        lookup_expr='iexact',
        empty_label='Any',
    )
    category_type=django_filters.ModelMultipleChoiceFilter(
        field_name='category', 
        queryset=Category.objects.all() ,
        widget=forms.CheckboxSelectMultiple(),

    )
    start_date=django_filters.DateFilter(
        field_name='time',
        lookup_expr='gte',
        label='Date From',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date=django_filters.DateFilter(
        field_name='time',
        lookup_expr='lte',
        label='Date To',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    
    class Meta:
        model=Transaction
        fields=(
            'transaction_type',
            'start_date',
            'end_date',
            "category_type",
            )
