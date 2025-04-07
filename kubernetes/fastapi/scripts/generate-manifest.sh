#!/bin/bash

# Create output directory if it doesn't exist
mkdir -p k8s/

# Convert .env to ConfigMap (non-sensitive variables)
echo "Creating ConfigMap..."
echo "apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:" > k8s/configmap.yaml

# Add non-sensitive variables to ConfigMap
grep -v '^#' .env | grep -v '^$' | grep -vE 'SECRET_KEY|POSTGRES_PASSWORD|JWT_PRIVATE_KEY|JWT_PUBLIC_KEY|EMAIL_PASSWORD|TWILIO_AUTH_TOKEN' | while read -r line; do
  key=$(echo "$line" | cut -d= -f1)
  value=$(echo "$line" | cut -d= -f2-)
  echo "  $key: \"$value\"" >> k8s/configmap.yaml
done

# Convert .env to Secret (sensitive variables)
echo "Creating Secret..."
echo "apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:" > k8s/secrets.yaml

# Add sensitive variables to Secret (using stringData to avoid manual base64 encoding)
grep -E 'SECRET_KEY|POSTGRES_PASSWORD|JWT_PRIVATE_KEY|JWT_PUBLIC_KEY|EMAIL_PASSWORD|TWILIO_AUTH_TOKEN' .env | grep -v '^#' | while read -r line; do
  key=$(echo "$line" | cut -d= -f1)
  value=$(echo "$line" | cut -d= -f2-)
  echo "  $key: \"$value\"" >> k8s/secrets.yaml
done

echo "Manifests created in k8s/configmap.yaml and k8s/secrets.yaml"