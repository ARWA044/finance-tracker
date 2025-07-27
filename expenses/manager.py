from django.db import models

class TransactionQuerySet(models.QuerySet):
    def income(self):
        return self.filter(type='income')
    def expense(self):
        return self.filter(type='expense')
    
    def Total_income(self):
        return self.income().aggregate(
            total=models.Sum("amount")
        )['total'] or 0
        
    def Total_expense(self):
        return self.expense().aggregate(
            total=models.Sum("amount")
        )['total'] or 0