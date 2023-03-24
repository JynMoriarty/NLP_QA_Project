#!/bin/bash

ACI_PERS_RESOURCE_GROUP=RG_GANFOUDI
ACI_PERS_STORAGE_ACCOUNT_NAME=storageganfoudi
ACI_PERS_LOCATION=francecentral
ACI_PERS_SHARE_NAME=fielshare1
STORAGE_KEY=$(az storage account keys list --resource-group $ACI_PERS_RESOURCE_GROUP --account-name $ACI_PERS_STORAGE_ACCOUNT_NAME --query "[0].value" --output tsv)
echo $STORAGE_KEY

az container create \
  --resource-group $ACI_PERS_RESOURCE_GROUP \
  --name question-answering2 \
  --image anasgfdi/nlp-qa:nlp \
  --dns-name-label question-answering2 \
  --ports 80 \
  --ip-address public \
  --environment-variables "SECRET_KEY=django-insecure-ogzze$cxfkdrh@(sm6g9)n^ama17)kt@7=)@se2qc5l-7-b=rd" "credential=e518b6bec9204e41b9cf4b968ddc83f6" \
  --azure-file-volume-account-name $ACI_PERS_STORAGE_ACCOUNT_NAME \
  --azure-file-volume-account-key $STORAGE_KEY \
  --azure-file-volume-share-name $ACI_PERS_SHARE_NAME \
  --azure-file-volume-mount-path /aci/logs/