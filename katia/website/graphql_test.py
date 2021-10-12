from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

transport = RequestsHTTPTransport(
    url="https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql", verify=True, retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

query = gql(
    """
    query {
        bikeRentalStations {
            bikesAvailable
            spacesAvailable
            stationId
            }
        }
"""
)

result = client.execute(query)
print("There are",len(result['bikeRentalStations']),"stations")
for i in result['bikeRentalStations']:
    print('Station',i['stationId'],':',i['bikesAvailable'],"bikes available and",i['spacesAvailable'],'spaces available')