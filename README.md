# Pharmacy Chatbot Project

## Overview

The Pharmacy Chatbot is a cloud-based application designed to assist users in finding medical information and managing pharmacy-related tasks through an intelligent chatbot interface. 
This project leverages a variety of Azure services and technologies, including Streamlit, FastAPI, and key Azure components, for scalability, security, and efficiency.

# Prerequisites

1. Azure subscription.

2. Python 3.9 or higher installed locally.

3. Docker installed for local deployment.

4. Azure CLI installed and authenticated.

# Setup Guide

## Step 1: Clone the Repository

```git clone https://github.com/your-username/pharmacy-chatbot.git```

```cd pharmacy-chatbot```

## Step 2: Configure Environment Variables

Create a .env file in the root directory with the following content:

```
OPENAI_API_KEY=your-openai-api-key
SQL_CONN_STRING=your-azure-postgresql-connection-string
SEARCH_SERVICE_ENDPOINT=https://your-search-service-name.search.windows.net
SEARCH_SERVICE_API_KEY=your-search-service-api-key
KEY_VAULT_NAME=your-key-vault-name
ADMIN_USER=your-sql-admin-user
ADMIN_PASSWORD=your-sql-admin-password
```

## Step 3: Provision Azure Resources

Run the deployment script to create all required Azure resources:

```cd deployment```

```./azure-deploy.sh```

## Step 5: Build and Push Docker Container Images
Ensure Docker is running and build the backend and frontend images:
Backend
```
cd ../backend
docker build -t pharmacy-backend .
```
Frontend
```
cd ../frontend
docker build -t pharmacy-frontend .
```

Push to Azure Container Registry

```
az acr login --name yourACRName
docker tag pharmacy-backend:latest yourACRName.azurecr.io/pharmacy-backend:latest
docker push yourACRName.azurecr.io/pharmacy-backend:latest
docker tag pharmacy-frontend:latest yourACRName.azurecr.io/pharmacy-frontend:latest
docker push yourACRName.azurecr.io/pharmacy-frontend:latest
```

## Deploy To Azure App service
```
az webapp create --name "pharmacy-backend" --resource-group pharmacy-chatbot-rg --plan "pharmacy-plan" --deployment-container-image-name yourACRName.azurecr.io/pharmacy-backend:latest
az webapp create --name "pharmacy-frontend" --resource-group pharmacy-chatbot-rg --plan "pharmacy-plan" --deployment-container-image-name yourACRName.azurecr.io/pharmacy-frontend:latest
```


Usage

Open the Streamlit frontend in your browser (default: http://localhost:8501).

Type your query into the chatbot interface.

View responses and search results in real-time.
