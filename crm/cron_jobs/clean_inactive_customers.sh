#!/bin/bash
# This script cleans up inactive customers from the CRM database.
# It removes customers with no orders since a year ago.

# /c/Users/SICKBOY/ceejay/alx-backend-pro/alx-backend-graphql_crm/.env/Scripts/python /c/Users/SICKBOY/ceejay/alx-backend-pro/alx-backend-graphql_crm/manage.py clean_inactive_customers

/c/Users/SICKBOY/ceejay/alx-backend-pro/alx-backend-graphql_crm/.env/Scripts/python /c/Users/SICKBOY/ceejay/alx-backend-pro/alx-backend-graphql_crm/manage.py shell -c "from crm.models import Customer; from django.utils import timezone; from datetime import timedelta; cutoff_date = timezone.now() - timedelta(days=365); inactive_customers = Customer.objects.filter(order__order_date__lte=cutoff_date); count = inactive_customers.count(); inactive_customers.delete(); print(f'Deleted {count} inactive customers.')"