import datetime

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from gql.transport.aiohttp import AIOHTTPTransport

# Select your transport with a defined url endpoint
transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")

# Create a GraphQL client using the defined transport
client = Client(transport=transport)




def log_crm_heartbeat():
    """
    DD/MM/YYYY-HH:MM:SS CRM is alive
    """

    datetime_now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
        log_file.write(f"{datetime_now} CRM is alive\n")

    # Provide a GraphQL query
    query = gql(
        """
        query {
            hello
        }
    """
    )

    # Execute the query
    response = client.execute(query)
    print(response)


def update_low_stock():
    query = gql(
        """
        mutation {
            updateLowStockProducts {
                products {
                    id
                    name
                    stock
                    price
                }
            }
        }
    """
    )
    response = client.execute(query)
    print(response)

    with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
        log_file.write(f"Low stock products updated at {datetime.datetime.now()}\n")
        for product in response['updateLowStockProducts']['products']:
            log_file.write(
                f"Product ID: {product['id']}, Name: {product['name']}, Stock: {product['stock']}, Price: {product['price']}\n"
            )
        log_file.write("\n")  # Add a newline for better readability

    print("Low stock products updated and logged!")
    