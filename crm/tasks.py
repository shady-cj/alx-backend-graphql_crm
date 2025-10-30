from gql import Client, gql
from celery import shared_task
from gql.transport.aiohttp import AIOHTTPTransport
import requests
from datetime import datetime

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="http://localhost:8000/graphql")

# Create a GraphQL client using the defined transport
client = Client(transport=transport)

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def generate_crm_report():

    # Provide a GraphQL query
    query = gql(
        """
        query {
            totalOrders 
            totalRevenue
            totalCustomers

        }
    """
    )

    # Execute the query on the transport
    result = client.execute(query)
    total_orders = result['totalOrders']
    total_revenue = result['totalRevenue']
    total_customers = result['totalCustomers']
    with open('/tmp/crm_report_log.txt', 'a') as f:
        datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{datetime_now} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue")
        f.write("\n")  # Add a newline for better readability
