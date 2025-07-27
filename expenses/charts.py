import plotly.express as px
from django.db import models
from .models import Category



def Total_income_expense_bar_charts(qs):
    x_vals=['income','expense']
    Total_income=qs.filter(type='income').aggregate(total=models.Sum('amount'))['total']
    Total_expese=qs.filter(type='expense').aggregate(total=models.Sum('amount'))['total']
    y_vals=[Total_income,Total_expese]
    fig = px.bar(x=x_vals, y=y_vals)
    return fig

def category_pie_chart(qs):
    count_category=qs.order_by('category').values('category').annotate(total=models.Sum('amount'))
    category_pks=count_category.values_list('category',flat=True)
    categories=Category.objects.filter(pk__in=category_pks).values_list('name', flat=True)
    total=count_category.values_list('total',flat=True)
    fig = px.pie(values=total, names=categories)
    return fig