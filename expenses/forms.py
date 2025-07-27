from django import forms
from .models import Transaction,Category


class TransactionForm(forms.ModelForm):
    category=forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.RadioSelect(),
    )
    class Meta:
        model=Transaction
        fields=(
            'type',
            'category',
            'amount',
            'time',
            
        )
        widgets={
            'time': forms.DateInput(attrs={'type':'date'}),
        }
    

    
    
    
