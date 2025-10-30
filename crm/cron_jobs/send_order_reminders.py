from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="http://localhost:8000/graphql")

# Create a GraphQL client using the defined transport
client = Client(transport=transport)

# Provide a GraphQL query
query = gql(
    """
    query ($date: DateTime!) {
      allOrders (orderDateGte: $date) {
        edges {
          node {
            id
            orderDate
            customerId {
              email
            } productIds {
              name
            }
          }
        }
      }
    }
"""
)




# Execute the query on the transport
from datetime import datetime, timedelta

variables = {"date": str(datetime.now() - timedelta(days=7))}
result = client.execute(query, variable_values=variables)


edges = result['allOrders']['edges']

for edge in edges:
    order = edge['node']
    order_date = order['orderDate']
    order_id = order['id']
    customer_email = order['customerId']['email']
    product_names = [product['name'] for product in order['productIds']]

    with open('/tmp/order_reminders_log.txt', 'a') as f:
        f.write(f"Order ID: {order_id}\n")
        f.write(f"Order Date: {order_date}\n")
        f.write(f"Customer Email: {customer_email}\n")
        f.write(f"Products: {', '.join(product_names)}\n")
        f.write("\n")  # Add a newline for better readability


print("Order reminders processed!")