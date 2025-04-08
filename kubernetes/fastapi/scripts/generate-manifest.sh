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
if [ -f .env ]; then
  grep -v '^#' .env | grep -v '^$' | grep -vE 'SECRET_KEY|POSTGRES_PASSWORD|JWT_PRIVATE_KEY|JWT_PUBLIC_KEY|EMAIL_PASSWORD|TWILIO_AUTH_TOKEN' | while read -r line; do
    key=$(echo "$line" | cut -d= -f1)
    value=$(echo "$line" | cut -d= -f2-)
    # Escape special characters in the value
    value=$(printf '%s' "$value" | sed -e 's/[\/&]/\\&/g')
    echo "  $key: \"$value\"" >> k8s/configmap.yaml
  done
else
  echo "Warning: .env file not found. Created empty ConfigMap."
fi

# Convert .env to Secret (sensitive variables)
echo "Creating Secret..."
echo "apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:" > k8s/secrets.yaml

# Add sensitive variables to Secret with base64 encoding
if [ -f .env ]; then
  grep -E 'SECRET_KEY|POSTGRES_PASSWORD|JWT_PRIVATE_KEY|JWT_PUBLIC_KEY|EMAIL_PASSWORD|TWILIO_AUTH_TOKEN' .env | grep -v '^#' | while read -r line; do
    key=$(echo "$line" | cut -d= -f1)
    value=$(echo "$line" | cut -d= -f2-)
    # Encode the value in base64
    encoded_value=$(printf '%s' "$value" | base64 | tr -d '\n')
    echo "  $key: $encoded_value" >> k8s/secrets.yaml
  done
else
  echo "Warning: .env file not found. Created empty Secret."
fi

# Add validation for empty secrets file
if [ -f k8s/secrets.yaml ] && [ $(wc -l < k8s/secrets.yaml) -le 4 ]; then
  echo "Warning: No secrets were found in .env file. The generated Secret will be empty."
fi

echo "Manifests created in:"
echo "- k8s/configmap.yaml"
echo "- k8s/secrets.yaml"
echo ""
echo "To apply these manifests:"
echo "kubectl apply -f k8s/configmap.yaml -f k8s/secrets.yaml"