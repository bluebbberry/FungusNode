import requests

class RdfService:
    def __init__(self, base_url="http://localhost:3030", dataset="dataset"):
        self.update_url = f"{base_url}/{dataset}/update"
        self.headers = {"Content-Type": "application/sparql-update"}

    def insert_data(self, sparql_insert_query):
        response = requests.post(self.update_url, data=sparql_insert_query, headers=self.headers)
        return response.status_code, response.text

# Example usage
if __name__ == "__main__":
    service = RdfService()
    insert_query = """
    PREFIX ex: <http://example.org/>
    INSERT DATA {
        ex:agent1 ex:hasPublicKey "key123" ;
                  ex:hasIPAddress "192.168.1.10" ;
                  ex:hasStatus "active" .
    }
    """
    status, msg = service.insert_data(insert_query)
    print(f"Insert Status: {status}, Message: {msg}")
