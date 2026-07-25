// deploy/infrastructure.bicep
targetScope = 'resourceGroup'

param location string = resourceGroup().location
param projectName string = 'fabric-semantic-assistant'
param aiHubName string = 'hub-enterprise-analytics'
param keyVaultName string = 'kv-fabric-agent-${uniqueString(resourceGroup().id)}'

// 1. Azure Key Vault (For secure credential storage)
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
  }
}

// 2. Azure AI Foundry Hub
resource aiHub 'Microsoft.MachineLearningServices/workspaces@2024-01-01-preview' = {
  name: aiHubName
  location: location
  kind: 'Hub'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: 'Enterprise Analytics AI Hub'
    description: 'Central hub for data analytics AI agents'
    keyVault: keyVault.id
  }
}

// 3. Azure AI Foundry Project
resource aiProject 'Microsoft.MachineLearningServices/workspaces@2024-01-01-preview' = {
  name: projectName
  location: location
  kind: 'Project'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: 'Fabric Semantic Model Assistant'
    description: 'Agent for generating and debugging T-SQL against Fabric metadata'
    hubResourceId: aiHub.id
  }
}