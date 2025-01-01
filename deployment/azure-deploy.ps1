# Variables
$RESOURCE_GROUP = "pharmacy-chatbot-rg"
$LOCATION = "eastus"
$APP_NAME = "pharmacy-chatbot"
$SQL_SERVER_NAME = "pharmacy-sql-server"
$SQL_DB_NAME = "pharmacy-db"
$SEARCH_SERVICE_NAME = "pharmacy-search"
$KEY_VAULT_NAME = "pharmacy-keyvault"

# Read credentials from .env file
$envVars = Get-Content .env | ForEach-Object {
    $key, $value = $_ -split '=', 2
    [PSCustomObject]@{Key=$key.Trim();Value=$value.Trim()}
} | ConvertFrom-Csv -Delimiter ','

$ADMIN_USER = $envVars | Where-Object { $_.Key -eq "ADMIN_USER" } | Select-Object -ExpandProperty Value
$ADMIN_PASSWORD = $envVars | Where-Object { $_.Key -eq "ADMIN_PASSWORD" } | Select-Object -ExpandProperty Value

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Azure OpenAI instance
az cognitiveservices account create `
    --name "$APP_NAME-openai" `
    --resource-group $RESOURCE_GROUP `
    --kind OpenAI `
    --sku S0 `
    --location $LOCATION `
    --yes

# Create SQL Server and Database
az mysql flexible-server create `
    --name pharmacy-sql-server `
    --resource-group pharmacy-chatbot-rg `
    --location westus `
    --admin-user adminuser `
    --admin-password adminpassword `
    --sku-name Standard_B1ms `
    --version 5.7 `
    --storage-size 32 `
    --public-access none

az mysql flexible-server db create `
    --resource-group pharmacy-chatbot-rg `
    --server-name pharmacy-sql-server `
    --database-name pharmacydb

# Create Azure Cognitive Search
az search service create `
    --name $SEARCH_SERVICE_NAME `
    --resource-group $RESOURCE_GROUP `
    --sku basic `
    --location $LOCATION

# Create Azure Key Vault
az keyvault create `
    --name $KEY_VAULT_NAME `
    --resource-group $RESOURCE_GROUP `
    --location $LOCATION

# Create App Service Plan
az appservice plan create `
    --name "$APP_NAME-plan" `
    --resource-group $RESOURCE_GROUP `
    --sku B1 `
    --is-linux

# Create Backend and Frontend Web Apps
az webapp create `
    --name "$APP_NAME-backend" `
    --resource-group $RESOURCE_GROUP `
    --plan "$APP_NAME-plan" `
    --runtime "PYTHON|3.9"

az webapp create `
    --name "$APP_NAME-frontend" `
    --resource-group $RESOURCE_GROUP `
    --plan "$APP_NAME-plan" `
    --runtime "PYTHON|3.9"
    