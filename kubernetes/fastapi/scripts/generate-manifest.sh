#!/bin/bash

# Convert .env to ConfigMap
echo "apiVersion: v1
kind: ConfigMap
metadata:
  name: config
data:" > k8s/configmap.yaml
grep -v '^#' .env | grep -v '^$' | grep -v 'DATABASE_PASSWORD' | sed 's/^/  /' >> k8s/configmap.yaml

# Convert .env to Secret
echo "apiVersion: v1
kind: Secret
metadata:
  name: secrets
type: Opaque
data:" > k8s/secrets.yaml
grep 'DATABASE_PASSWORD' .env | awk -F= '{print "  " $1 ": " $2}' | base64 >> k8s/secrets.yaml