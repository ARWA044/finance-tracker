
"""
URL configuration for monprojet project.
"""

from django.contrib import admin
from django.urls import path, include
from expenses import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.home, name='home'),
    path('transactions/', views.Transactions, name='Transactions'),
    path('transactions/add_transactions/', views.Add_Transaction, name='Add_Transactions'),
    path('charts/', views.Charts, name='Charts'),
    path('transactions/<int:pk>/update/', views.update_transaction, name='update_transaction'),
    path('transactions/<int:pk>/delete/', views.delete_transaction, name='delete_transaction'),
    path('transactions/export/', views.export, name='export'),
    path('transactions/import/', views.import_transaction, name='import'),
    path('get_transaction/', views.get_transaction, name='get_transaction'),
]

# Only include debug toolbar in development
from django.conf import settings
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass  # Debug toolbar not installed
