import requests

class RdfService:
    def __init__(self, base_url="http://localhost:3030", dataset="my-knowledge-base"):
        self.update_url = f"{base_url}/{dataset}/update"
        self.headers = {"Content-Type": "application/sparql-update"}

    def insert_data(self, sparql_insert_query):
        response = requests.post(self.update_url, data=sparql_insert_query, headers=self.headers)
        return response.status_code, response.text

    def insert_loss_accuracy(self, agent_id, loss, accuracy):
        sparql_insert_query = f'''
        PREFIX ex: <http://example.org/>
        INSERT DATA {{
            ex:{agent_id} ex:hasLoss "{loss}" ;
                        ex:hasAccuracy "{accuracy}" .
        }}
        '''
        return self.insert_data(sparql_insert_query)
