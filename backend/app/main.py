from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import pyodbc
import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Initialize FastAPI app
app = FastAPI()

# Configurations
key_vault_name = os.getenv("KEY_VAULT_NAME")
key_vault_url = f"https://{key_vault_name}.vault.azure.net"
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
openai.api_key = secret_client.get_secret("OpenAI-API-Key").value

search_service_endpoint = os.getenv("SEARCH_SERVICE_ENDPOINT")
search_service_api_key = secret_client.get_secret("Search-Service-Api-Key").value
search_client = SearchClient(endpoint=search_service_endpoint, index_name="pharmacy-index", credential=AzureKeyCredential(search_service_api_key))

sql_conn_str = secret_client.get_secret("SQL-Conn-String").value

# Models
class UserQuery(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"message": "Pharmacy Chatbot Backend"}

@app.post("/ask")
async def ask_chatbot(user_query: UserQuery):
    try:
        response = openai.Completion.create(
            engine="your-engine-id",
            prompt=user_query.query,
            max_tokens=100,
        )
        return {"response": response.choices[0].text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search")
def search_pharmacy(query: str):
    try:
        results = search_client.search(query)
        return {"results": [doc for doc in results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/medications/{name}")
def get_medication(name: str):
    try:
        conn = pyodbc.connect(sql_conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medications WHERE Name = ?", name)
        result = cursor.fetchone()
        if result:
            return {"name": result[0], "details": result[1]}
        else:
            return {"message": "Medication not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
