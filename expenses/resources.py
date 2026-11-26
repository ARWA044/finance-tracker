from import_export import resources, fields
from expenses.models import Transaction, Category
from import_export.widgets import ForeignKeyWidget


class TransactionResource(resources.ModelResource):
    """Export only. Imports are validated and created by the authenticated view."""
    category = fields.Field(column_name='category', attribute='category',
                            widget=ForeignKeyWidget(Category, field='name'))

    def import_data(self, *args, **kwargs):
        raise NotImplementedError("Use the authenticated CSV import view.")

    class Meta:
        model = Transaction
        fields = ('type', 'category', 'amount', 'time')
        export_order = fields
