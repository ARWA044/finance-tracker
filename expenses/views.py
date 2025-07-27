from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from expenses.filters import TransactionFilter
from expenses.forms import TransactionForm
from expenses.models import Transaction,Category
from .charts import Total_income_expense_bar_charts,category_pie_chart
from django.http import HttpResponse
from expenses.resources import TransactionResource
import tablib
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator


# Create your views here.
def home(request):
    return render(request,'expenses/home.html')

@login_required
def Transactions(request):
    transaction=Transaction.objects.filter(user=request.user).select_related('category')
    transacion_filter=TransactionFilter(
        request.GET,
        queryset=transaction,
    )
    paginator=Paginator(transacion_filter.qs,settings.PAGE_SIZE)
    transaction_page = paginator.page(1)
    Totale_Income=transacion_filter.qs.Total_income()
    Totale_Expense=transacion_filter.qs.Total_expense()
    context={ 'transactions':transaction_page,
             'filter':transacion_filter,
             'Totale_Income':Totale_Income,
              'Totale_Expense':Totale_Expense,
              'Net_income':Totale_Income-Totale_Expense,
             
             }
    if request.htmx:
        return render(request, 'partials/Transactions_container.html',context)
        
    return render(request, 'expenses/Transactions.html',context)
@login_required
def get_transaction(request):
    transaction=Transaction.objects.filter(user=request.user).select_related('category')
    transacion_filter=TransactionFilter(
        request.GET,
        queryset=transaction,
    )
    paginator=Paginator(transacion_filter.qs,settings.PAGE_SIZE)
    page_number = request.GET.get("page") or 1
    transactions = paginator.get_page(page_number)
    context = {
        'transactions': transactions,
    }
    return render(
        request,
        'partials/Transactions_container.html#transaction_list',
        context
    )


@login_required
def Add_Transaction(request):
    form = TransactionForm()
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if  form.is_valid():     
            transaction = form.save(commit=False)
            transaction.user = request.user  
            transaction.save()
            return render(request,'partials/success_transaction.html',{'message':'transaction has been added successfuly'})  

    return render(request, 'partials/add_transaction.html' , {'form': form})

@login_required
def update_transaction(request,pk):
    transaction=get_object_or_404(Transaction,pk=pk,user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST,instance=transaction)
        if  form.is_valid():     
            transaction = form.save()
            return render(request,'partials/success_transaction.html',{'message':'transaction was updated successefuly'})  
            
    context = {
        'form': TransactionForm(instance=transaction),
        'transaction': transaction,
    }
    return render(request, 'partials/update_transaction.html' ,context)

@require_http_methods('DELETE')
@login_required
def delete_transaction(request,pk):
    transaction=get_object_or_404(Transaction,pk=pk,user=request.user)
    transaction.delete()
    
    return render(request,'partials/success_transaction.html',{'message':f'transaction of {transaction.amount } in {transaction.time} is successefuly deleted '})
                   

@login_required
def Charts(request):
    transaction=Transaction.objects.filter(user=request.user).select_related('category')
    transacion_filter=TransactionFilter(
        request.GET,
        queryset=transaction,
    )
    income_expense_bar_charts=Total_income_expense_bar_charts(transacion_filter.qs)
    income_category_pie_charts=category_pie_chart(transacion_filter.qs.filter(type='income'))
    expense_category_pie_charts=category_pie_chart(transacion_filter.qs.filter(type='expense'))
    context={'filter':transacion_filter,
             'income_expense_barcharts':income_expense_bar_charts.to_html(),
             'income_category_piecharts':income_category_pie_charts.to_html(),
             'expense_category_piecharts':expense_category_pie_charts.to_html(),
            
             }
    if request.htmx:
        return render(request, 'partials/Charts_container.html',context)
        
    return render(request, 'expenses/Charts.html',context)
    

@login_required
def export(request):
    if request.htmx:
        return HttpResponse(headers={'Hx-redirect':request.get_full_path()})
    transaction=Transaction.objects.filter(user=request.user).select_related('category')
    transacion_filter=TransactionFilter(    
        request.GET,
        queryset=transaction,
    )
    data=TransactionResource().export(transacion_filter.qs)
    response=HttpResponse(data.csv)
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
    return response

                
@login_required
def import_transaction(request):
    if request.method=='POST':
        file = request.FILES['file']  
        raw_data = file.read().decode('utf-8-sig')
        csv_data = raw_data.replace(';', ',')  # Fix separator

        dataset = tablib.Dataset().load(csv_data, format='csv')
        result = TransactionResource().import_data(dataset, user=request.user, dry_run= True )
        for row in result:
             for error in row.errors:
                print(error.error)
        
        if not result.has_errors():
            TransactionResource().import_data(dataset, user=request.user, dry_run=False)
            context = {'message': f'{len(dataset)} transactions were uploaded successfully'}
        else:
            context = {'message': 'Sorry, an error occurred.'}
        return render(request, 'partials/success_transaction.html', context)
    
    return render( request, 'partials/import.html')
        