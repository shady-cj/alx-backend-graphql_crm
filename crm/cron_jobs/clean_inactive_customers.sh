#!/bin/bash
# This script cleans up inactive customers from the CRM database.
# It removes customers with no orders since a year ago.

/c/Users/SICKBOY/ceejay/alx-backend-pro/alx-backend-graphql_crm/.env/Scripts/python /c/Users/SICKBOY/ceejay/alx-backend-pro/alx-backend-graphql_crm/manage.py clean_inactive_customers