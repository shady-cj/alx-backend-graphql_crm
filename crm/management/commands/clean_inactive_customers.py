from django.core.management.base import BaseCommand

from crm.models import Customer
from django.utils import timezone

class Command(BaseCommand):
    help = 'Cleans up inactive customers who have not placed orders in the last year.'

    def handle(self, *args, **kwargs):
        one_year_ago = timezone.now() - timezone.timedelta(days=365)
        inactive_customers = Customer.objects.filter(order__order_date__lte=one_year_ago)

        count = inactive_customers.count()
        inactive_customers.delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} inactive customers.'))